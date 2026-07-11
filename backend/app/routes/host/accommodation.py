from datetime import date, datetime as dt
import json

from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from backend.app.extensions import db
from backend.app.models import Accommodation, Booking, Room
from backend.app.models.review import Review
from backend.app.utils.media import (
    accommodation_has_images,
    room_has_images,
    save_accommodation_images,
    save_room_images,
)

accommodation_bp = Blueprint("accommodation", __name__, url_prefix="/accommodations")


def _host_accommodations_query():
    return Accommodation.query.filter_by(host_id=current_user.id)


def _host_accommodation_or_404(acc_id):
    return _host_accommodations_query().filter_by(id=acc_id).first_or_404()


def _acc_counts():
    base = _host_accommodations_query()
    return {
        "all": base.filter(Accommodation.status != Accommodation.STATUS_PENDING).count(),
        "active": base.filter_by(status=Accommodation.STATUS_ACTIVE).count(),
        "paused": base.filter_by(status=Accommodation.STATUS_PAUSED).count(),
        "draft": base.filter_by(status=Accommodation.STATUS_DRAFT).count(),
    }


def _staying_count(acc, room_id=None):
    q = Booking.query.join(Room).filter(
        Room.accommodation_id == acc.id,
        Booking.status.in_([Booking.STATUS_CONFIRMED, "confirmed"]),
        Booking.check_in <= date.today(),
        Booking.check_out > date.today(),
    )
    if room_id:
        q = q.filter(Room.id == room_id)
    return q.count()


def _room_staying_count(room):
    return _staying_count(room.accommodation, room_id=room.id)


def _collect_room_image_files():
    files = []
    order_raw = request.form.get("image_order", "")
    indexed = {}
    for key in request.files.keys():
        if key.startswith("room_image_"):
            idx = int(key.replace("room_image_", ""))
            f = request.files[key]
            if f and f.filename:
                indexed[idx] = f
    if order_raw:
        try:
            order = json.loads(order_raw)
            files = [indexed[i] for i in order if i in indexed]
        except (json.JSONDecodeError, ValueError, KeyError):
            pass
    if not files:
        files = [f for f in request.files.getlist("room_images") if f and f.filename]
    return files[:5]


def _collect_room_services(form):
    names = form.getlist("service_name")
    prices = form.getlist("service_price")
    notes = form.getlist("service_note")
    services = []
    for i, name in enumerate(names):
        name = (name or "").strip()
        if not name:
            continue
        services.append(
            {
                "name": name,
                "price": (prices[i] if i < len(prices) else "").strip(),
                "note": (notes[i] if i < len(notes) else "").strip(),
            }
        )
    return services


def _collect_room_features(form):
    features = form.getlist("features")
    for custom in form.getlist("custom_feature_name"):
        custom = (custom or "").strip()
        if custom:
            features.append(custom)
    return features


def _room_stats(room):
    today = date.today()
    month_start = today.replace(day=1)
    completed = room.bookings.filter(
        Booking.status.in_([Booking.STATUS_COMPLETED, "completed"])
    ).count()
    month_bookings = room.bookings.filter(
        Booking.check_in >= month_start,
        Booking.check_in <= today,
        Booking.status.in_([Booking.STATUS_CONFIRMED, Booking.STATUS_COMPLETED, "confirmed", "completed"]),
    ).count()
    upcoming = room.bookings.filter(
        Booking.status.in_([Booking.STATUS_CONFIRMED, "confirmed"]),
        Booking.check_in > today,
    ).count()
    occupancy = min(100, month_bookings * 10) if month_bookings else 0
    return {
        "completed_bookings": completed,
        "upcoming_bookings": upcoming,
        "occupancy_percent": occupancy,
    }


def _collect_features(form):
    features = form.getlist("features")
    for custom in form.getlist("custom_feature_name"):
        custom = (custom or "").strip()
        if custom:
            features.append(custom)
    return features


def _collect_image_files():
    files = []
    for key in sorted(request.files.keys()):
        if key.startswith("acc_image_"):
            f = request.files[key]
            if f and f.filename:
                files.append(f)
    order_raw = request.form.get("image_order", "")
    if order_raw:
        try:
            order = json.loads(order_raw)
            indexed = {}
            for key in request.files.keys():
                if key.startswith("acc_image_"):
                    idx = int(key.replace("acc_image_", ""))
                    f = request.files[key]
                    if f and f.filename:
                        indexed[idx] = f
            files = [indexed[i] for i in order if i in indexed]
        except (json.JSONDecodeError, ValueError, KeyError):
            pass
    if not files:
        multi = request.files.getlist("acc_images")
        files = [f for f in multi if f and f.filename]
    return files[:5]


def _apply_form_fields(acc, form):
    acc.name = form.get("name")
    acc.type = form.get("type")
    acc.city = form.get("city")
    acc.district = form.get("district")
    acc.address = form.get("address")
    acc.description = form.get("description")
    acc.features = _collect_features(form)
    acc.check_in_time = form.get("check_in_time", "14:00")
    acc.check_out_time = form.get("check_out_time", "12:00")
    acc.cancellation_policy = form.get("cancellation_policy")
    acc.house_rules = form.get("house_rules")


@accommodation_bp.route("/")
@login_required
def index():
    accommodations = (
        _host_accommodations_query()
        .filter(Accommodation.status != Accommodation.STATUS_PENDING)
        .order_by(Accommodation.id.desc())
        .all()
    )
    return render_template(
        "host/accommodation/index.html",
        active_nav="accommodations",
        accommodations=accommodations,
        current_status=request.args.get("status", "all"),
        counts=_acc_counts(),
    )


@accommodation_bp.route("/<int:id>")
@login_required
def detail(id):
    acc = _host_accommodation_or_404(id)
    all_rooms = acc.rooms.order_by(Room.id).all()
    counts = {
        "all": len(all_rooms),
        "active": sum(1 for r in all_rooms if r.status == Room.STATUS_ACTIVE),
        "paused": sum(1 for r in all_rooms if r.status == Room.STATUS_PAUSED),
        "draft": sum(1 for r in all_rooms if r.status == Room.STATUS_DRAFT),
    }
    return render_template(
        "host/accommodation/detail.html",
        active_nav="accommodations",
        acc=acc,
        rooms=all_rooms,
        current_status=request.args.get("status", "all"),
        counts=counts,
        staying_count=_staying_count(acc),
    )


@accommodation_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        image_files = _collect_image_files()
        if not image_files:
            flash("CSLT bắt buộc có ít nhất 1 ảnh trước khi lưu.", "danger")
            return redirect(url_for("accommodation.create"))

        acc = Accommodation(
            host_id=current_user.id,
            name=request.form.get("name"),
            type=request.form.get("type"),
            city=request.form.get("city"),
            district=request.form.get("district"),
            address=request.form.get("address"),
            description=request.form.get("description"),
            features=_collect_features(request.form),
            check_in_time=request.form.get("check_in_time", "14:00"),
            check_out_time=request.form.get("check_out_time", "12:00"),
            cancellation_policy=request.form.get("cancellation_policy"),
            house_rules=request.form.get("house_rules"),
            status=Accommodation.STATUS_DRAFT,
            image=f"customer/images/accommodations/0/cover.jpg",
        )
        db.session.add(acc)
        db.session.flush()
        save_accommodation_images(acc.id, image_files)
        acc.image = f"customer/images/accommodations/{acc.id}/cover.jpg"
        db.session.commit()
        flash("Thông tin của bạn đã được lưu.", "acc_saved")
        return redirect(url_for("accommodation.edit", id=acc.id))
    return render_template("host/accommodation/form.html", active_nav="accommodations", acc=None, staying_count=0)


@accommodation_bp.route("/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit(id):
    acc = _host_accommodation_or_404(id)
    staying_count = _staying_count(acc)
    if request.method == "POST":
        image_files = _collect_image_files()
        has_images = accommodation_has_images(acc.id) or bool(image_files)
        if not has_images:
            flash("CSLT bắt buộc có ít nhất 1 ảnh trước khi lưu.", "danger")
            return redirect(url_for("accommodation.edit", id=acc.id))

        _apply_form_fields(acc, request.form)
        if image_files:
            save_accommodation_images(acc.id, image_files)
            acc.image = f"customer/images/accommodations/{acc.id}/cover.jpg"
        db.session.commit()
        flash("Thông tin của bạn đã được lưu.", "acc_saved")
        return redirect(url_for("accommodation.edit", id=acc.id))
    return render_template(
        "host/accommodation/form.html",
        active_nav="accommodations",
        acc=acc,
        staying_count=staying_count,
    )


@accommodation_bp.route("/<int:id>/delete", methods=["POST"])
@login_required
def delete(id):
    acc = _host_accommodation_or_404(id)
    staying = _staying_count(acc)
    if staying:
        flash(f"Đang có {staying} booking đang lưu trú, không thể xóa.", "danger")
        return redirect(url_for("accommodation.edit", id=id))
    db.session.delete(acc)
    db.session.commit()
    flash("Cơ sở lưu trú đã được xóa.", "success")
    return redirect(url_for("accommodation.index"))


@accommodation_bp.route("/<int:id>/pause", methods=["POST"])
@login_required
def pause(id):
    acc = _host_accommodation_or_404(id)
    staying = _staying_count(acc)
    if staying:
        flash(f"Đang có {staying} booking đang lưu trú, không thể tạm ngưng.", "danger")
        return redirect(request.referrer or url_for("accommodation.detail", id=id))
    if acc.status == Accommodation.STATUS_ACTIVE:
        acc.status = Accommodation.STATUS_PAUSED
    elif acc.status == Accommodation.STATUS_PAUSED:
        acc.status = Accommodation.STATUS_ACTIVE
    db.session.commit()
    flash("Đã cập nhật trạng thái cơ sở lưu trú.", "success")
    return redirect(request.referrer or url_for("accommodation.detail", id=id))


@accommodation_bp.route("/<int:acc_id>/rooms/<int:room_id>")
@login_required
def room_detail(acc_id, room_id):
    acc = _host_accommodation_or_404(acc_id)
    room = Room.query.filter_by(id=room_id, accommodation_id=acc.id).first_or_404()
    reviews = Review.query.filter_by(room_id=room.id).order_by(Review.created_at.desc()).all()
    stats = _room_stats(room)
    rating_dist = {i: 0 for i in range(1, 6)}
    for r in reviews:
        rating_dist[r.rating] = rating_dist.get(r.rating, 0) + 1
    total_reviews = len(reviews) or 1
    rating_pct = {k: round(v / total_reviews * 100) for k, v in rating_dist.items()}
    return render_template(
        "host/room/detail.html",
        active_nav="accommodations",
        acc=acc,
        room=room,
        reviews=reviews,
        room_stats=stats,
        rating_pct=rating_pct,
        staying_count=_room_staying_count(room),
    )


@accommodation_bp.route("/<int:acc_id>/rooms/create", methods=["GET", "POST"])
@login_required
def room_create(acc_id):
    acc = _host_accommodation_or_404(acc_id)
    if request.method == "POST":
        image_files = _collect_room_image_files()
        if not image_files:
            flash("Phòng bắt buộc có ít nhất 1 ảnh trước khi lưu.", "danger")
            return redirect(url_for("accommodation.room_create", acc_id=acc.id))
        room = Room(
            accommodation_id=acc.id,
            name=request.form.get("name"),
            bed_info=request.form.get("bed_info", "1 Giường đôi"),
            capacity=int(request.form.get("capacity", 2) or 2),
            area=request.form.get("area", "30m2"),
            base_price=int(request.form.get("base_price", 0) or 0),
            description=request.form.get("description"),
            features=_collect_room_features(request.form),
            services=_collect_room_services(request.form),
            check_in_time=request.form.get("check_in_time", "14:00"),
            check_out_time=request.form.get("check_out_time", "12:00"),
            cancellation_policy=request.form.get(
                "cancellation_policy", "Linh hoạt: Hoàn tiền 100% trước 24h"
            ),
            status=Room.STATUS_ACTIVE,
            image=f"customer/images/accommodations/{acc.id}/rooms/0/cover.jpg",
        )
        db.session.add(room)
        db.session.flush()
        save_room_images(acc.id, room.id, image_files)
        room.image = f"customer/images/accommodations/{acc.id}/rooms/{room.id}/cover.jpg"
        db.session.commit()
        flash("Thông tin phòng đã được lưu.", "success")
        return redirect(url_for("accommodation.room_detail", acc_id=acc.id, room_id=room.id))
    return render_template(
        "host/room/form.html", active_nav="accommodations", acc=acc, room=None, staying_count=0
    )


@accommodation_bp.route("/<int:acc_id>/rooms/<int:room_id>/edit", methods=["GET", "POST"])
@login_required
def room_edit(acc_id, room_id):
    acc = _host_accommodation_or_404(acc_id)
    room = Room.query.filter_by(id=room_id, accommodation_id=acc.id).first_or_404()
    staying_count = _room_staying_count(room)
    if request.method == "POST":
        image_files = _collect_room_image_files()
        has_images = room_has_images(acc.id, room.id) or bool(image_files)
        if not has_images:
            flash("Phòng bắt buộc có ít nhất 1 ảnh trước khi lưu.", "danger")
            return redirect(url_for("accommodation.room_edit", acc_id=acc.id, room_id=room.id))
        room.name = request.form.get("name")
        room.bed_info = request.form.get("bed_info", "1 Giường đôi")
        room.capacity = int(request.form.get("capacity", 2) or 2)
        room.area = request.form.get("area", "30m2")
        room.base_price = int(request.form.get("base_price", 0) or 0)
        room.description = request.form.get("description")
        room.features = _collect_room_features(request.form)
        room.services = _collect_room_services(request.form)
        room.check_in_time = request.form.get("check_in_time", "14:00")
        room.check_out_time = request.form.get("check_out_time", "12:00")
        room.cancellation_policy = request.form.get(
            "cancellation_policy", "Linh hoạt: Hoàn tiền 100% trước 24h"
        )
        if image_files:
            save_room_images(acc.id, room.id, image_files)
            room.image = f"customer/images/accommodations/{acc.id}/rooms/{room.id}/cover.jpg"
        db.session.commit()
        flash("Thông tin phòng đã được lưu.", "success")
        return redirect(url_for("accommodation.room_edit", acc_id=acc.id, room_id=room.id))
    return render_template(
        "host/room/form.html",
        active_nav="accommodations",
        acc=acc,
        room=room,
        staying_count=staying_count,
        room_stats=_room_stats(room),
    )


@accommodation_bp.route("/<int:acc_id>/rooms/<int:room_id>/pricing")
@login_required
def room_pricing(acc_id, room_id):
    acc = _host_accommodation_or_404(acc_id)
    room = Room.query.filter_by(id=room_id, accommodation_id=acc.id).first_or_404()
    price_history = [
        {"changed": "14/12/2024", "applied": "25/12/2024", "old": "1.200.000đ", "new": "1.800.000đ", "type": "Giáng sinh"},
        {"changed": "10/12/2024", "applied": "27/12/2024", "old": "1.200.000đ", "new": "1.500.000đ", "type": "Cuối tuần"},
    ]
    price_ranges = [
        {"from": "25/12/2024", "to": "25/12/2024", "price": "1.800.000đ", "type": "Giáng sinh"},
        {"from": "27/12/2024", "to": "27/12/2024", "price": "1.500.000đ", "type": "Cuối tuần"},
    ]
    return render_template(
        "host/room/pricing.html",
        active_nav="accommodations",
        acc=acc,
        room=room,
        price_history=price_history,
        price_ranges=price_ranges,
    )


@accommodation_bp.route("/<int:acc_id>/rooms/<int:room_id>/price-suggestions")
@login_required
def room_price_suggestions(acc_id, room_id):
    from backend.app.services.host_dashboard import get_revenue_chart

    acc = _host_accommodation_or_404(acc_id)
    room = Room.query.filter_by(id=room_id, accommodation_id=acc.id).first_or_404()
    pricing_rules = [
        {
            "id": 1,
            "name": "Cuối tuần",
            "condition": "Thứ 6, Thứ 7 & Chủ Nhật",
            "adjust": "+20%",
            "adjust_type": "percent_up",
            "adjust_value": "20",
            "active": True,
            "note": "Tăng giá cuối tuần khi nhu cầu cao.",
        },
        {
            "id": 2,
            "name": "Đặt muộn",
            "condition": "Trong vòng 24h trước check-in",
            "adjust": "-15%",
            "adjust_type": "percent_down",
            "adjust_value": "15",
            "active": True,
            "note": "Giảm giá để lấp đầy phòng trống phút chót.",
        },
    ]
    chart = get_revenue_chart(current_user.id, "30d")
    actual_values = chart["values"]
    predicted_values = [
        int(v * (1.06 + (i % 4) * 0.03)) if v else int(room.base_price * 0.3 * (1 + i * 0.02))
        for i, v in enumerate(actual_values)
    ]
    return render_template(
        "host/room/price_suggestions.html",
        active_nav="accommodations",
        acc=acc,
        room=room,
        pricing_rules=pricing_rules,
        revenue_labels=chart["labels"],
        revenue_actual=actual_values,
        revenue_predicted=predicted_values,
    )


@accommodation_bp.route("/<int:acc_id>/rooms/<int:room_id>/pause", methods=["POST"])
@login_required
def room_pause(acc_id, room_id):
    acc = _host_accommodation_or_404(acc_id)
    room = Room.query.filter_by(id=room_id, accommodation_id=acc.id).first_or_404()
    staying = _room_staying_count(room)
    if staying:
        flash(f"Đang có {staying} booking đang lưu trú, không thể tạm ngưng.", "danger")
        return redirect(request.referrer or url_for("accommodation.room_detail", acc_id=acc.id, room_id=room.id))
    if room.status == Room.STATUS_ACTIVE:
        room.status = Room.STATUS_PAUSED
    elif room.status == Room.STATUS_PAUSED:
        room.status = Room.STATUS_ACTIVE
    db.session.commit()
    flash("Đã cập nhật trạng thái phòng.", "success")
    return redirect(request.referrer or url_for("accommodation.room_detail", acc_id=acc.id, room_id=room.id))


@accommodation_bp.route("/<int:acc_id>/rooms/<int:room_id>/reviews/<int:review_id>/reply", methods=["POST"])
@login_required
def room_review_reply(acc_id, room_id, review_id):
    acc = _host_accommodation_or_404(acc_id)
    room = Room.query.filter_by(id=room_id, accommodation_id=acc.id).first_or_404()
    review = Review.query.filter_by(id=review_id, room_id=room.id).first_or_404()
    reply = (request.form.get("reply") or "").strip()
    if not reply:
        flash("Nội dung phản hồi không được để trống.", "danger")
        return redirect(url_for("accommodation.room_detail", acc_id=acc.id, room_id=room.id) + "#tab-reviews")
    review.reply = reply
    review.reply_at = dt.utcnow()
    db.session.commit()
    flash("Phản hồi đã được gửi.", "success")
    return redirect(url_for("accommodation.room_detail", acc_id=acc.id, room_id=room.id) + "#tab-reviews")


@accommodation_bp.route("/<int:acc_id>/rooms/<int:room_id>/delete", methods=["POST"])
@login_required
def room_delete(acc_id, room_id):
    acc = _host_accommodation_or_404(acc_id)
    room = Room.query.filter_by(id=room_id, accommodation_id=acc.id).first_or_404()
    db.session.delete(room)
    db.session.commit()
    return redirect(url_for("accommodation.detail", id=acc.id))
