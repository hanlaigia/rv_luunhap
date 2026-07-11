"""Guest insight — chỉ hiện khi có ghi chú hoặc tín hiệu trẻ em."""

from __future__ import annotations

CHILD_KEYWORDS = ("trẻ", "bé", "con nhỏ", "em bé", "baby", "ăn dặm", "nôi", "trẻ em", "trẻ nhỏ")


def _analyze_guest_note(note: str) -> str:
    lower = note.lower()
    if any(k in lower for k in ["check-in sớm", "check in sớm", "đến sớm", "sớm"]):
        return "Khách yêu cầu check-in sớm — liên hệ trước để sắp xếp phòng sẵn sàng."
    if any(k in lower for k in ["chăn", "gối", "giường phụ", "nệm"]):
        return "Khách cần thêm chăn gối/giường phụ — chuẩn bị trước khi khách đến."
    if any(k in lower for k in ["pet", "chó", "mèo", "thú cưng", "cún"]):
        return "Khách đi cùng thú cưng — chuẩn bị thảm lau chân, bát nước và nhắc quy định khu vực."
    if any(k in lower for k in ["xe", "đỗ xe", "bãi đỗ", "ô tô"]):
        return "Khách hỏi về chỗ đỗ xe — gửi hướng dẫn bãi đỗ và vị trí trước giờ đến."
    if any(k in lower for k in ["ăn", "bữa sáng", "nấu", "bếp"]):
        return "Khách quan tâm bữa ăn/bếp — xác nhận dịch vụ ăn sáng hoặc quy định sử dụng bếp."
    return f'Phân tích ghi chú: "{note}" — chủ động liên hệ khách để xác nhận và đáp ứng yêu cầu.'


def build_guest_insight(booking) -> dict | None:
    """Trả về insight hoặc None nếu không có ghi chú / tín hiệu trẻ em."""
    note = (booking.guest_note or "").strip()
    note_lower = note.lower()
    has_children = any(k in note_lower for k in CHILD_KEYWORDS)

    if not note and not has_children:
        return None

    if has_children or any(k in note_lower for k in ("ăn dặm", "nôi", "em bé")):
        return {
            "icon": "bi-people-fill",
            "label": "Gia đình có trẻ nhỏ",
            "suggestion": "Chuẩn bị ghế ăn dặm, bình nước ấm và gối phụ để hỗ trợ gia đình có trẻ nhỏ.",
            "booking_id": booking.id,
            "guest_name": booking.guest_name,
        }

    if note:
        return {
            "icon": "bi-chat-left-heart",
            "label": "Ghi chú từ khách",
            "suggestion": _analyze_guest_note(note),
            "booking_id": booking.id,
            "guest_name": booking.guest_name,
            "note": note,
        }

    return None
