from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from . import auth_bp
from models import get_user, add_user
from user import User


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        firstname = request.form["firstname"]
        lastname = request.form["lastname"]
        username = request.form["username"]
        password = request.form["password"]
        role_id = request.form["role_id"]
        if get_user(username):
            flash("Username already exists")
            return redirect(url_for("auth.register"))
        add_user(firstname, lastname, username, password, role_id)
        flash("Registration successful! Please log in.")
        return redirect(url_for("auth.login"))
    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user_data = get_user(username)
        if user_data and check_password_hash(user_data[4], password):
            user = User(
                id=user_data[0],
                firstname=user_data[1],
                lastname=user_data[2],
                username=user_data[3],
                password=user_data[4],
                role_id=user_data[5],
            )
            login_user(user)
            return redirect(url_for("dashboard.dashboard"))
        flash("Invalid username or password")
    return render_template("login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("auth.login"))
