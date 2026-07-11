from functools import wraps
import csv
import io

from flask import abort, flash, make_response, redirect, render_template, request, url_for
from flask_login import current_user

from backend.app.extensions import db
from backend.app.models import (
    Accommodation,
    Booking,
    Dispute,
    Promotion,
    Room,
    User,
)
from backend.app.routes.admin import admin_bp
from backend.app.services.admin_portal import build_portal_context, normalize_view
from backend.app.utils.admin_roles import ADMIN_ROLE_CHOICES


def _resolve_admin_role(raw_role):
    role = (raw_role or "admin").strip()
    if role not in ADMIN_ROLE_CHOICES:
        return "admin"
    if role == "super" and not current_user.is_super_admin:
        return "admin"
    return role


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != "admin":
            flash("Bạn không có quyền truy cập trang này.", "error")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)

    return decorated_function


def _redirect_portal(view=None):
    return redirect(url_for("admin.index", view=view or "dashboard"))


@admin_bp.route("/")
@admin_required
def index():
    active_view = normalize_view(request.args.get("view", "dashboard"))
    ctx = build_portal_context(active_view=active_view, current_user_id=current_user.id)
    ctx["current_user"] = current_user
    ctx["can_manage_admin_roles"] = current_user.is_super_admin
    return render_template("admin/portal.html", **ctx)


@admin_bp.route("/customers")
@admin_required
def customers():
    return redirect(url_for("admin.index", view="users"))


@admin_bp.route("/customers/<int:user_id>/toggle-lock", methods=["POST"])
@admin_required
def toggle_customer_lock(user_id):
    user = User.query.get_or_404(user_id)
    if user.role != "guest":
        abort(403)
    user.is_locked = not user.is_locked
    db.session.commit()
    state = "khóa" if user.is_locked else "mở khóa"
    flash(f"Đã {state} tài khoản {user.email}.", "success")
    return redirect(url_for("admin.index", view="users"))


@admin_bp.route("/hosts")
@admin_required
def hosts():
    return redirect(url_for("admin.index", view="hosts"))


@admin_bp.route("/hosts/<int:user_id>/approve", methods=["POST"])
@admin_required
def approve_host(user_id):
    user = User.query.get_or_404(user_id)
    if user.host_status == "pending":
        user.host_status = "approved"
        user.role = "host"
        db.session.commit()
        flash(f"Đã duyệt tài khoản Host: {user.email}", "success")
    return redirect(url_for("admin.index", view="hosts"))


@admin_bp.route("/hosts/<int:user_id>/reject", methods=["POST"])
@admin_required
def reject_host(user_id):
    user = User.query.get_or_404(user_id)
    if user.host_status == "pending":
        user.host_status = "rejected"
        db.session.commit()
        flash(f"Đã từ chối tài khoản Host: {user.email}", "success")
    return redirect(url_for("admin.index", view="hosts"))


@admin_bp.route("/accommodations")
@admin_required
def accommodations():
    return redirect(url_for("admin.index", view="hosts"))


@admin_bp.route("/accommodations/<int:acc_id>/approve", methods=["POST"])
@admin_required
def approve_accommodation(acc_id):
    acc = Accommodation.query.get_or_404(acc_id)
    if acc.status in (Accommodation.STATUS_PENDING, Accommodation.STATUS_REJECTED):
        acc.status = Accommodation.STATUS_ACTIVE
        for room in acc.rooms:
            if room.status == Room.STATUS_PENDING:
                room.status = Room.STATUS_ACTIVE
        db.session.commit()
        flash(f"Đã duyệt chỗ nghỉ: {acc.name}", "success")
    return redirect(url_for("admin.index", view="hosts"))


@admin_bp.route("/accommodations/<int:acc_id>/reject", methods=["POST"])
@admin_required
def reject_accommodation(acc_id):
    acc = Accommodation.query.get_or_404(acc_id)
    if acc.status in (Accommodation.STATUS_PENDING, Accommodation.STATUS_ACTIVE):
        acc.status = Accommodation.STATUS_REJECTED
        db.session.commit()
        flash(f"Đã từ chối chỗ nghỉ: {acc.name}", "success")
    return redirect(url_for("admin.index", view="hosts"))


@admin_bp.route("/rooms/<int:room_id>/update", methods=["POST"])
@admin_required
def update_room(room_id):
    room = Room.query.get_or_404(room_id)
    name = request.form.get("name", "").strip()
    if name:
        room.name = name
    capacity = request.form.get("capacity", type=int)
    if capacity:
        room.capacity = capacity
    base_price = request.form.get("base_price", type=int)
    if base_price is not None:
        room.base_price = base_price
    status = request.form.get("status", "").strip()
    if status in Room.STATUS_LABELS:
        room.status = status
    db.session.commit()
    flash(f"Đã cập nhật phòng: {room.name}", "success")
    return redirect(url_for("admin.index", view="rooms"))


@admin_bp.route("/bookings/<int:booking_id>/status", methods=["POST"])
@admin_required
def update_booking_status(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    status = request.form.get("status", "").strip()
    if status == Booking.STATUS_CONFIRMED and booking.status in (
        Booking.STATUS_PENDING,
        Booking.STATUS_HOLDING,
    ):
        booking.status = Booking.STATUS_CONFIRMED
        flash(f"Đã xác nhận booking {booking.booking_code}.", "success")
    elif status == Booking.STATUS_CANCELLED and booking.status not in (
        Booking.STATUS_CANCELLED,
        Booking.STATUS_COMPLETED,
    ):
        booking.status = Booking.STATUS_CANCELLED
        flash(f"Đã hủy booking {booking.booking_code}.", "success")
    elif status == Booking.STATUS_COMPLETED and booking.status == Booking.STATUS_CONFIRMED:
        booking.status = Booking.STATUS_COMPLETED
        flash(f"Đã hoàn thành booking {booking.booking_code}.", "success")
    db.session.commit()
    return redirect(url_for("admin.index", view="bookings"))


@admin_bp.route("/disputes/<int:dispute_id>/process", methods=["POST"])
@admin_required
def process_dispute(dispute_id):
    dispute = Dispute.query.get_or_404(dispute_id)
    if dispute.status == Dispute.STATUS_NEEDS_RESPONSE:
        dispute.status = Dispute.STATUS_PROCESSING
        db.session.commit()
        flash(f"Tranh chấp {dispute.dispute_code} đang được xem xét.", "success")
    return redirect(url_for("admin.index", view="disputes"))


@admin_bp.route("/rooms")
@admin_required
def rooms():
    return redirect(url_for("admin.index", view="rooms"))


@admin_bp.route("/bookings")
@admin_required
def bookings():
    return redirect(url_for("admin.index", view="bookings"))


@admin_bp.route("/disputes")
@admin_required
def disputes():
    return redirect(url_for("admin.index", view="disputes"))


@admin_bp.route("/disputes/<int:dispute_id>/resolve", methods=["POST"])
@admin_required
def resolve_dispute(dispute_id):
    dispute = Dispute.query.get_or_404(dispute_id)
    resolution = request.form.get("admin_resolution", "").strip()
    refund = request.form.get("refund_amount", 0, type=int)
    if resolution:
        dispute.admin_resolution = resolution
        dispute.refund_amount = refund or 0
        dispute.status = Dispute.STATUS_RESOLVED
        db.session.commit()
        flash(f"Đã xử lý tranh chấp {dispute.dispute_code}.", "success")
    return redirect(url_for("admin.index", view="disputes"))


@admin_bp.route("/payments")
@admin_required
def payments():
    return redirect(url_for("admin.index", view="payments"))


@admin_bp.route("/promotions")
@admin_required
def promotions():
    return redirect(url_for("admin.index", view="promotions"))


@admin_bp.route("/admins")
@admin_required
def admins():
    return redirect(url_for("admin.index", view="admins"))


@admin_bp.route("/payments/<int:booking_id>/reprocess", methods=["POST"])
@admin_required
def reprocess_payment(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if booking.payment_status != "paid":
        booking.payment_status = "paid"
        db.session.commit()
        flash(f"Đã xử lý thanh toán cho booking {booking.booking_code}.", "success")
    return redirect(url_for("admin.index", view="payments"))


@admin_bp.route("/promotions/create", methods=["POST"])
@admin_required
def create_promotion():
    name = request.form.get("name", "").strip()
    promo_type = request.form.get("type", "Phiếu giảm giá").strip()
    discount = request.form.get("discount_value", "").strip()
    start_date = request.form.get("start_date", "").strip()
    end_date = request.form.get("end_date", "").strip()
    host_id = request.form.get("host_id", type=int)
    if not host_id:
        host = User.query.filter_by(role="host").first()
        host_id = host.id if host else None
    if not name or not host_id:
        flash("Vui lòng nhập đủ thông tin khuyến mãi.", "error")
        return redirect(url_for("admin.index", view="promotions"))
    promo = Promotion(
        host_id=host_id,
        name=name,
        type=promo_type,
        discount_value=discount,
        start_date=start_date,
        end_date=end_date,
        status=True,
    )
    db.session.add(promo)
    db.session.commit()
    flash(f"Đã tạo khuyến mãi: {name}", "success")
    return redirect(url_for("admin.index", view="promotions"))


@admin_bp.route("/promotions/<int:promo_id>/toggle", methods=["POST"])
@admin_required
def toggle_promotion(promo_id):
    promo = Promotion.query.get_or_404(promo_id)
    promo.status = request.form.get("enabled") == "1"
    db.session.commit()
    state = "bật" if promo.status else "tắt"
    flash(f"Đã {state} khuyến mãi {promo.name}.", "success")
    return redirect(url_for("admin.index", view="promotions"))


@admin_bp.route("/admins/create", methods=["POST"])
@admin_required
def create_admin():
    full_name = request.form.get("full_name", "").strip()
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "").strip()
    phone = request.form.get("phone", "").strip()
    admin_role = _resolve_admin_role(request.form.get("admin_role"))
    if not full_name or not email or not password:
        flash("Vui lòng nhập đủ họ tên, email và mật khẩu.", "error")
        return redirect(url_for("admin.index", view="admins"))
    if User.query.filter_by(email=email).first():
        flash("Email đã tồn tại trong hệ thống.", "error")
        return redirect(url_for("admin.index", view="admins"))
    admin = User(
        full_name=full_name,
        email=email,
        phone=phone or None,
        role="admin",
        admin_role=admin_role,
        is_email_verified=True,
    )
    admin.set_password(password)
    db.session.add(admin)
    db.session.commit()
    flash(f"Đã tạo tài khoản quản trị viên: {email}", "success")
    return redirect(url_for("admin.index", view="admins"))


@admin_bp.route("/admins/<int:admin_id>/update", methods=["POST"])
@admin_required
def update_admin(admin_id):
    admin = User.query.get_or_404(admin_id)
    if admin.role != "admin":
        abort(403)

    full_name = request.form.get("full_name", "").strip()
    email = request.form.get("email", "").strip().lower()
    phone = request.form.get("phone", "").strip()
    status = request.form.get("status", "").strip()
    admin_role = request.form.get("admin_role", "").strip()
    password = request.form.get("password", "").strip()

    if not full_name or not email:
        flash("Vui lòng nhập đủ họ tên và email.", "error")
        return redirect(url_for("admin.index", view="admins"))

    if email != admin.email and User.query.filter_by(email=email).first():
        flash("Email đã tồn tại trong hệ thống.", "error")
        return redirect(url_for("admin.index", view="admins"))

    if password and len(password) < 6:
        flash("Mật khẩu mới phải có ít nhất 6 ký tự.", "error")
        return redirect(url_for("admin.index", view="admins"))

    admin.full_name = full_name
    admin.email = email
    admin.phone = phone or None

    if admin_id != current_user.id:
        admin.is_locked = status == "revoked"
        if current_user.is_super_admin:
            admin.admin_role = _resolve_admin_role(admin_role or admin.admin_role)
    elif current_user.is_super_admin and admin_role:
        admin.admin_role = _resolve_admin_role(admin_role)

    if password:
        admin.set_password(password)

    db.session.commit()
    flash(f"Đã cập nhật quản trị viên: {admin.email}", "success")
    return redirect(url_for("admin.index", view="admins"))


@admin_bp.route("/admins/<int:admin_id>/toggle-lock", methods=["POST"])
@admin_required
def toggle_admin_lock(admin_id):
    if admin_id == current_user.id:
        flash("Không thể khóa tài khoản đang đăng nhập.", "error")
        return redirect(url_for("admin.index", view="admins"))
    admin = User.query.get_or_404(admin_id)
    if admin.role != "admin":
        abort(403)
    admin.is_locked = not admin.is_locked
    db.session.commit()
    state = "khóa" if admin.is_locked else "mở khóa"
    flash(f"Đã {state} tài khoản {admin.email}.", "success")
    return redirect(url_for("admin.index", view="admins"))


@admin_bp.route("/reports/<report_type>/export")
@admin_required
def export_report(report_type):
    output = io.StringIO()
    writer = csv.writer(output)

    if report_type == "Doanh thu":
        writer.writerow(["Mã booking", "Khách", "Tổng tiền", "Trạng thái", "Ngày tạo"])
        for b in Booking.query.order_by(Booking.created_at.desc()).all():
            writer.writerow([
                b.booking_code,
                b.guest_name,
                b.total_amount or 0,
                b.status,
                b.created_at.strftime("%Y-%m-%d") if b.created_at else "",
            ])
        filename = "bao-cao-doanh-thu.csv"
    elif report_type == "Tranh chấp":
        writer.writerow(["Mã tranh chấp", "Booking", "Khiếu nại", "Trạng thái", "Hoàn tiền"])
        for d in Dispute.query.order_by(Dispute.created_at.desc()).all():
            writer.writerow([
                d.dispute_code,
                d.booking.booking_code if d.booking else "",
                (d.guest_complaint or "")[:120],
                d.status,
                d.refund_amount or 0,
            ])
        filename = "bao-cao-tranh-chap.csv"
    elif report_type == "Đặt phòng":
        writer.writerow(["Mã booking", "Khách sạn", "Check-in", "Check-out", "Giá trị", "Trạng thái"])
        for b in Booking.query.order_by(Booking.created_at.desc()).all():
            acc = b.room.accommodation.name if b.room and b.room.accommodation else ""
            writer.writerow([
                b.booking_code,
                acc,
                b.check_in.strftime("%Y-%m-%d") if b.check_in else "",
                b.check_out.strftime("%Y-%m-%d") if b.check_out else "",
                b.total_amount or 0,
                b.status,
            ])
        filename = "bao-cao-dat-phong.csv"
    else:
        writer.writerow(["Loại", "Số lượng"])
        writer.writerow(["Khách hàng", User.query.filter_by(role="guest").count()])
        writer.writerow(["Host", User.query.filter_by(role="host").count()])
        writer.writerow(["Booking", Booking.query.count()])
        writer.writerow(["Tranh chấp", Dispute.query.count()])
        filename = "bao-cao-van-hanh.csv"

    response = make_response("\ufeff" + output.getvalue())
    response.headers["Content-Type"] = "text/csv; charset=utf-8"
    response.headers["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response
