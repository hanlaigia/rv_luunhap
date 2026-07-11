from flask import Blueprint, render_template
from flask_login import login_required

support_bp = Blueprint("support", __name__)


@support_bp.route("/faq")
@login_required
def faq():
    return render_template("host/pages/support/faq.html")


@support_bp.route("/room-guide")
@login_required
def room_guide():
    return render_template("host/pages/support/room-guide.html")


@support_bp.route("/cancellation-policy")
@login_required
def cancellation_policy():
    return render_template("host/pages/support/cancellation-policy.html")


@support_bp.route("/accommodation-guide")
@login_required
def accommodation_guide():
    return render_template("host/pages/support/accommodation-guide.html")


@support_bp.route("/booking-guide")
@login_required
def booking_guide():
    return render_template("host/pages/support/booking-guide.html")


@support_bp.route("/terms-of-service")
@login_required
def terms_of_service():
    return render_template("host/pages/support/terms-of-service.html")


@support_bp.route("/privacy-policy")
@login_required
def privacy_policy():
    return render_template("host/pages/support/privacy-policy.html")


@support_bp.route("/content-policy")
@login_required
def content_policy():
    return render_template("host/pages/support/content-policy.html")


@support_bp.route("/payment-policy")
@login_required
def payment_policy():
    return render_template("host/pages/support/payment-policy.html")


@support_bp.route("/dispute-policy")
@login_required
def dispute_policy():
    return render_template("host/pages/support/dispute-policy.html")


@support_bp.route("/smart-pricing")
@login_required
def smart_pricing():
    return render_template("host/pages/support/smart-pricing.html")
