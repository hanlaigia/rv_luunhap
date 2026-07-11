"""Nhãn và quy tắc hiển thị theo loại hình lưu trú."""

WHOLE_UNIT_TYPES = ["Homestay", "Căn hộ", "Villa", "Cottage"]
ROOM_UNIT_TYPES = ["Khách sạn", "Resort"]
ROOM_GALLERY_PREVIEW_TYPES = ["Homestay", "Villa"]


def books_whole_unit(accommodation_type):
    return accommodation_type in WHOLE_UNIT_TYPES


def shows_room_gallery_detail(accommodation_type):
    """Homestay/Villa: xem chi tiết từng không gian, không chọn phòng để đặt."""
    return accommodation_type in ROOM_GALLERY_PREVIEW_TYPES


def booking_unit_label(accommodation_type):
    labels = {
        "Homestay": "Homestay",
        "Căn hộ": "Căn hộ",
        "Villa": "Villa",
        "Cottage": "Cottage",
        "Khách sạn": "Phòng",
        "Resort": "Phòng",
    }
    return labels.get(accommodation_type, "Phòng")


def book_cta_label(accommodation_type):
    labels = {
        "Homestay": "Đặt homestay ngay",
        "Khách sạn": "Đặt phòng ngay",
        "Resort": "Đặt phòng ngay",
        "Căn hộ": "Đặt căn hộ ngay",
        "Villa": "Đặt villa ngay",
        "Cottage": "Đặt cottage ngay",
    }
    return labels.get(accommodation_type, "Đặt ngay")


def unavailable_label(accommodation_type):
    labels = {
        "Homestay": "Hiện chưa có homestay trống",
        "Khách sạn": "Hiện chưa có phòng trống",
        "Resort": "Hiện chưa có phòng trống",
        "Căn hộ": "Hiện chưa có căn hộ trống",
        "Villa": "Hiện chưa có villa trống",
        "Cottage": "Hiện chưa có cottage trống",
    }
    return labels.get(accommodation_type, "Hiện chưa có chỗ trống")
