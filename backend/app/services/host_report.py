"""Báo cáo Host từ dữ liệu thật."""

from __future__ import annotations

from collections import defaultdict
from datetime import date, timedelta

from backend.app.models import Accommodation, Booking, Room
from backend.app.services.host_dashboard import get_revenue_chart
from backend.app.utils.host_display import booking_status_label, resolve_booking_display_status


def _period_start(period: str) -> date | None:
    today = date.today()
    if period == "7d":
        return today - timedelta(days=6)
    if period == "30d":
        return today - timedelta(days=29)
    if period == "year":
        return today - timedelta(days=364)
    return None  # all time


def _host_bookings(host_id: int, period: str = "30d", acc_id: int | None = None):
    start = _period_start(period)
    q = (
        Booking.query.join(Room)
        .join(Accommodation)
        .filter(Accommodation.host_id == host_id)
    )
    if acc_id:
        q = q.filter(Accommodation.id == acc_id)
    if start:
        q = q.filter(Booking.check_in >= start)
    return q.all()


def build_report_data(host_id: int, period: str = "30d", acc_id: int | None = None) -> dict:
    bookings = _host_bookings(host_id, period, acc_id)
    chart_period = period if period in ("7d", "30d") else "30d"
    chart = get_revenue_chart(host_id, chart_period)

    total_revenue = sum(
        b.total_amount or 0
        for b in bookings
        if resolve_booking_display_status(b) in ("confirmed", "staying", "completed")
    )
    completed = [b for b in bookings if resolve_booking_display_status(b) == "completed"]
    cancelled = [b for b in bookings if resolve_booking_display_status(b) == "cancelled"]
    cancel_rate = round(len(cancelled) / len(bookings) * 100, 1) if bookings else 0

    acc_stats = defaultdict(lambda: {"bookings": 0, "revenue": 0})
    room_stats = defaultdict(lambda: {"bookings": 0, "revenue": 0, "acc": ""})

    for b in bookings:
        if not b.room:
            continue
        acc_name = b.room.accommodation.name
        acc_stats[acc_name]["bookings"] += 1
        acc_stats[acc_name]["revenue"] += b.total_amount or 0
        key = (b.room.name, acc_name)
        room_stats[key]["bookings"] += 1
        room_stats[key]["revenue"] += b.total_amount or 0
        room_stats[key]["acc"] = acc_name

    accommodations_perf = sorted(
        [
            {
                "name": name,
                "bookings": data["bookings"],
                "revenue": f"{data['revenue']:,}".replace(",", ".") + "đ",
                "occupancy": min(100, data["bookings"] * 3),
            }
            for name, data in acc_stats.items()
        ],
        key=lambda x: x["bookings"],
        reverse=True,
    )[:3]

    rooms_perf = sorted(
        [
            {
                "name": name,
                "acc": data["acc"],
                "revenue": f"{data['revenue']:,}".replace(",", ".") + "đ",
                "occupancy": f"{min(100, data['bookings'] * 5)}%",
            }
            for (name, _), data in room_stats.items()
        ],
        key=lambda x: int(x["revenue"].replace(".", "").replace("đ", "") or 0),
        reverse=True,
    )[:3]

    transactions = []
    for b in sorted(bookings, key=lambda x: x.check_in or date.min, reverse=True):
        if not b.room:
            continue
        label = booking_status_label(b)
        color = "success" if label == "Hoàn thành" else ("primary" if label == "Đang lưu trú" else ("danger" if label == "Đã hủy" else "info"))
        transactions.append(
            {
                "date": b.check_in.strftime("%d/%m/%Y") if b.check_in else "—",
                "acc": b.room.accommodation.name,
                "room": b.room.name,
                "code": b.booking_code or f"#RV{b.id}",
                "revenue": f"{(b.total_amount or 0):,}".replace(",", ".") + "đ",
                "status": label,
                "status_color": color,
            }
        )

    stats = {
        "revenue": {"value": f"{total_revenue:,}".replace(",", ".") + "đ", "trend": ""},
        "bookings": {"value": str(len(bookings)), "trend": ""},
        "occupancy": {"value": f"{min(100, len(completed) * 5)}%", "trend": ""},
        "cancellation": {"value": f"{cancel_rate}%", "trend": ""},
        "nights": {"value": str(sum(b.nights for b in bookings)), "label": "đêm"},
    }

    max_bar = max(chart["values"]) if chart["values"] else 1
    bar_chart_labels = chart["labels"]
    bar_chart_values = chart["values"]

    status_counts = {"completed": 0, "staying": 0, "cancelled": 0, "other": 0}
    for b in bookings:
        st = resolve_booking_display_status(b)
        if st == "completed":
            status_counts["completed"] += 1
        elif st == "staying":
            status_counts["staying"] += 1
        elif st == "cancelled":
            status_counts["cancelled"] += 1
        else:
            status_counts["other"] += 1

    total_status = len(bookings) or 1
    status_chart = {
        "completed": status_counts["completed"],
        "staying": status_counts["staying"],
        "cancelled": status_counts["cancelled"],
        "completed_pct": round(status_counts["completed"] / total_status * 100),
        "staying_pct": round(status_counts["staying"] / total_status * 100),
        "cancelled_pct": round(status_counts["cancelled"] / total_status * 100),
    }

    accommodations = Accommodation.query.filter_by(host_id=host_id).order_by(Accommodation.name).all()

    return {
        "stats": stats,
        "bar_chart_labels": bar_chart_labels,
        "bar_chart_values": bar_chart_values,
        "status_chart": status_chart,
        "accommodations_perf": accommodations_perf,
        "rooms_perf": rooms_perf,
        "transactions": transactions,
        "accommodations": accommodations,
        "period": period,
        "acc_id": acc_id,
    }
