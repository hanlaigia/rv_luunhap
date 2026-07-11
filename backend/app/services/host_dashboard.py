"""Dữ liệu dashboard Host từ SQLite."""

from __future__ import annotations

from collections import defaultdict
from datetime import date, timedelta

from backend.app.models import Accommodation, Booking, Room


def _host_bookings_query(host_id):
    return (
        Booking.query.join(Room)
        .join(Accommodation)
        .filter(Accommodation.host_id == host_id)
    )


def get_host_stats(host_id: int) -> dict:
    bookings = _host_bookings_query(host_id).all()
    rooms = (
        Room.query.join(Accommodation)
        .filter(Accommodation.host_id == host_id)
        .all()
    )
    active_rooms = sum(1 for r in rooms if r.status == "active")
    total_rooms = len(rooms)

    revenue_bookings = [
        b for b in bookings
        if b.status in (Booking.STATUS_CONFIRMED, Booking.STATUS_COMPLETED, "completed", "confirmed")
        and b.status != Booking.STATUS_CANCELLED
    ]
    total_revenue = sum(b.total_amount or 0 for b in revenue_bookings)

    today = date.today()
    month_start = today.replace(day=1)
    new_this_month = sum(
        1 for b in bookings
        if b.created_at and b.created_at.date() >= month_start
        and b.status in (Booking.STATUS_CONFIRMED, Booking.STATUS_COMPLETED)
    )

    occupied_nights = 0
    window_start = today
    window_end = today + timedelta(days=6)
    for b in bookings:
        if b.status not in (Booking.STATUS_CONFIRMED, Booking.STATUS_COMPLETED, "confirmed", "completed"):
            continue
        if b.check_out <= window_start or b.check_in > window_end:
            continue
        start = max(b.check_in, window_start)
        end = min(b.check_out, window_end + timedelta(days=1))
        occupied_nights += max(0, (end - start).days)

    capacity = max(total_rooms * 7, 1)
    occupancy_rate = round(occupied_nights / capacity * 100, 1)

    return {
        "total_revenue": total_revenue,
        "booking_count": len([b for b in bookings if b.status != Booking.STATUS_CANCELLED]),
        "new_bookings": new_this_month,
        "active_rooms": active_rooms,
        "total_rooms": total_rooms,
        "occupancy_rate": occupancy_rate,
    }


def get_revenue_chart(host_id: int, period: str = "7d") -> dict:
    """period: 7d | 30d | month (tháng hiện tại)."""
    today = date.today()
    if period == "30d":
        start = today - timedelta(days=29)
        labels_fmt = "%d/%m"
    elif period == "month":
        start = today.replace(day=1)
        labels_fmt = "%d/%m"
    else:
        start = today - timedelta(days=6)
        labels_fmt = "%a"
        period = "7d"

    day_keys = []
    cursor = start
    while cursor <= today:
        day_keys.append(cursor)
        cursor += timedelta(days=1)

    totals = defaultdict(int)
    bookings = _host_bookings_query(host_id).filter(
        Booking.status.in_([
            Booking.STATUS_CONFIRMED,
            Booking.STATUS_COMPLETED,
            "confirmed",
            "completed",
        ])
    ).all()

    for b in bookings:
        if not b.check_in:
            continue
        pay_day = b.check_in
        if pay_day < start or pay_day > today:
            continue
        totals[pay_day] += b.total_amount or 0

    if period == "7d":
        vi_days = ["T2", "T3", "T4", "T5", "T6", "T7", "CN"]
        labels = [vi_days[d.weekday()] for d in day_keys]
    else:
        labels = [d.strftime(labels_fmt) for d in day_keys]

    values = [totals[d] for d in day_keys]
    max_val = max(values) if values else 0
    avg_val = round(sum(values) / len(values)) if values else 0

    return {
        "period": period,
        "labels": labels,
        "values": values,
        "max": max_val or 1,
        "avg": avg_val,
        "subtitle": {
            "7d": "Thống kê 7 ngày gần nhất",
            "30d": "Thống kê 30 ngày gần nhất",
        }.get(period, "Thống kê doanh thu"),
    }
