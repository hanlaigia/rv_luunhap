"""Dữ liệu hội thoại khách — cơ sở lưu trú."""
from sqlalchemy import or_

from backend.app.extensions import db
from backend.app.models import Accommodation, Booking, Conversation, Message


def _guest_filter(user):
    return or_(
        Conversation.guest_id == user.id,
        Conversation.guest_email == user.email,
    )


def guest_conversations(user):
    return (
        Conversation.query.filter(_guest_filter(user))
        .order_by(Conversation.updated_at.desc())
        .all()
    )


def conversation_for_guest(conversation_id, user):
    return Conversation.query.filter(
        Conversation.id == conversation_id,
        _guest_filter(user),
    ).first()


def conversation_accommodation(conversation):
    booking = conversation_booking(conversation)
    if booking and booking.room and booking.room.accommodation:
        return booking.room.accommodation
    return Accommodation.query.filter_by(host_id=conversation.host_id).first()


def conversation_booking(conversation):
    if conversation.guest_id:
        booking = (
            Booking.query.filter_by(guest_id=conversation.guest_id)
            .order_by(Booking.created_at.desc())
            .first()
        )
        if booking:
            return booking
    return (
        Booking.query.filter_by(guest_email=conversation.guest_email)
        .order_by(Booking.created_at.desc())
        .first()
    )


def mark_host_messages_read(conversation):
    for msg in conversation.messages.filter_by(sender_type="host", is_read=False):
        msg.is_read = True


def conversation_messages(conversation):
    return conversation.messages.order_by(Message.created_at.asc()).all()


def conversation_for_host(user, host_id):
    return (
        Conversation.query.filter(
            _guest_filter(user),
            Conversation.host_id == host_id,
        )
        .order_by(Conversation.updated_at.desc())
        .first()
    )


def get_or_create_host_conversation(user, accommodation):
    """Tìm hoặc tạo hội thoại giữa khách và chủ cơ sở lưu trú."""
    conv = conversation_for_host(user, accommodation.host_id)
    if conv:
        if not conv.guest_id:
            conv.guest_id = user.id
            conv.guest_email = user.email
            conv.guest_name = user.full_name
            if user.phone:
                conv.guest_phone = user.phone
        db.session.commit()
        return conv

    conv = Conversation(
        host_id=accommodation.host_id,
        guest_id=user.id,
        guest_name=user.full_name,
        guest_email=user.email,
        guest_phone=user.phone or "",
    )
    db.session.add(conv)
    db.session.commit()
    return conv
