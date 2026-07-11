from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import or_

from backend.app.extensions import db
from backend.app.models import Accommodation, Booking, Dispute, Room

dispute_bp = Blueprint("dispute", __name__, url_prefix="/disputes")


def _host_disputes_query():
    return (
        Dispute.query.join(Booking)
        .join(Room)
        .join(Accommodation)
        .filter(Accommodation.host_id == current_user.id)
    )


def _host_dispute_or_404(dispute_id):
    return _host_disputes_query().filter(Dispute.id == dispute_id).first_or_404()


@dispute_bp.route("/")
@login_required
def index():
    status_filter = request.args.get("status", "Tất cả")
    page = request.args.get("page", 1, type=int)
    period = request.args.get("period", "30d")
    q = request.args.get("q", "").strip()
    acc_id = request.args.get("acc_id", type=int)
    room_id = request.args.get("room_id", type=int)
    per_page = 10

    query = _host_disputes_query()
    if status_filter == "Đang xử lý":
        query = query.filter(Dispute.status == Dispute.STATUS_PROCESSING)
    elif status_filter == "Cần phản hồi":
        query = query.filter(Dispute.status == Dispute.STATUS_NEEDS_RESPONSE)
    elif status_filter == "Đã giải quyết":
        query = query.filter(Dispute.status == Dispute.STATUS_RESOLVED)

    if q:
        like = f"%{q}%"
        query = query.filter(
            or_(
                Dispute.dispute_code.ilike(like),
                Booking.booking_code.ilike(like),
                Booking.guest_name.ilike(like),
            )
        )
    if acc_id:
        query = query.filter(Accommodation.id == acc_id)
    if room_id:
        query = query.filter(Room.id == room_id)

    if period == "7d":
        from datetime import date, timedelta
        start = date.today() - timedelta(days=6)
        query = query.filter(Dispute.created_at >= start)
    elif period == "30d":
        from datetime import date, timedelta
        start = date.today() - timedelta(days=29)
        query = query.filter(Dispute.created_at >= start)
    elif period == "year":
        from datetime import date, timedelta
        start = date.today() - timedelta(days=364)
        query = query.filter(Dispute.created_at >= start)

    pagination = query.order_by(Dispute.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    total_all_disputes = _host_disputes_query().count()
    needs_response_count = _host_disputes_query().filter_by(
        status=Dispute.STATUS_NEEDS_RESPONSE
    ).count()

    accommodations = Accommodation.query.filter_by(host_id=current_user.id).order_by(
        Accommodation.name
    ).all()
    rooms = (
        Room.query.join(Accommodation)
        .filter(Accommodation.host_id == current_user.id)
        .order_by(Accommodation.name, Room.name)
        .all()
    )

    return render_template(
        "host/dispute/index.html",
        active_nav="disputes",
        active_tab=status_filter,
        period=period,
        filter_q=q,
        selected_acc_id=acc_id,
        selected_room_id=room_id,
        pagination=pagination,
        total_all_disputes=total_all_disputes,
        needs_response_count=needs_response_count,
        accommodations=accommodations,
        rooms=rooms,
    )


@dispute_bp.route("/<int:id>")
@login_required
def detail(id):
    dispute = _host_dispute_or_404(id)
    return render_template(
        "host/dispute/detail.html",
        active_nav="disputes",
        dispute=dispute,
    )


@dispute_bp.route("/<int:id>/respond", methods=["POST"])
@login_required
def respond(id):
    dispute = _host_dispute_or_404(id)
    response_content = request.form.get("response_content")
    if response_content:
        dispute.host_response = response_content
        dispute.status = Dispute.STATUS_PROCESSING
        db.session.commit()
        flash("Phản hồi của bạn đã được hệ thống ghi nhận.", "success")
    return redirect(url_for("dispute.detail", id=id))
