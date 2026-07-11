import os

from flask import Flask, redirect, url_for
from flask_login import current_user

from backend.app.config import config_by_name
from backend.app.extensions import db, login_manager
from backend.app.routes import register_blueprints


def create_app(config_name="default"):
    config = config_by_name[config_name]
    os.makedirs(config.INSTANCE_DIR, exist_ok=True)

    app = Flask(
        __name__,
        template_folder=config.TEMPLATE_FOLDER,
        static_folder=config.STATIC_FOLDER,
        static_url_path="/static",
        instance_path=config.INSTANCE_DIR,
    )
    app.config.from_object(config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    
    @login_manager.user_loader
    def load_user(user_id):
        from backend.app.models import User
        return User.query.get(int(user_id))

    register_blueprints(app)
    register_cli(app)

    @app.route("/")
    def root():
        """Trang chủ mặc định: guest (chưa đăng nhập) hoặc member."""
        if current_user.is_authenticated and current_user.role == "admin":
            return redirect(url_for("admin.index"))
        if current_user.is_authenticated and current_user.role in ("host",):
            return redirect(url_for("main.index"))
        return redirect(url_for("customer.index"))

    @app.context_processor
    def inject_media_helpers():
        from backend.app.utils.media import resolve_media

        return {"resolve_media": resolve_media}

    from backend.app.utils.reviews import (
        SUB_RATING_LABELS,
        SUB_RATING_KEYS,
        format_review_datetime,
        format_stay_range,
        format_vnd,
        rating_label,
    )

    app.add_template_global(format_stay_range, "format_stay_range")
    app.add_template_global(format_vnd, "format_vnd")
    app.add_template_global(rating_label, "rating_label")
    app.add_template_global(format_review_datetime, "format_review_datetime")
    app.add_template_global(SUB_RATING_LABELS, "sub_rating_labels")
    app.add_template_global(SUB_RATING_KEYS, "sub_rating_keys")

    with app.app_context():
        from backend.app import models  # noqa: F401

        db.create_all()
        from backend.app.seed import (
            patch_guest_review_demo,
            patch_host_payment_demo,
            patch_review_schema,
            seed_database,
        )

        patch_review_schema()
        seed_database()
        patch_host_payment_demo()
        patch_guest_review_demo()

    return app


def register_cli(app):
    @app.cli.command("seed")
    def seed_command():
        """Reset and seed the database with sample data."""
        from backend.app.seed import seed_database

        db.drop_all()
        db.create_all()
        if seed_database():
            print("Database seeded successfully.")
        else:
            print("Database already contains data. Use drop/create first.")
        from backend.app.seed import patch_host_payment_demo

        patch_host_payment_demo()
