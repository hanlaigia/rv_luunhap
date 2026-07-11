from backend.app.routes.host.main import main_bp
from backend.app.routes.host.accommodation import accommodation_bp
from backend.app.routes.host.promotion import promotion_bp
from backend.app.routes.host.booking import booking_bp
from backend.app.routes.host.report import report_bp
from backend.app.routes.host.dispute import dispute_bp
from backend.app.routes.host.payment import payment_bp
from backend.app.routes.host.message import message_bp
from backend.app.routes.customer.main import customer_bp
from backend.app.routes.customer.booking import customer_booking_bp
from backend.app.routes.auth.routes import auth_bp
from backend.app.routes.admin import admin_bp

__all__ = ["main_bp", "accommodation_bp", "promotion_bp", "booking_bp", "report_bp", "dispute_bp", "payment_bp", "message_bp", "customer_bp", "customer_booking_bp", "auth_bp", "admin_bp"]

def register_blueprints(app):
    app.register_blueprint(main_bp, url_prefix="/host")
    app.register_blueprint(accommodation_bp, url_prefix="/host/accommodation")
    app.register_blueprint(promotion_bp, url_prefix="/host/promotion")
    app.register_blueprint(booking_bp, url_prefix="/host/booking")
    app.register_blueprint(report_bp, url_prefix="/host/report")
    app.register_blueprint(dispute_bp, url_prefix="/host/dispute")
    app.register_blueprint(payment_bp, url_prefix="/host/payment")
    app.register_blueprint(message_bp, url_prefix="/host/message")
    app.register_blueprint(customer_bp)
    app.register_blueprint(customer_booking_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")
