from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
import uuid
from datetime import datetime, timedelta

from backend.app.models import User
from backend.app.extensions import db

auth_bp = Blueprint("auth", __name__)


def _is_customer_role(user):
    return user.role in ("guest", "customer")


def _redirect_after_login(user):
    """Điều hướng sau đăng nhập theo vai trò; chặn next trỏ sai portal."""
    next_page = request.args.get("next") or request.form.get("next")
    if next_page and next_page.startswith("/") and not next_page.startswith("//"):
        if _is_customer_role(user) and (
            next_page.startswith("/admin") or next_page.startswith("/host")
        ):
            next_page = None
        elif user.role == "host" and next_page.startswith("/admin"):
            next_page = None
        if next_page:
            return redirect(next_page)

    if user.role == "admin":
        return redirect(url_for("admin.index"))
    if user.role == "host":
        return redirect(url_for("main.index"))
    return redirect(url_for("customer.index"))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated and _is_customer_role(current_user):
        return redirect(url_for("customer.index"))
            
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        user = User.query.filter_by(email=email).first()
        if user:
            if user.is_locked:
                flash("Tài khoản của bạn đã bị khóa do đăng nhập sai nhiều lần. Vui lòng liên hệ Admin.", "error")
                return redirect(url_for("auth.login"))
                
            if not user.is_email_verified:
                flash("Vui lòng xác thực email trước khi đăng nhập.", "warning")
                return redirect(url_for("auth.login"))
                
            if user.check_password(password):
                user.failed_login_attempts = 0
                db.session.commit()
                
                login_user(user)
                return _redirect_after_login(user)
            else:
                user.failed_login_attempts += 1
                if user.failed_login_attempts >= 5:
                    user.is_locked = True
                db.session.commit()
                
        flash("Email hoặc mật khẩu không chính xác.", "error")
        
    return render_template("auth/login.html")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated and _is_customer_role(current_user):
        return redirect(url_for("customer.index"))
            
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        
        # Check if email exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email này đã được sử dụng. Vui lòng đăng nhập hoặc dùng email khác.", "error")
            return redirect(url_for("auth.register"))
            
        if password != confirm_password:
            flash("Mật khẩu xác nhận không khớp.", "error")
            return redirect(url_for("auth.register"))
            
        # Create user
        verification_token = str(uuid.uuid4())
        new_user = User(
            full_name=name,
            email=email,
            phone=phone,
            role="guest",
            is_email_verified=False,
            email_verification_token=verification_token
        )
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        # Simulate sending email by showing a beautiful demo inbox page
        return render_template("auth/verify_notice.html", action="register", email=email, token=verification_token)
        
    return render_template("auth/register.html")

@auth_bp.route("/verify-email/<token>")
def verify_email(token):
    user = User.query.filter_by(email_verification_token=token).first()
    if not user:
        flash("Liên kết xác thực không hợp lệ hoặc đã hết hạn.", "error")
        return redirect(url_for("auth.login"))
        
    user.is_email_verified = True
    user.email_verification_token = None
    db.session.commit()
    flash("Xác thực email thành công! Bạn có thể đăng nhập.", "success")
    return redirect(url_for("auth.login"))

@auth_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email")
        user = User.query.filter_by(email=email).first()
        if user:
            reset_token = str(uuid.uuid4())
            user.reset_password_token = reset_token
            user.reset_password_expiry = datetime.utcnow() + timedelta(hours=1)
            db.session.commit()
            
            # Simulate sending email by showing a beautiful demo inbox page
            return render_template("auth/verify_notice.html", action="reset", email=email, token=reset_token)
            
        flash("Nếu email tồn tại trong hệ thống, bạn sẽ nhận được một email hướng dẫn đặt lại mật khẩu.", "success")
        return redirect(url_for("auth.login"))
        
    return render_template("auth/forgot_password.html")

@auth_bp.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    user = User.query.filter_by(reset_password_token=token).first()
    if not user or (user.reset_password_expiry and user.reset_password_expiry < datetime.utcnow()):
        flash("Liên kết đặt lại mật khẩu không hợp lệ hoặc đã hết hạn.", "error")
        return redirect(url_for("auth.forgot_password"))
        
    if request.method == "POST":
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        
        if password != confirm_password:
            flash("Mật khẩu xác nhận không khớp.", "error")
            return redirect(url_for("auth.reset_password", token=token))
            
        user.set_password(password)
        user.reset_password_token = None
        user.reset_password_expiry = None
        
        # Unlock account if it was locked due to wrong passwords
        user.failed_login_attempts = 0
        user.is_locked = False
        
        db.session.commit()
        flash("Đặt lại mật khẩu thành công! Vui lòng đăng nhập bằng mật khẩu mới.", "success")
        return redirect(url_for("auth.login"))
        
    return render_template("auth/reset_password.html", token=token)

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("customer.index"))
