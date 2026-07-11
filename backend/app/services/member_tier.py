"""Hạng thành viên — tính theo tổng chi tiêu đơn hoàn thành trong 365 ngày."""
from datetime import date, timedelta

from sqlalchemy import func, or_

from backend.app.extensions import db
from backend.app.models import Booking

TIER_LEVELS = [
    {
        "key": "member",
        "label": "Thành viên",
        "cls": "",
        "threshold": 0,
    },
    {
        "key": "silver",
        "label": "Hạng Bạc",
        "cls": "account-sidebar__tier--silver",
        "threshold": 3_000_000,
    },
    {
        "key": "gold",
        "label": "Hạng Vàng",
        "cls": "account-sidebar__tier--gold",
        "threshold": 10_000_000,
    },
    {
        "key": "platinum",
        "label": "Hạng Bạch Kim",
        "cls": "account-sidebar__tier--platinum",
        "threshold": 25_000_000,
    },
    {
        "key": "diamond",
        "label": "Hạng Kim Cương",
        "cls": "account-sidebar__tier--diamond",
        "threshold": 50_000_000,
    },
]

TIER_BENEFITS = {
    "member": [
        "Tích lũy 1% giá trị đơn đặt phòng thành công.",
        "Thanh toán bằng xu tối đa 10% hóa đơn.",
        "Thưởng 5 xu cho mỗi đánh giá nơi lưu trú.",
    ],
    "silver": [
        "Tích lũy 1% giá trị đơn đặt phòng thành công.",
        "Thanh toán bằng xu tối đa 12% hóa đơn.",
        "Ưu tiên hỗ trợ khách hàng và xử lý yêu cầu nhanh hơn.",
        "Nhận ưu đãi và mã giảm giá độc quyền cho thành viên.",
        "Thưởng 5 xu cho mỗi đánh giá nơi lưu trú.",
    ],
    "gold": [
        "Tích lũy 1,2% giá trị đơn đặt phòng thành công.",
        "Thanh toán bằng xu tối đa 15% hóa đơn.",
        "Nhân đôi xu thưởng cho đơn đặt phòng vào tháng sinh nhật.",
        "Nhận ưu đãi và mã giảm giá độc quyền cho thành viên.",
        "Thưởng 5 xu cho mỗi đánh giá nơi lưu trú.",
    ],
    "platinum": [
        "Tích lũy 1,5% giá trị đơn đặt phòng thành công.",
        "Thanh toán bằng xu tối đa 17% hóa đơn.",
        "Nhân ba xu thưởng cho đơn đặt phòng vào tháng sinh nhật.",
        "Ưu tiên hỗ trợ khách hàng và xử lý yêu cầu nhanh hơn.",
        "Thưởng 10 xu cho mỗi đánh giá nơi lưu trú.",
    ],
    "diamond": [
        "Tích lũy 2,5% giá trị đơn đặt phòng thành công.",
        "Thanh toán bằng xu tối đa 20% hóa đơn.",
        "Giảm 20% phí dịch vụ phát sinh.",
        "Tặng 01 đêm phòng miễn phí/năm (tối đa 2.000.000đ).",
        "Thưởng 10 xu cho mỗi đánh giá nơi lưu trú.",
    ],
}


def format_vnd(amount):
    return f"{int(amount):,}".replace(",", ".") + "đ"


def guest_total_spending(user, days=365):
    """Tổng chi tiêu từ đơn đã hoàn thành trong `days` ngày gần nhất."""
    if not getattr(user, "is_authenticated", False):
        return 0

    since = date.today() - timedelta(days=days)
    total = (
        db.session.query(func.coalesce(func.sum(Booking.total_amount), 0))
        .filter(
            Booking.status == Booking.STATUS_COMPLETED,
            Booking.check_out >= since,
            or_(Booking.guest_id == user.id, Booking.guest_email == user.email),
        )
        .scalar()
    )
    return int(total or 0)


def resolve_tier(spent):
    for idx in range(len(TIER_LEVELS) - 1, -1, -1):
        tier = TIER_LEVELS[idx]
        if spent >= tier["threshold"]:
            return {**tier, "index": idx}
    return {**TIER_LEVELS[0], "index": 0}


def member_tier_info(user):
    if not getattr(user, "is_authenticated", False):
        return {"label": "Khách", "cls": "account-sidebar__tier--silver", "key": "member"}

    current = resolve_tier(guest_total_spending(user))
    return {"label": current["label"], "cls": current["cls"], "key": current["key"]}


def member_tier_progress(user):
    spent = guest_total_spending(user)
    current = resolve_tier(spent)
    idx = current["index"]
    next_tier = TIER_LEVELS[idx + 1] if idx + 1 < len(TIER_LEVELS) else None
    year = date.today().year

    if next_tier:
        remain = max(0, next_tier["threshold"] - spent)
        span = next_tier["threshold"] - current["threshold"]
        if span > 0:
            progress = min(100, max(0, round((spent - current["threshold"]) / span * 100)))
        else:
            progress = 100
        next_title = f"Tiến trình lên {next_tier['label']}"
        target_label = f"{next_tier['label']} ({format_vnd(next_tier['threshold'])})"
        hint = (
            f"Bạn chỉ cần chi tiêu thêm {format_vnd(remain)} trước ngày 31/12/{year} "
            f"để thăng {next_tier['label']} và nhận các đặc quyền cao hơn."
        )
    else:
        remain = 0
        progress = 100
        next_title = "Bạn đã đạt hạng cao nhất"
        target_label = f"{current['label']} ({format_vnd(current['threshold'])})"
        hint = (
            "Chúc mừng! Bạn đang ở hạng cao nhất. Hãy duy trì chi tiêu trong chu kỳ 12 tháng "
            "để giữ nguyên đặc quyền thành viên."
        )

    return {
        "spent": spent,
        "spent_display": format_vnd(spent),
        "remain": remain,
        "remain_display": format_vnd(remain),
        "progress_percent": progress,
        "next_title": next_title,
        "target_label": target_label,
        "hint": hint,
        "benefits": TIER_BENEFITS.get(current["key"], TIER_BENEFITS["member"]),
        "deadline": f"31/12/{year}",
    }
