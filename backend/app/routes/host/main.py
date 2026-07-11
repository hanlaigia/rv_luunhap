from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from backend.app.models import Accommodation, Booking, Notification, Room
from backend.app.services.ai_chat import HOST_SYSTEM_PROMPT, chat_completion
from backend.app.services.host_copilot import build_recommendations
from backend.app.services.host_dashboard import get_host_stats, get_revenue_chart
from backend.app.utils.guest_insight import build_guest_insight
from backend.app.utils.host_display import booking_status_badge_class, booking_status_label
from backend.app.utils.notification_links import notification_action_label, notification_action_url

main_bp = Blueprint("main", __name__)


def _copilot_action_url(rec):
    """Chuyển action_url + params thành URL thật."""
    from urllib.parse import urlencode

    name = rec.get("action_url")
    params = dict(rec.get("action_params") or {})
    if not name:
        return "#"
    try:
        if name == "promotion.create":
            base = url_for(name)
            return f"{base}?{urlencode(params)}" if params else base
        return url_for(name, **params)
    except Exception:
        return "#"


@main_bp.route("/")
@login_required
def index():
    period = request.args.get("period", "7d")
    if period not in ("7d", "30d"):
        period = "7d"

    stats = get_host_stats(current_user.id)
    chart = get_revenue_chart(current_user.id, period)

    recent_bookings = (
        Booking.query.join(Room)
        .join(Accommodation)
        .filter(Accommodation.host_id == current_user.id)
        .order_by(Booking.created_at.desc())
        .limit(6)
        .all()
    )

    copilot_recs, copilot_ctx = build_recommendations(current_user.id)
    tips = []
    for rec in copilot_recs:
        rec = dict(rec)
        if rec.get("action_url") == "copilot.index":
            continue
        rec["href"] = _copilot_action_url(rec)
        tips.append(rec)

    for booking in recent_bookings:
        insight = build_guest_insight(booking)
        if not insight:
            continue
        tips.append(
            {
                "id": f"guest_insight_{booking.id}",
                "icon": insight["icon"],
                "title": f"Guest insight — {insight['guest_name']}",
                "description": insight["suggestion"],
                "impact": insight["label"],
                "action_label": "Xem booking",
                "href": url_for("booking.detail", id=booking.id),
                "category": "insight",
            }
        )

    tip_summary = (
        f"Tỷ lệ lấp đầy tuần tới {(copilot_ctx.get('next_week_occupancy', 0) * 100):.0f}%. "
        "Xem gợi ý khuyến mãi, giá phòng và insight khách."
    )

    return render_template(
        "host/index.html",
        active_nav="dashboard",
        stats=stats,
        chart=chart,
        chart_period=period,
        recent_bookings=recent_bookings,
        host=current_user,
        revenue_tips=tips[:8],
        tip_summary=tip_summary,
        booking_status_label=booking_status_label,
        booking_status_badge_class=booking_status_badge_class,
    )


@main_bp.route("/notifications")
@login_required
def notifications():
    from datetime import datetime as dt

    category = request.args.get("category", "all")
    date_from = request.args.get("date_from")
    date_to = request.args.get("date_to")

    q = Notification.query.filter_by(user_id=current_user.id)
    if category != "all":
        q = q.filter_by(category=category)
    if date_from:
        q = q.filter(Notification.created_at >= dt.strptime(date_from, "%Y-%m-%d"))
    if date_to:
        end = dt.strptime(date_to, "%Y-%m-%d").replace(hour=23, minute=59, second=59)
        q = q.filter(Notification.created_at <= end)

    items = q.order_by(Notification.created_at.desc()).all()

    counts = {
        "all": Notification.query.filter_by(user_id=current_user.id).count(),
        "booking": Notification.query.filter_by(user_id=current_user.id, category="booking").count(),
        "payment": Notification.query.filter_by(user_id=current_user.id, category="payment").count(),
        "dispute": Notification.query.filter_by(user_id=current_user.id, category="dispute").count(),
        "system": Notification.query.filter_by(user_id=current_user.id, category="system").count(),
    }

    return render_template(
        "host/notifications.html",
        active_nav="dashboard",
        notifications=items,
        category=category,
        counts=counts,
        date_from=date_from or "",
        date_to=date_to or "",
        notification_action_url=notification_action_url,
        notification_action_label=notification_action_label,
        now=dt.utcnow(),
    )


@main_bp.route("/ai-chat")
@login_required
def ai_chat():
    return render_template(
        "host/chat.html",
        active_nav="dashboard",
        hide_footer=True,
    )


@main_bp.route("/notifications/mark-all-read", methods=["POST"])
@login_required
def mark_all_notifications_read():
    from backend.app.extensions import db
    Notification.query.filter_by(user_id=current_user.id, is_read=False).update({"is_read": True})
    db.session.commit()
    return redirect(request.referrer or url_for("main.index"))


@main_bp.route("/notifications/<int:id>/read", methods=["POST"])
@login_required
def mark_notification_read(id):
    note = Notification.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    from backend.app.extensions import db
    note.is_read = True
    db.session.commit()
    return redirect(request.referrer or url_for("main.notifications"))


@main_bp.route("/api/ai-chat", methods=["POST"])
@login_required
def ai_chat_api():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()
    if not message:
        return jsonify({"error": "Tin nhắn trống."}), 400
    history = data.get("history") or []
    messages = [{"role": h.get("role"), "content": h.get("content")} for h in history if h.get("content")]
    messages.append({"role": "user", "content": message})
    try:
        reply = chat_completion(messages, system_prompt=HOST_SYSTEM_PROMPT)
        return jsonify({"reply": reply})
    except RuntimeError as exc:
        return jsonify({"error": str(exc)}), 503
    except Exception as exc:
        return jsonify({"error": f"Lỗi AI: {exc}"}), 500


@main_bp.route("/profile")
@login_required
def profile():
    return render_template(
        "host/profile.html",
        active_nav="profile",
        host=current_user
    )

@main_bp.route("/profile/edit", methods=["POST"])
@login_required
def edit_profile():
    from backend.app.extensions import db
    from werkzeug.utils import secure_filename
    
    user = current_user
    user.full_name = request.form.get("full_name", user.full_name)
    user.email = request.form.get("email", user.email)
    user.phone = request.form.get("phone", user.phone)
    if not user.id_card:
        id_card = request.form.get("id_card", "").strip()
        if id_card:
            user.id_card = id_card
    user.introduction = request.form.get("introduction", user.introduction)
    
    if "avatar" in request.files:
        file = request.files["avatar"]
        if file.filename != "":
            filename = secure_filename(file.filename)
            user.avatar = f"images/{filename}"
            
    db.session.commit()
    return redirect(url_for("main.profile"))

@main_bp.route("/profile/change-password", methods=["POST"])
@login_required
def change_password():
    from backend.app.extensions import db
    from flask import flash
    
    user = current_user
    current_password = request.form.get("current_password")
    new_password = request.form.get("new_password")
    confirm_password = request.form.get("confirm_password")
    
    if not user.check_password(current_password):
        flash("Mật khẩu hiện tại không đúng.", "danger")
        return redirect(url_for("main.profile"))
        
    if new_password != confirm_password:
        flash("Mật khẩu mới không khớp.", "error")
        return redirect(url_for("main.profile"))
        
    user.set_password(new_password)
    db.session.commit()
    flash("Đổi mật khẩu thành công.", "success")
    return redirect(url_for("main.profile"))
