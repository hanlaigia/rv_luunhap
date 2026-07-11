"""Dữ liệu cho admin portal SPA."""
import json
from datetime import date, datetime

from sqlalchemy import func

from backend.app.extensions import db
from backend.app.models import Accommodation, Booking, Dispute, Promotion, Review, Room, User
from backend.app.services.admin_dashboard import (
    accommodation_stats,
    customer_booking_counts,
    dashboard_charts,
    dashboard_kpis,
)


def _fmt_vnd(amount):
    return f"{int(amount or 0):,}".replace(",", ".")


def _fmt_money(amount):
    return f"{_fmt_vnd(amount)} ₫"


def _fmt_m(amount):
    return _fmt_money(amount)


def _serialize_period(kpis, charts):
    return {
        "kpis": {
            "revenue": _fmt_money(kpis["revenue"]),
            "bookings": kpis["booking_count"],
            "users": kpis["customer_count"],
            "hosts": kpis["host_count"],
            "disputes": kpis["dispute_count"],
            "completion": f"{kpis['completion_rate']}%",
        },
        "chartLabels": charts["labels"],
        "chartRevenue": charts["revenue"],
        "chartBookings": charts["bookings"],
        "status": charts["status"],
        "topHotels": [h["revenue"] for h in charts["top_hotels"]],
        "topHotelsDetail": [
            {**h, "revenue_display": _fmt_money(h["revenue"])}
            for h in charts["top_hotels"]
        ],
    }


def build_chart_database():
    today = date.today()
    database = {}
    for year in range(today.year, today.year - 5, -1):
        database[str(year)] = {"months": {}, "yearly": {}}
        yk = dashboard_kpis(year=year, period="year")
        yc = dashboard_charts(year=year, period="year")
        database[str(year)]["yearly"] = _serialize_period(yk, yc)
        for month in range(1, 13):
            mk = dashboard_kpis(year=year, month=month, period="month")
            mc = dashboard_charts(year=year, month=month, period="month")
            database[str(year)]["months"][str(month)] = _serialize_period(mk, mc)
    return database


def _activity_items():
    items = []
    for b in Booking.query.order_by(Booking.created_at.desc()).limit(3).all():
        items.append({
            "type": "success",
            "text": f"Đơn đặt phòng {b.booking_code} — {b.status}",
            "sub": b.created_at.strftime("%d/%m/%Y %H:%M") if b.created_at else "",
        })
    for d in Dispute.query.order_by(Dispute.created_at.desc()).limit(2).all():
        items.append({
            "type": "warning",
            "text": f"Tranh chấp {d.dispute_code} — {d.status}",
            "sub": d.created_at.strftime("%d/%m/%Y %H:%M") if d.created_at else "",
        })
    return items[:5]


def build_entity_catalog(booking_counts, acc_stats):
    catalog = {
        "user": {},
        "host": {},
        "room": {},
        "booking": {},
        "dispute": {},
        "payment": {},
        "promotion": {},
        "admin": {},
    }

    for user in User.query.filter_by(role="guest").all():
        bc = booking_counts.get(user.id, 0)
        if user.is_locked:
            status = "Bị khóa"
        elif bc == 0:
            status = "Không hoạt động"
        else:
            status = "Hoạt động"
        catalog["user"][f"u{user.id}"] = {
            "title": "Chi tiết khách hàng",
            "fields": [
                ("Tên", user.full_name),
                ("Email", user.email),
                ("SĐT", user.phone or "—"),
                ("Số booking", str(bc)),
                ("Trạng thái", status),
                ("Ngày tạo", user.created_at.strftime("%d/%m/%Y") if user.created_at else "—"),
            ],
        }

    for acc in Accommodation.query.all():
        st = acc_stats.get(acc.id, {})
        catalog["host"][f"h{acc.id}"] = {
            "title": "Chi tiết đơn vị lưu trú",
            "fields": [
                ("Tên", acc.name),
                ("Chủ sở hữu", acc.host.full_name if acc.host else "—"),
                ("Loại", acc.type or "—"),
                ("Địa chỉ", acc.address or acc.location or "—"),
                ("Số phòng", str(acc.total_rooms)),
                ("Doanh thu", _fmt_money(st.get("revenue", 0))),
                ("Đánh giá", f"{st['rating']} ⭐" if st.get("rating") else "—"),
                ("Trạng thái", acc.status_label),
            ],
        }

    for room in Room.query.all():
        catalog["room"][f"r{room.id}"] = {
            "title": "Chi tiết phòng",
            "id": room.id,
            "fields": [
                ("Tên phòng", room.name),
                ("Đơn vị lưu trú", room.accommodation.name if room.accommodation else "—"),
                ("Sức chứa", f"{room.capacity} người"),
                ("Giá/đêm", _fmt_money(room.base_price)),
                ("Diện tích", room.area or "—"),
                ("Trạng thái", room.status_label),
            ],
            "edit": {
                "name": room.name,
                "capacity": room.capacity,
                "base_price": room.base_price,
                "status": room.status,
            },
        }

    for b in Booking.query.all():
        catalog["booking"][f"bk{b.id}"] = {
            "title": "Chi tiết booking",
            "id": b.id,
            "status": b.status,
            "fields": [
                ("Mã booking", b.booking_code),
                ("Khách hàng", b.guest_name),
                ("Email", b.guest_email or "—"),
                ("SĐT", b.guest_phone or "—"),
                ("Khách sạn", b.room.accommodation.name if b.room and b.room.accommodation else "—"),
                ("Phòng", b.room.name if b.room else "—"),
                ("Check-in", b.check_in.strftime("%Y-%m-%d") if b.check_in else "—"),
                ("Check-out", b.check_out.strftime("%Y-%m-%d") if b.check_out else "—"),
                ("Tổng tiền", _fmt_money(b.total_amount or 0)),
                ("Trạng thái", b.status),
                ("Thanh toán", b.payment_status),
            ],
        }
        catalog["payment"][f"tx{b.id}"] = {
            "title": "Chi tiết giao dịch",
            "id": b.id,
            "paid": b.payment_status == "paid",
            "fields": [
                ("Mã giao dịch", f"TXN{b.id:03d}"),
                ("Booking", b.booking_code),
                ("Số tiền", _fmt_money(b.total_amount or 0)),
                ("Phương thức", b.payment_method or "—"),
                ("Trạng thái", "Hoàn thành" if b.payment_status == "paid" else "Chờ xử lý"),
                ("Ngày", b.created_at.strftime("%d/%m/%Y") if b.created_at else "—"),
            ],
        }

    for d in Dispute.query.all():
        booking = d.booking
        catalog["dispute"][f"ds{d.id}"] = {
            "title": "Chi tiết tranh chấp",
            "id": d.id,
            "status": d.status,
            "fields": [
                ("Mã tranh chấp", d.dispute_code),
                ("Booking", booking.booking_code if booking else "—"),
                ("Khiếu nại", d.guest_complaint or "—"),
                ("Phản hồi host", d.host_response or "—"),
                ("Giải pháp admin", d.admin_resolution or "—"),
                ("Hoàn tiền", _fmt_money(d.refund_amount or 0)),
                ("Trạng thái", d.status),
            ],
        }

    for p in Promotion.query.all():
        catalog["promotion"][f"p{p.id}"] = {
            "title": "Chi tiết khuyến mãi",
            "fields": [
                ("Tên", p.name),
                ("Loại", p.type),
                ("Giảm giá", p.discount_value or "—"),
                ("Từ ngày", p.start_date or "—"),
                ("Đến ngày", p.end_date or "—"),
                ("Trạng thái", "Hoạt động" if p.status else "Không hoạt động"),
            ],
        }

    for admin in User.query.filter_by(role="admin").all():
        catalog["admin"][f"ad{admin.id}"] = {
            "title": "Chi tiết quản trị viên",
            "fields": [
                ("Tên", admin.full_name),
                ("Email", admin.email),
                ("SĐT", admin.phone or "—"),
                ("Trạng thái", "Không hoạt động" if admin.is_locked else "Hoạt động"),
            ],
        }

    return catalog


def build_portal_context(active_view="dashboard"):
    today = date.today()
    year = today.year
    month = today.month
    kpis = dashboard_kpis(year=year, month=month, period="month")
    charts = dashboard_charts(year=year, month=month, period="month")

    users = User.query.filter_by(role="guest").order_by(User.created_at.desc()).all()
    booking_counts = customer_booking_counts()

    accommodations = Accommodation.query.order_by(Accommodation.name).all()
    acc_ids = [a.id for a in accommodations]
    acc_stats = accommodation_stats(acc_ids)

    rooms = Room.query.order_by(Room.id.desc()).all()
    bookings = Booking.query.order_by(Booking.created_at.desc()).all()
    disputes = Dispute.query.order_by(Dispute.created_at.desc()).all()
    promotions = Promotion.query.order_by(Promotion.created_at.desc()).all()
    admins = User.query.filter_by(role="admin").order_by(User.created_at.desc()).all()

    paid = [b for b in bookings if b.payment_status == "paid"]
    pending_pay = [
        b
        for b in bookings
        if b.payment_status != "paid"
        and b.status in (Booking.STATUS_CONFIRMED, Booking.STATUS_HOLDING)
    ]

    booking_counts_stat = {
        "total": len(bookings),
        "pending": sum(
            1
            for b in bookings
            if b.status in (Booking.STATUS_PENDING, Booking.STATUS_HOLDING)
        ),
        "completed": sum(1 for b in bookings if b.status == Booking.STATUS_COMPLETED),
        "cancelled": sum(1 for b in bookings if b.status == Booking.STATUS_CANCELLED),
    }

    dispute_counts = {
        "total": len(disputes),
        "open": sum(1 for d in disputes if d.status != Dispute.STATUS_RESOLVED),
        "resolved": sum(1 for d in disputes if d.status == Dispute.STATUS_RESOLVED),
    }

    paid_total = sum(b.total_amount or 0 for b in paid)
    pending_total = sum(b.total_amount or 0 for b in pending_pay)
    refund_total = sum(d.refund_amount or 0 for d in disputes if d.refund_amount)

    host_users = User.query.filter_by(role="host").order_by(User.full_name).all()
    entity_catalog = build_entity_catalog(booking_counts, acc_stats)

    return {
        "active_view": active_view,
        "current_user": None,  # filled by route
        "year": year,
        "month": month,
        "kpis": kpis,
        "charts": charts,
        "chart_database_json": json.dumps(build_chart_database()),
        "activities": _activity_items(),
        "users": users,
        "booking_counts": booking_counts,
        "accommodations": accommodations,
        "acc_stats": acc_stats,
        "rooms": rooms,
        "bookings": bookings,
        "booking_counts_stat": booking_counts_stat,
        "disputes": disputes,
        "dispute_counts": dispute_counts,
        "paid": paid,
        "pending_pay": pending_pay,
        "paid_total": paid_total,
        "pending_total": pending_total,
        "refund_total": refund_total,
        "promotions": promotions,
        "promo_active": sum(1 for p in promotions if p.status),
        "admins": admins,
        "recent_bookings": Booking.query.order_by(Booking.created_at.desc()).limit(4).all(),
        "host_users": host_users,
        "entity_catalog_json": json.dumps(entity_catalog, ensure_ascii=False),
        "fmt_vnd": _fmt_vnd,
        "fmt_m": _fmt_money,
        "fmt_money": _fmt_money,
    }


VIEW_ALIASES = {
    "customers": "users",
    "accommodations": "hosts",
}


def normalize_view(view):
    return VIEW_ALIASES.get(view, view or "dashboard")
