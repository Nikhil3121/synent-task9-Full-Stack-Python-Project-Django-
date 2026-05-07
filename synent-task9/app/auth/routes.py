import re
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from app import db
from app.models import User

auth_bp = Blueprint("auth", __name__)

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _validate_signup(username, email, password):
    errors = []
    if not username or len(username) < 3:
        errors.append("Username must be at least 3 characters long.")
    if not EMAIL_RE.match(email or ""):
        errors.append("Please enter a valid email address.")
    if not password or len(password) < 6:
        errors.append("Password must be at least 6 characters.")
    return errors


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("notes.list_notes"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        errors = _validate_signup(username, email, password)

        if not errors:
            if User.query.filter_by(username=username).first():
                errors.append("That username is already taken.")
            if User.query.filter_by(email=email).first():
                errors.append("An account with this email already exists.")

        if errors:
            for err in errors:
                flash(err, "error")
            return render_template("auth/register.html", username=username, email=email)

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash("Account created. You can log in now.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("notes.list_notes"))

    if request.method == "POST":
        identifier = request.form.get("identifier", "").strip()
        password = request.form.get("password", "")
        remember = bool(request.form.get("remember"))

        # let users log in with either username or email
        user = User.query.filter(
            (User.username == identifier) | (User.email == identifier.lower())
        ).first()

        if user is None or not user.check_password(password):
            flash("Invalid credentials. Please try again.", "error")
            return render_template("auth/login.html", identifier=identifier)

        login_user(user, remember=remember)
        next_url = request.args.get("next")
        return redirect(next_url or url_for("notes.list_notes"))

    return render_template("auth/login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You've been logged out.", "success")
    return redirect(url_for("main.index"))
