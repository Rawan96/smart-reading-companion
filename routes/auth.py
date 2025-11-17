from flask import Blueprint, request, session, flash, redirect, url_for, render_template
from models.reader import Reader

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"].lower()
        password = request.form["password"]

        if Reader.find_by_email(email):
            flash("Email already registered!", "error")
            return redirect(url_for("auth.sign_up"))

        reader = Reader.create_user(name, email, password)
        if reader:
            session["user"] = reader.email
            flash("Account created successfully!", "success")
            return redirect(url_for("dashboard.dashboard"))
        else:
            flash("Failed to create account.", "error")

    return render_template("auth/sign_up.html")


@auth_bp.route("/sign-in", methods=["GET", "POST"])
def sign_in():
    if request.method == "POST":
        email = request.form["email"].lower()
        password = request.form["password"]

        reader = Reader.find_by_email(email)
        if reader and reader.check_password(password):
            session["user"] = reader.email
            flash(f"Welcome back, {reader.name}!", "success")
            return redirect(url_for("dashboard.dashboard"))
        else:
            flash("Invalid email or password", "error")
            return redirect(url_for("auth.sign_in"))

    return render_template("auth/sign_in.html")




@auth_bp.route("/logout")
def logout():
    session.pop("user", None)
    flash("Logged out successfully.", "info")
    return redirect(url_for("auth.sign_in"))
