from datetime import date

from flask import Blueprint, render_template, request
from flask_login import current_user, login_required
from sqlalchemy import or_

from backend.app.models import Accommodation, Booking, Room
from backend.app.services.host_copilot import infer_guest_persona
from backend.app.services.host_dashboard import get_host_stats
from backend.app.utils.host_display import filter_bookings_by_tab

booking_bp = Blueprint("booking", __name__, url_prefix="/bookings")


def _host_booking_or_404(booking_id):
    return (
        Booking.query.join(Room)
        .join(Accommodation)
        .filter(Booking.id == booking_id, Accommodation.host_id == current_user.id)
        .first_or_404()
    )


def _host_bookings_base():
    return (
        Booking.query.join(Room)
        .join(Accommodation)
        .filter(Accommodation.host_id == current_user.id)
    )


@booking_bp.route("/")
@login_required
def index():
    status_filter = request.args.get("status", "Tất cả")
    acc_id = request.args.get("acc_id", type=int)
    q = request.args.get("q", "").strip()
    date_from = request.args.get("date_from")
    date_to = request.args.get("date_to")

    query = _host_bookings_base()
    if acc_id:
        query = query.filter(Accommodation.id == acc_id)
    if q:
        like = f"%{q}%"
        query = query.filter(
            or_(
                Booking.booking_code.ilike(like),
                Booking.guest_name.ilike(like),
                Booking.guest_phone.ilike(like),
            )
        )
    if date_from:
        query = query.filter(Booking.check_in >= date_from)
    if date_to:
        query = query.filter(Booking.check_out <= date_to)

    all_bookings = query.order_by(Booking.created_at.desc()).all()
    bookings = filter_bookings_by_tab(all_bookings, status_filter)

    today = date.today()
    check_in_today = [
        b
        for b in all_bookings
        if b.check_in == today and filter_bookings_by_tab([b], "Đã hủy") == []
        and filter_bookings_by_tab([b], "Hoàn thành") == []
    ]
    check_out_today = [
        b
        for b in all_bookings
        if b.check_out == today
        and filter_bookings_by_tab([b], "Đã hủy") == []
        and filter_bookings_by_tab([b], "Hoàn thành") == []
    ]
    stats = get_host_stats(current_user.id)
    accommodations = Accommodation.query.filter_by(host_id=current_user.id).order_by(
        Accommodation.name
    ).all()

    return render_template(
        "host/booking/index.html",
        active_nav="bookings",
        active_tab=status_filter,
        bookings=bookings,
        check_in_today=check_in_today,
        check_out_today=check_out_today,
        month_revenue=stats["total_revenue"],
        accommodations=accommodations,
        selected_acc_id=acc_id,
        search_q=q,
        today=today,
    )


@booking_bp.route("/<int:id>")
@login_required
def detail(id):
    from backend.app.models import Review

    from backend.app.utils.guest_insight import build_guest_insight

    booking = _host_booking_or_404(id)
    persona = infer_guest_persona(booking)
    guest_insight = build_guest_insight(booking)
    review = None
    if booking.booking_code:
        review = Review.query.filter_by(booking_code=booking.booking_code).first()
    return render_template(
        "host/booking/detail.html",
        active_nav="bookings",
        booking=booking,
        persona=persona,
        guest_insight=guest_insight,
        review=review,
    )
