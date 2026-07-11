from flask import Blueprint, render_template, request, flash, redirect, url_for, session, abort, jsonify
from flask_login import current_user
from datetime import datetime, timedelta
import uuid

from backend.app.models import Room, Booking
from backend.app.extensions import db
from backend.app.services.booking_notify import send_booking_confirmation_email
from backend.app.services.ai_chat import chat_completion

customer_booking_bp = Blueprint("customer_booking", __name__, url_prefix="/customer/booking")


def _grant_anonymous_access(booking_code: str):
    codes = list(session.get("anonymous_booking_codes") or [])
    if booking_code not in codes:
        codes.append(booking_code)
        session["anonymous_booking_codes"] = codes


def _can_access_booking(booking: Booking) -> bool:
    if current_user.is_authenticated and booking.guest_id and booking.guest_id == current_user.id:
        return True
    if not booking.guest_id:
        return booking.booking_code in (session.get("anonymous_booking_codes") or [])
    return False


def _get_booking_or_403(booking_code: str) -> Booking:
    code = booking_code if booking_code.startswith("#") else f"#{booking_code}"
    booking = Booking.query.filter_by(booking_code=code).first_or_404()
    if not _can_access_booking(booking):
        abort(403)
    return booking


def _notify_and_redirect(booking: Booking, *, success_msg: str):
    email_meta = send_booking_confirmation_email(booking)
    flash(f"{success_msg} Email xác nhận đã gửi tới {email_meta['to']} (mô phỏng).", "success")
    return redirect(url_for("customer_booking.order_detail", booking_code=booking.booking_code.lstrip("#")))


@customer_booking_bp.route("/create/<int:room_id>", methods=["POST"])
def create_booking(room_id):
    room = Room.query.get_or_404(room_id)

    check_in_str = request.form.get("check_in")
    check_out_str = request.form.get("check_out")
    guest_count = request.form.get("guest_count", 1, type=int)
    guest_note = request.form.get("guest_note", "")

    try:
        check_in = datetime.strptime(check_in_str, "%Y-%m-%d").date()
        check_out = datetime.strptime(check_out_str, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        flash("Ngày check-in hoặc check-out không hợp lệ.", "error")
        return redirect(url_for("customer.accommodation_detail", id=room.accommodation_id))

    if check_in >= check_out:
        flash("Ngày trả phòng phải sau ngày nhận phòng.", "error")
        return redirect(url_for("customer.accommodation_detail", id=room.accommodation_id))

    overlap = Booking.query.filter(
        Booking.room_id == room_id,
        Booking.status.in_([Booking.STATUS_CONFIRMED, Booking.STATUS_HOLDING]),
        Booking.check_in < check_out,
        Booking.check_out > check_in,
    ).first()

    if overlap and overlap.status == Booking.STATUS_HOLDING and overlap.hold_expiry_at and overlap.hold_expiry_at < datetime.utcnow():
        overlap.status = Booking.STATUS_CANCELLED
        db.session.commit()
    elif overlap:
        flash("Phòng đã được đặt hoặc đang có người giữ chỗ trong khoảng thời gian này.", "error")
        return redirect(url_for("customer.accommodation_detail", id=room.accommodation_id))

    nights = (check_out - check_in).days
    total_amount = room.base_price * nights

    booking_code = f"#RV{uuid.uuid4().hex[:6].upper()}"

    if current_user.is_authenticated:
        guest_id = current_user.id
        guest_name = current_user.full_name
        guest_phone = current_user.phone
        guest_email = current_user.email
    else:
        guest_id = None
        guest_name = "Khách vãng lai"
        guest_phone = None
        guest_email = None

    booking = Booking(
        booking_code=booking_code,
        room_id=room_id,
        guest_id=guest_id,
        guest_name=guest_name,
        guest_phone=guest_phone,
        guest_email=guest_email,
        guest_count=guest_count,
        guest_note=guest_note,
        check_in=check_in,
        check_out=check_out,
        total_amount=total_amount,
        status=Booking.STATUS_HOLDING,
        hold_expiry_at=datetime.utcnow() + timedelta(minutes=15),
    )

    db.session.add(booking)
    db.session.commit()

    if not current_user.is_authenticated:
        _grant_anonymous_access(booking.booking_code)

    return redirect(url_for("customer_booking.checkout", booking_code=booking.booking_code.lstrip("#")))


@customer_booking_bp.route("/checkout/<booking_code>", methods=["GET", "POST"])
def checkout(booking_code):
    booking = _get_booking_or_403(booking_code)

    if booking.status != Booking.STATUS_HOLDING:
        flash("Booking này không ở trạng thái chờ thanh toán.", "warning")
        return redirect(url_for("customer.index"))

    if booking.hold_expiry_at and booking.hold_expiry_at < datetime.utcnow():
        booking.status = Booking.STATUS_CANCELLED
        db.session.commit()
        flash("Thời gian giữ chỗ đã hết hạn. Vui lòng đặt lại.", "error")
        return redirect(url_for("customer.index"))

    is_guest_checkout = not current_user.is_authenticated or booking.guest_id is None

    if request.method == "POST":
        guest_name = (request.form.get("guest_name") or "").strip()
        guest_email = (request.form.get("guest_email") or "").strip()
        guest_phone = (request.form.get("guest_phone") or "").strip()

        if is_guest_checkout:
            if not guest_name or not guest_email or not guest_phone:
                flash("Vui lòng nhập đầy đủ họ tên, email và số điện thoại.", "error")
                pricing = _compute_pricing(booking, request.form)
                return render_template(
                    "customer/pages/checkout.html",
                    booking=booking,
                    pricing=pricing,
                    is_guest_checkout=is_guest_checkout,
                )

        booking.guest_name = guest_name or booking.guest_name
        booking.guest_email = guest_email or booking.guest_email
        booking.guest_phone = guest_phone or booking.guest_phone
        booking.guest_note = request.form.get("guest_note", booking.guest_note)

        pricing = _compute_pricing(booking, request.form)
        booking.total_amount = pricing["total"]
        db.session.commit()

        payment_method = request.form.get("payment_method")

        if payment_method == "cash":
            booking.status = Booking.STATUS_CONFIRMED
            booking.payment_method = "cash"
            booking.payment_status = "pending"
            booking.commission_fee = int(booking.total_amount * 0.15)
            booking.host_payout_amount = booking.total_amount - booking.commission_fee
            db.session.commit()
            return _notify_and_redirect(
                booking,
                success_msg="Đặt phòng thành công! Bạn sẽ thanh toán bằng tiền mặt khi nhận phòng.",
            )

        return redirect(url_for("customer_booking.mock_gateway", booking_code=booking.booking_code.lstrip("#")))

    pricing = _compute_pricing(booking, request.args)
    return render_template(
        "customer/pages/checkout.html",
        booking=booking,
        pricing=pricing,
        is_guest_checkout=is_guest_checkout,
    )


PROMO_CODES = {
    "WELCOME10": ("percent", 0.10, "Giảm 10% cho thành viên mới"),
    "ROVVA50": ("fixed", 50000, "Giảm trực tiếp 50.000đ"),
}

XU_DISCOUNT = 50000


def _compute_pricing(booking, source):
    room = booking.room
    nights = booking.nights
    room_subtotal = (room.base_price or 0) * nights

    selected_services = source.getlist("service") if hasattr(source, "getlist") else []
    services = []
    services_total = 0
    for s in (room.services or []):
        if isinstance(s, dict) and s.get("name") in selected_services:
            price = int(s.get("price") or 0)
            services.append({"name": s.get("name"), "price": price})
            services_total += price

    promo_code = (source.get("promo_code") or "").strip().upper()
    promo_discount = 0
    promo_label = None
    if promo_code in PROMO_CODES:
        kind, value, label = PROMO_CODES[promo_code]
        promo_discount = int(room_subtotal * value) if kind == "percent" else int(value)
        promo_label = label

    use_xu = bool(source.get("use_xu")) and current_user.is_authenticated
    xu_discount = XU_DISCOUNT if use_xu else 0

    total = max(0, room_subtotal + services_total - promo_discount - xu_discount)

    return {
        "nights": nights,
        "room_price": room.base_price or 0,
        "room_subtotal": room_subtotal,
        "services": services,
        "services_total": services_total,
        "promo_code": promo_code,
        "promo_label": promo_label,
        "promo_discount": promo_discount,
        "use_xu": use_xu,
        "xu_discount": xu_discount,
        "total": total,
    }


@customer_booking_bp.route("/order/<booking_code>")
def order_detail(booking_code):
    booking = _get_booking_or_403(booking_code)
    email_meta = None
    if request.args.get("sent") == "1":
        email_meta = send_booking_confirmation_email(booking)
    return render_template(
        "customer/pages/booking/detail.html",
        booking=booking,
        email_meta=email_meta,
        is_guest_order=booking.guest_id is None,
    )


@customer_booking_bp.route("/success/<booking_code>")
def success(booking_code):
    return redirect(url_for("customer_booking.order_detail", booking_code=booking_code))


@customer_booking_bp.route("/mock-gateway/<booking_code>")
def mock_gateway(booking_code):
    booking = _get_booking_or_403(booking_code)
    return render_template("customer/pages/mock_payment.html", booking=booking)


@customer_booking_bp.route("/payment-callback/<booking_code>")
def payment_callback(booking_code):
    booking = _get_booking_or_403(booking_code)

    status = request.args.get("status")
    if status == "success":
        booking.status = Booking.STATUS_CONFIRMED
        booking.payment_status = "paid"
        booking.payment_method = "online"
        booking.payment_gateway_ref = f"TXN{uuid.uuid4().hex[:8].upper()}"
        booking.commission_fee = int(booking.total_amount * 0.15)
        booking.host_payout_amount = booking.total_amount - booking.commission_fee
        db.session.commit()
        return _notify_and_redirect(booking, success_msg="Thanh toán thành công! Chúc bạn có kỳ nghỉ vui vẻ.")

    flash("Thanh toán thất bại hoặc bị hủy. Vui lòng thử lại.", "error")
    return redirect(url_for("customer_booking.checkout", booking_code=booking.booking_code.lstrip("#")))


@customer_booking_bp.route("/api/ai-chat", methods=["POST"])
def ai_chat_api():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()
    history = data.get("history") or []

    if not message:
        return jsonify({"error": "Tin nhắn trống."}), 400

    messages = []
    for item in history[-8:]:
        role = item.get("role")
        content = (item.get("content") or "").strip()
        if role in ("user", "assistant") and content:
            messages.append({"role": role, "content": content})
    messages.append({"role": "user", "content": message})

    try:
        reply = chat_completion(messages)
    except RuntimeError as exc:
        return jsonify({"error": str(exc)}), 503

    return jsonify({"reply": reply, "source": "groq"})
