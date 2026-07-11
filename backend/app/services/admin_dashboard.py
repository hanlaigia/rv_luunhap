"""Thống kê dashboard admin từ dữ liệu thật."""
from calendar import monthrange
from datetime import date, datetime

from sqlalchemy import extract, func

from backend.app.extensions import db
from backend.app.models import Accommodation, Booking, Dispute, Review, Room, User


def _booking_base_query():
    return Booking.query.filter(
        Booking.status.in_([Booking.STATUS_CONFIRMED, Booking.STATUS_COMPLETED])
    )


def _in_period(query, year, month=None):
    if month:
        return query.filter(
            extract("year", Booking.created_at) == year,
            extract("month", Booking.created_at) == month,
        )
    return query.filter(extract("year", Booking.created_at) == year)


def dashboard_kpis(year=None, month=None, period="month"):
    year = year or date.today().year
    bookings_q = Booking.query
    period_q = _in_period(bookings_q, year, month if period == "month" else None)

    revenue = sum(
        b.total_amount or 0
        for b in period_q.filter(
            Booking.status.in_([Booking.STATUS_CONFIRMED, Booking.STATUS_COMPLETED])
        ).all()
    )
    booking_count = period_q.count()
    completed = period_q.filter_by(status=Booking.STATUS_COMPLETED).count()
    total_in_period = booking_count or 1
    completion_rate = round(completed / total_in_period * 100, 1)

    return {
        "revenue": revenue,
        "booking_count": booking_count,
        "customer_count": User.query.filter_by(role="guest").count(),
        "host_count": User.query.filter_by(role="host", host_status="approved").count(),
        "dispute_count": Dispute.query.filter(
            Dispute.status != Dispute.STATUS_RESOLVED
        ).count(),
        "completion_rate": completion_rate,
        "pending_hosts": User.query.filter_by(host_status="pending").count(),
        "pending_accs": Accommodation.query.filter_by(
            status=Accommodation.STATUS_PENDING
        ).count(),
        "recent_bookings": Booking.query.order_by(Booking.created_at.desc()).limit(5).all(),
    }


def dashboard_charts(year=None, month=None, period="month"):
    year = year or date.today().year
    month = month or date.today().month

    if period == "year":
        labels = [f"T{m}" for m in range(1, 13)]
        revenue = []
        bookings = []
        for m in range(1, 13):
            rows = _in_period(Booking.query, year, m).all()
            bookings.append(len(rows))
            revenue.append(
                sum(
                    (b.total_amount or 0)
                    for b in rows
                    if b.status
                    in (Booking.STATUS_CONFIRMED, Booking.STATUS_COMPLETED)
                )
            )
    else:
        days_in_month = monthrange(year, month)[1]
        labels = [f"Tuần {i}" for i in range(1, 5)]
        revenue = [0, 0, 0, 0]
        bookings = [0, 0, 0, 0]
        rows = _in_period(Booking.query, year, month).all()
        for b in rows:
            created = b.created_at or datetime.utcnow()
            week_idx = min((created.day - 1) // 7, 3)
            bookings[week_idx] += 1
            if b.status in (Booking.STATUS_CONFIRMED, Booking.STATUS_COMPLETED):
                revenue[week_idx] += int(b.total_amount or 0)

    all_bookings = Booking.query.all()
    status_counts = [
        sum(1 for b in all_bookings if b.status == Booking.STATUS_COMPLETED),
        sum(
            1
            for b in all_bookings
            if b.status in (Booking.STATUS_CONFIRMED, Booking.STATUS_PENDING, Booking.STATUS_HOLDING)
        ),
        sum(1 for b in all_bookings if b.status == Booking.STATUS_CANCELLED),
    ]

    top_rows = (
        db.session.query(
            Accommodation.name.label("name"),
            func.count(Booking.id).label("booking_count"),
            func.sum(Booking.total_amount).label("revenue"),
        )
        .join(Room, Room.accommodation_id == Accommodation.id)
        .join(Booking, Booking.room_id == Room.id)
        .filter(
            Booking.status.in_([Booking.STATUS_CONFIRMED, Booking.STATUS_COMPLETED])
        )
        .group_by(Accommodation.id)
        .order_by(func.sum(Booking.total_amount).desc())
        .limit(5)
        .all()
    )

    top_hotels = []
    for row in top_rows:
        top_hotels.append(
            {
                "name": row.name,
                "bookings": int(row.booking_count or 0),
                "revenue": int(row.revenue or 0),
            }
        )

    return {
        "labels": labels,
        "revenue": revenue,
        "bookings": bookings,
        "status": status_counts,
        "top_hotels": top_hotels,
    }


def customer_booking_counts():
    rows = (
        db.session.query(Booking.guest_id, func.count(Booking.id))
        .filter(Booking.guest_id.isnot(None))
        .group_by(Booking.guest_id)
        .all()
    )
    return {guest_id: count for guest_id, count in rows}


def accommodation_stats(acc_ids):
    if not acc_ids:
        return {}
    revenue_rows = (
        db.session.query(
            Accommodation.id,
            func.sum(Booking.total_amount),
            func.count(Booking.id),
        )
        .join(Room, Room.accommodation_id == Accommodation.id)
        .join(Booking, Booking.room_id == Room.id)
        .filter(Accommodation.id.in_(acc_ids))
        .group_by(Accommodation.id)
        .all()
    )
    rating_rows = (
        db.session.query(
            Room.accommodation_id,
            func.avg(Review.rating),
        )
        .join(Review, Review.room_id == Room.id)
        .filter(Room.accommodation_id.in_(acc_ids))
        .group_by(Room.accommodation_id)
        .all()
    )
    ratings = {acc_id: round(float(avg), 1) for acc_id, avg in rating_rows}
    stats = {}
    for acc_id, revenue, bookings in revenue_rows:
        stats[acc_id] = {
            "revenue": revenue or 0,
            "bookings": bookings or 0,
            "rating": ratings.get(acc_id),
        }
    return stats
