from datetime import datetime, timedelta

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import or_
from sqlalchemy.orm import joinedload

from backend.app.extensions import db
from backend.app.models import Accommodation, Booking, Room, Withdrawal

payment_bp = Blueprint("payment", __name__, url_prefix="/payments")

HOST_SHARE = 0.9


def _host_bookings_query(host_id):
    return (
        Booking.query.join(Room, Booking.room_id == Room.id)
        .join(Accommodation, Room.accommodation_id == Accommodation.id)
        .filter(Accommodation.host_id == host_id)
    )


def _host_share(amount):
    return int((amount or 0) * HOST_SHARE)


def _wallet_stats(host_id):
    bookings = _host_bookings_query(host_id).all()

    pending_revenue = sum(
        _host_share(b.total_amount)
        for b in bookings
        if b.payment_status == "pending"
    )
    in_dispute_amount = sum(
        _host_share(b.total_amount)
        for b in bookings
        if b.payment_status == "in_dispute"
    )
    total_credited = sum(
        _host_share(b.total_amount)
        for b in bookings
        if b.payment_status in ("disbursed", "resolved")
    )

    withdrawals = Withdrawal.query.filter_by(host_id=host_id).all()
    total_withdrawn = sum(
        w.amount for w in withdrawals if w.status == Withdrawal.STATUS_COMPLETED
    )
    total_pending_withdraw = sum(
        w.amount for w in withdrawals if w.status == Withdrawal.STATUS_PENDING
    )

    withdrawable_balance = max(
        0, total_credited - total_withdrawn - total_pending_withdraw
    )

    in_dispute_count = sum(
        1 for b in bookings if b.payment_status == "in_dispute"
    )

    return {
        "pending_revenue": int(pending_revenue),
        "in_dispute_amount": int(in_dispute_amount),
        "withdrawable_balance": int(withdrawable_balance),
        "total_withdrawn": int(total_withdrawn),
        "in_dispute_count": in_dispute_count,
    }


@payment_bp.route("/")
@login_required
def index():
    host_id = current_user.id
    status_filter = request.args.get("status", "Tất cả")
    page = request.args.get("page", 1, type=int)
    q = request.args.get("q", "").strip()
    acc_id = request.args.get("acc_id", type=int)
    date_from = request.args.get("date_from", "")
    date_to = request.args.get("date_to", "")
    per_page = 10

    stats = _wallet_stats(host_id)

    query = (
        _host_bookings_query(host_id)
        .options(
            joinedload(Booking.room).joinedload(Room.accommodation)
        )
    )
    if status_filter == "Chờ giải ngân":
        query = query.filter(Booking.payment_status == "pending")
    elif status_filter == "Đang tranh chấp":
        query = query.filter(Booking.payment_status == "in_dispute")
    elif status_filter == "Đã giải ngân":
        query = query.filter(Booking.payment_status == "disbursed")
    elif status_filter == "Đã giải quyết":
        query = query.filter(Booking.payment_status == "resolved")

    if q:
        like = f"%{q}%"
        query = query.filter(
            or_(
                Booking.booking_code.ilike(like),
                Booking.guest_name.ilike(like),
            )
        )
    if acc_id:
        query = query.filter(Accommodation.id == acc_id)
    if date_from:
        try:
            query = query.filter(Booking.created_at >= datetime.strptime(date_from, "%Y-%m-%d"))
        except ValueError:
            pass
    if date_to:
        try:
            end = datetime.strptime(date_to, "%Y-%m-%d").replace(hour=23, minute=59, second=59)
            query = query.filter(Booking.created_at <= end)
        except ValueError:
            pass

    pagination = query.order_by(Booking.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    total_all = _host_bookings_query(host_id).count()

    withdrawals = (
        Withdrawal.query.filter_by(host_id=host_id, status=Withdrawal.STATUS_COMPLETED)
        .order_by(Withdrawal.completed_at.desc(), Withdrawal.created_at.desc())
        .all()
    )

    accommodations = Accommodation.query.filter_by(host_id=host_id).order_by(
        Accommodation.name
    ).all()

    return render_template(
        "host/payment/index.html",
        active_nav="payments",
        active_tab=status_filter,
        pagination=pagination,
        total_all_bookings=total_all,
        filter_q=q,
        selected_acc_id=acc_id,
        date_from=date_from,
        date_to=date_to,
        withdrawals=withdrawals,
        timedelta=timedelta,
        accommodations=accommodations,
        **stats,
    )


@payment_bp.route("/withdraw", methods=["POST"])
@login_required
def withdraw():
    host_id = current_user.id
    amount_str = request.form.get("amount", "")

    try:
        amount = int(amount_str.replace(".", "").replace(",", "").strip())
    except (ValueError, AttributeError):
        flash("Số tiền không hợp lệ", "danger")
        return redirect(url_for("payment.index"))

    if amount <= 0:
        flash("Số tiền rút phải lớn hơn 0", "danger")
        return redirect(url_for("payment.index"))

    stats = _wallet_stats(host_id)
    if amount > stats["withdrawable_balance"]:
        flash("Số tiền vượt quá số dư có thể rút", "danger")
        return redirect(url_for("payment.index"))

    withdrawal = Withdrawal(
        host_id=host_id,
        amount=amount,
        bank_account="Vietcombank xxxx 1234",
        status=Withdrawal.STATUS_COMPLETED,
    )
    db.session.add(withdrawal)
    db.session.commit()

    flash(f"Đã rút thành công {amount:,.0f} đ", "success")
    return redirect(url_for("payment.index"))
