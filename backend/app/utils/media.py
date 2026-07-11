"""Trợ giúp phân giải đường dẫn ảnh với cơ chế fallback placeholder.

Quy ước thư mục (đặt trong frontend/static/):
    customer/images/accommodations/<acc_id>/cover.jpg
    customer/images/accommodations/<acc_id>/gallery/1..5.jpg
    customer/images/accommodations/<acc_id>/rooms/<room_id>.jpg
    customer/images/avatars/<user_id>.jpg

Nếu file chưa được "thả" vào thư mục, trả ảnh placeholder tương ứng để
giao diện không bị vỡ. Nhờ vậy có thể bổ sung ảnh demo dần mà không cần sửa code.
"""

import os

from flask import current_app, url_for

PLACEHOLDERS = {
    "accommodation": "customer/images/placeholders/accommodation.svg",
    "room": "customer/images/placeholders/room.svg",
    "avatar": "customer/images/placeholders/avatar.svg",
}


def _static_exists(rel_path):
    static_folder = current_app.static_folder
    if not static_folder or not rel_path:
        return False
    full_path = os.path.join(static_folder, *rel_path.split("/"))
    return os.path.isfile(full_path)


def resolve_media(rel_path, kind="accommodation"):
    """Trả URL tĩnh nếu file tồn tại, ngược lại trả placeholder theo `kind`."""
    if rel_path and _static_exists(rel_path):
        return url_for("static", filename=rel_path)
    placeholder = PLACEHOLDERS.get(kind, PLACEHOLDERS["accommodation"])
    return url_for("static", filename=placeholder)


def accommodation_cover(acc_id):
    return resolve_media(
        f"customer/images/accommodations/{acc_id}/cover.jpg", "accommodation"
    )


def accommodation_gallery(acc_id, count=5):
    return [
        resolve_media(
            f"customer/images/accommodations/{acc_id}/gallery/{i}.jpg", "accommodation"
        )
        for i in range(1, count + 1)
    ]


def accommodation_existing_images(acc_id):
    """Chỉ trả URL ảnh thật đã upload (cover + gallery), không placeholder."""
    urls = []
    cover = f"customer/images/accommodations/{acc_id}/cover.jpg"
    if _static_exists(cover):
        urls.append(url_for("static", filename=cover))
    for i in range(1, 5):
        path = f"customer/images/accommodations/{acc_id}/gallery/{i}.jpg"
        if _static_exists(path):
            urls.append(url_for("static", filename=path))
    return urls


def accommodation_has_images(acc_id):
    return bool(accommodation_existing_images(acc_id))


def save_accommodation_images(acc_id, image_files):
    """Lưu tối đa 5 ảnh: ảnh đầu = cover.jpg, còn lại = gallery/1..4.jpg."""
    static_folder = current_app.static_folder
    if not static_folder:
        return
    base = os.path.join(static_folder, "customer", "images", "accommodations", str(acc_id))
    gallery_dir = os.path.join(base, "gallery")
    os.makedirs(gallery_dir, exist_ok=True)

    cover_path = os.path.join(base, "cover.jpg")
    if os.path.isfile(cover_path):
        os.remove(cover_path)
    for i in range(1, 5):
        p = os.path.join(gallery_dir, f"{i}.jpg")
        if os.path.isfile(p):
            os.remove(p)

    for idx, f in enumerate(image_files[:5]):
        if not f or not getattr(f, "filename", None):
            continue
        dest = cover_path if idx == 0 else os.path.join(gallery_dir, f"{idx}.jpg")
        f.save(dest)


def room_image(acc_id, room_id):
    room_path = f"customer/images/accommodations/{acc_id}/rooms/{room_id}.jpg"
    cover_path = f"customer/images/accommodations/{acc_id}/rooms/{room_id}/cover.jpg"
    if _static_exists(cover_path):
        return url_for("static", filename=cover_path)
    if _static_exists(room_path):
        return url_for("static", filename=room_path)
    acc_cover = f"customer/images/accommodations/{acc_id}/cover.jpg"
    if _static_exists(acc_cover):
        return url_for("static", filename=acc_cover)
    return url_for("static", filename=PLACEHOLDERS["room"])


def room_existing_images(acc_id, room_id):
    urls = []
    base = f"customer/images/accommodations/{acc_id}/rooms/{room_id}"
    cover = f"{base}/cover.jpg"
    legacy = f"customer/images/accommodations/{acc_id}/rooms/{room_id}.jpg"
    if _static_exists(cover):
        urls.append(url_for("static", filename=cover))
    elif _static_exists(legacy):
        urls.append(url_for("static", filename=legacy))
    for i in range(1, 5):
        path = f"{base}/gallery/{i}.jpg"
        if _static_exists(path):
            urls.append(url_for("static", filename=path))
    return urls


def room_has_images(acc_id, room_id):
    return bool(room_existing_images(acc_id, room_id))


def save_room_images(acc_id, room_id, image_files):
    static_folder = current_app.static_folder
    if not static_folder:
        return
    base = os.path.join(
        static_folder, "customer", "images", "accommodations", str(acc_id), "rooms", str(room_id)
    )
    gallery_dir = os.path.join(base, "gallery")
    os.makedirs(gallery_dir, exist_ok=True)
    cover_path = os.path.join(base, "cover.jpg")
    legacy_path = os.path.join(
        static_folder, "customer", "images", "accommodations", str(acc_id), "rooms", f"{room_id}.jpg"
    )
    if os.path.isfile(cover_path):
        os.remove(cover_path)
    if os.path.isfile(legacy_path):
        os.remove(legacy_path)
    for i in range(1, 5):
        p = os.path.join(gallery_dir, f"{i}.jpg")
        if os.path.isfile(p):
            os.remove(p)
    for idx, f in enumerate(image_files[:5]):
        if not f or not getattr(f, "filename", None):
            continue
        dest = cover_path if idx == 0 else os.path.join(gallery_dir, f"{idx}.jpg")
        f.save(dest)


def user_avatar(user_id):
    return resolve_media(f"customer/images/avatars/{user_id}.jpg", "avatar")
