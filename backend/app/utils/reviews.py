_VN_MONTHS = (
    "",
    "Tháng 1",
    "Tháng 2",
    "Tháng 3",
    "Tháng 4",
    "Tháng 5",
    "Tháng 6",
    "Tháng 7",
    "Tháng 8",
    "Tháng 9",
    "Tháng 10",
    "Tháng 11",
    "Tháng 12",
)

_RATING_LABELS = {
    5: "Rất hài lòng",
    4: "Hài lòng",
    3: "Bình thường",
    2: "Không hài lòng",
    1: "Rất không hài lòng",
}

SUB_RATING_LABELS = ("Vị trí", "Dịch vụ", "Sạch sẽ", "Tiện nghi")
SUB_RATING_KEYS = ("location", "service", "cleanliness", "amenities")


def format_stay_range(check_in, check_out):
    month_in = _VN_MONTHS[check_in.month]
    month_out = _VN_MONTHS[check_out.month]
    if check_in.year == check_out.year:
        return f"{check_in.day} {month_in} - {check_out.day} {month_out}, {check_out.year}"
    return (
        f"{check_in.day} {month_in}, {check_in.year} - "
        f"{check_out.day} {month_out}, {check_out.year}"
    )


def format_vnd(amount):
    return f"{amount:,.0f}".replace(",", ".") + "₫"


def rating_label(rating):
    return _RATING_LABELS.get(rating, "Đánh giá")


def format_review_datetime(dt):
    if not dt:
        return ""
    return f"Đã đánh giá vào {dt.strftime('%H:%M')} - {dt.day}/{dt.month}/{dt.year}"
