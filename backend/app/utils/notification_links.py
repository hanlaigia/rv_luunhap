"""Liên kết hành động cho thông báo Host."""

from __future__ import annotations

from flask import url_for


def notification_action_url(notification) -> str | None:
    if notification.link_url:
        return notification.link_url
    cat = notification.category
    if cat == "booking":
        return url_for("booking.index")
    if cat == "payment":
        return url_for("payment.index")
    if cat == "dispute":
        return url_for("dispute.index")
    return None


def notification_action_label(notification) -> str:
    labels = {
        "booking": "Xem chi tiết",
        "payment": "Xem thanh toán",
        "dispute": "Xem tranh chấp",
        "system": "Xem thêm",
    }
    return labels.get(notification.category, "Xem chi tiết")
