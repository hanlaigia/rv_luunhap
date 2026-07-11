from datetime import datetime
from backend.app.extensions import db

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=True)
    phone = db.Column(db.String(20))
    id_card = db.Column(db.String(20), nullable=True)
    introduction = db.Column(db.Text, nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    birthday = db.Column(db.Date, nullable=True)
    city = db.Column(db.String(120), nullable=True)
    avatar = db.Column(db.String(255), nullable=True)
    role = db.Column(db.String(20), default="guest") # guest, host, admin
    admin_role = db.Column(db.String(20), nullable=True)  # super, admin, support
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Auth Status
    is_email_verified = db.Column(db.Boolean, default=False)
    email_verification_token = db.Column(db.String(255), nullable=True)
    reset_password_token = db.Column(db.String(255), nullable=True)
    reset_password_expiry = db.Column(db.DateTime, nullable=True)
    failed_login_attempts = db.Column(db.Integer, default=0)
    is_locked = db.Column(db.Boolean, default=False)
    
    # Host Onboarding Status
    host_status = db.Column(db.String(20), default="none") # none, pending, approved, rejected
    host_document_path = db.Column(db.String(255), nullable=True)

    accommodations = db.relationship("Accommodation", back_populates="host", lazy="dynamic")
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    @property
    def is_super_admin(self):
        return self.role == "admin" and (self.admin_role or "admin") == "super"

    @property
    def admin_role_label(self):
        from backend.app.utils.admin_roles import admin_role_label
        if self.role != "admin":
            return None
        return admin_role_label(self.admin_role)

    @property
    def admin_status_label(self):
        from backend.app.utils.admin_roles import admin_status_label
        if self.role != "admin":
            return None
        return admin_status_label(self.is_locked)

    @property
    def avatar_url(self):
        from backend.app.utils.media import user_avatar
        return user_avatar(self.id) if self.id else user_avatar(0)

    def __repr__(self):
        return f"<User {self.full_name}>"
