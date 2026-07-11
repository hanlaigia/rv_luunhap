from datetime import date

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from backend.app.extensions import db
from backend.app.models import Accommodation, Booking, Conversation, Dispute, Message, Room, User
from backend.app.services.host_dashboard import get_host_stats
from backend.app.utils.host_display import filter_bookings_by_tab

message_bp = Blueprint("message", __name__, url_prefix="/messages")


@message_bp.route("/")
@login_required
def index():
    host_id = current_user.id
    conversations = (
        Conversation.query.filter_by(host_id=host_id)
        .order_by(Conversation.updated_at.desc())
        .all()
    )

    active_conversation = None
    bookings = []
    conversation_id = request.args.get("conversation_id", type=int)

    if not conversation_id and conversations:
        conversation_id = conversations[0].id

    if conversation_id:
        active_conversation = Conversation.query.filter_by(
            id=conversation_id, host_id=host_id
        ).first_or_404()
        if not active_conversation.guest_id:
            guest_user = User.query.filter_by(email=active_conversation.guest_email).first()
            if guest_user:
                active_conversation.guest_id = guest_user.id
        unread_msgs = active_conversation.messages.filter_by(
            sender_type="guest", is_read=False
        ).all()
        for msg in unread_msgs:
            msg.is_read = True
        db.session.commit()

        bookings = (
            Booking.query.join(Room)
            .join(Accommodation)
            .filter(
                Accommodation.host_id == host_id,
                Booking.guest_email == active_conversation.guest_email,
            )
            .order_by(Booking.created_at.desc())
            .all()
        )

    return render_template(
        "host/message/index.html",
        active_nav="messages",
        conversations=conversations,
        active_conversation=active_conversation,
        bookings=bookings,
    )


@message_bp.route("/<int:conversation_id>/send", methods=["POST"])
@login_required
def send_message(conversation_id):
    conversation = Conversation.query.filter_by(
        id=conversation_id, host_id=current_user.id
    ).first_or_404()
    content = request.form.get("content")
    if content and content.strip():
        from datetime import datetime

        msg = Message(
            conversation_id=conversation.id,
            sender_type="host",
            content=content.strip(),
        )
        db.session.add(msg)
        conversation.updated_at = datetime.utcnow()
        db.session.commit()
    return redirect(url_for("message.index", conversation_id=conversation.id))


@message_bp.route("/report", methods=["POST"])
@login_required
def report():
    report_type = request.form.get("type", "Báo cáo")
    title = request.form.get("title")
    content = request.form.get("content")
    if title and content:
        flash(f"Đã gửi {report_type} thành công! Quản trị viên sẽ sớm xem xét.", "success")
    else:
        flash("Vui lòng điền đầy đủ thông tin.", "danger")
    conversation_id = request.form.get("conversation_id")
    if conversation_id:
        return redirect(url_for("message.index", conversation_id=conversation_id))
    return redirect(url_for("message.index"))
