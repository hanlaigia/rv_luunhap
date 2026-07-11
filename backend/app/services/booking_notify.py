"""Giả lập gửi email xác nhận đặt phòng."""

from __future__ import annotations

import logging

from flask import url_for

logger = logging.getLogger(__name__)


def send_booking_confirmation_email(booking) -> dict:
    """
    Mô phỏng gửi email xác nhận. Trong production thay bằng SMTP/SendGrid.
    Trả về metadata để hiển thị trên UI.
    """
    room = booking.room
    acc = room.accommodation if room else None
    detail_path = f"/customer/booking/order/{booking.booking_code.lstrip('#')}"

    payload = {
        "to": booking.guest_email or "(chưa có email)",
        "subject": f"Xác nhận đặt phòng {booking.booking_code} — Rovva",
        "booking_code": booking.booking_code,
        "detail_url": detail_path,
        "acc_name": acc.name if acc else "Chỗ nghỉ Rovva",
    }

    logger.info(
        "[MOCK EMAIL] To=%s | Subject=%s | Link=%s",
        payload["to"],
        payload["subject"],
        payload["detail_url"],
    )
    return payload
