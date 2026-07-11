from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from backend.app.models import Promotion
from backend.app.extensions import db

promotion_bp = Blueprint("promotion", __name__, url_prefix="/promotions")

@promotion_bp.route("/")
@login_required
def index():
    promotions = Promotion.query.filter_by(host_id=current_user.id).all()
    return render_template(
        "host/promotion/index.html",
        active_nav="accommodations",
        promotions=promotions
    )

@promotion_bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        promo = Promotion(
            host_id=current_user.id,
            name=request.form.get("name"),
            type=request.form.get("type"),
            discount_value=request.form.get("discount_value"),
            start_date=request.form.get("start_date"),
            end_date=request.form.get("end_date"),
            min_nights=request.form.get("min_nights", 1),
            apply_days=request.form.get("apply_days", "Tất cả các ngày"),
            not_combine="not_combine" in request.form,
            status=True
        )
        db.session.add(promo)
        db.session.commit()
        return redirect(url_for("promotion.index"))
        
    return render_template(
        "host/promotion/form.html",
        active_nav="accommodations",
        promo=None,
        prefill={
            "name": request.args.get("name", ""),
            "type": request.args.get("type", ""),
            "discount_value": request.args.get("discount_value", ""),
            "apply_days": request.args.get("apply_days", ""),
            "min_nights": request.args.get("min_nights", ""),
        },
    )

@promotion_bp.route("/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit(id):
    promo = Promotion.query.get_or_404(id)
    if request.method == "POST":
        promo.name = request.form.get("name")
        promo.type = request.form.get("type")
        promo.discount_value = request.form.get("discount_value")
        promo.start_date = request.form.get("start_date")
        promo.end_date = request.form.get("end_date")
        promo.min_nights = request.form.get("min_nights", 1)
        promo.apply_days = request.form.get("apply_days", "Tất cả các ngày")
        promo.not_combine = "not_combine" in request.form
        
        db.session.commit()
        return redirect(url_for("promotion.index"))
        
    return render_template(
        "host/promotion/form.html",
        active_nav="accommodations",
        promo=promo
    )

@promotion_bp.route("/<int:id>/delete", methods=["POST"])
@login_required
def delete(id):
    promo = Promotion.query.get_or_404(id)
    db.session.delete(promo)
    db.session.commit()
    return redirect(url_for("promotion.index"))
