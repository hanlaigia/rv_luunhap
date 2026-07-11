"""Nhãn và hằng số phân quyền quản trị viên."""

ADMIN_ROLE_LABELS = {
    "super": "Quản trị cấp cao",
    "admin": "Quản trị viên",
    "support": "Hỗ trợ viên",
}

ADMIN_ROLE_CHOICES = ("super", "admin", "support")

ADMIN_STATUS_LABELS = {
    "active": "Hoạt động",
    "revoked": "Thu hồi quyền",
}


def admin_role_label(role):
    return ADMIN_ROLE_LABELS.get(role or "admin", "Quản trị viên")


def admin_status_label(is_locked):
    return ADMIN_STATUS_LABELS["revoked"] if is_locked else ADMIN_STATUS_LABELS["active"]


def admin_status_from_locked(is_locked):
    return "revoked" if is_locked else "active"
