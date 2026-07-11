"""Hiển thị trạng thái booking và badge cho Host portal."""

from __future__ import annotations

from datetime import date

BOOKING_STATUS_META = {
    "confirmed": {
        "label": "Đã đặt phòng",
        "bg": "#DBE1FF",
        "color": "#003DA8",
        "css": "status-confirmed",
    },
    "staying": {
        "label": "Đang lưu trú",
        "bg": "#DCFCE7",
        "color": "#15803D",
        "css": "status-staying",
    },
    "cancelled": {
        "label": "Đã hủy",
        "bg": "#FFDAD6",
        "color": "#93000A",
        "css": "status-cancelled",
    },
    "completed": {
        "label": "Hoàn thành",
        "bg": "#EADDFF",
        "color": "#6750A4",
        "css": "status-completed",
    },
}


def resolve_booking_display_status(booking) -> str:
    """Map DB status + ngày lưu trú → mã hiển thị."""
    raw = (booking.status or "").strip().lower()
    today = date.today()

    if raw in ("cancelled", "đã hủy"):
        return "cancelled"
    if raw in ("completed", "hoàn thành"):
        return "completed"
    if raw in ("đang lưu trú", "staying"):
        return "staying"

    if booking.check_in and booking.check_out:
        if booking.check_in <= today < booking.check_out and raw not in ("cancelled", "completed"):
            return "staying"

    if raw in ("confirmed", "holding", "pending", "đã đặt phòng"):
        return "confirmed"

    return "confirmed"


def booking_status_meta(booking) -> dict:
    key = resolve_booking_display_status(booking)
    return BOOKING_STATUS_META.get(key, BOOKING_STATUS_META["confirmed"])


def booking_status_label(booking) -> str:
    return booking_status_meta(booking)["label"]


def booking_status_badge_class(booking) -> str:
    return f"badge-status {booking_status_meta(booking)['css']}"


def mask_id_card(value: str | None) -> str:
    if not value:
        return "—"
    digits = "".join(c for c in value.strip() if c.isdigit())
    if not digits:
        return "—"
    if len(digits) <= 4:
        return "•" * len(digits)
    return "•" * (len(digits) - 4) + digits[-4:]


def filter_bookings_by_tab(bookings, tab: str):
    if tab == "Tất cả":
        return bookings
    return [b for b in bookings if booking_status_label(b) == tab]
