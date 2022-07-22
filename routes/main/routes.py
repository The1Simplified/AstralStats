from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask_login import login_user, current_user, logout_user
from routes.main.forms import LoginForm, RegistrationForm
from routes.xbox.utils import get_user_search
from __init__ import db, bcrypt
from models import User

main = Blueprint('main', __name__)


@main.route("/", methods=["GET", "POST"])
async def homepage():
    return render_template("homepage.html")


@main.route("/search/<string:platform>/<string:username>",
            methods=["GET", "POST"])
async def saerch(platform: str = "", username: str = ""):
    platform_string = f"color:var(--provider-color-{platform})"
    xbox_search = await get_user_search(username)

    return render_template("search.html",
                           platform=platform,
                           username=username,
                           xbox_search=xbox_search,
                           platform_string=platform_string)


@main.route("/login", methods=["GET", "POST"])
async def login():
    try:
        if current_user.is_authenticated:
            return redirect(url_for('main.homepage'))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and bcrypt.check_password_hash(user.password,
                                                   form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                db.session.remove()
                return redirect(next_page) if next_page else redirect(
                    url_for('main.homepage'))
            elif not user:
                flash('There is no account with that name', 'warning')
            else:
                flash('Username and Password do not match', 'warning')
    except:
        flash('A database error ocurred', 'error')
        db.session.rollback()
    return render_template('login.html', title='Login', form=form)


@main.route("/logout", methods=["GET", "POST"])
async def logout():
    try:
        logout_user()
    except:
        db.session.rollback()
    return redirect(url_for('main.homepage'))


@main.route("/register", methods=["GET", "POST"])
async def register():
    try:
        if current_user.is_authenticated:
            return redirect(url_for('main.homepage'))
        form = RegistrationForm()
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(
                form.password.data).decode('utf-8')
            user = User(username=form.username.data,
                        email=form.email.data,
                        password=hashed_password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.login'))
    except:
        db.session.rollback()
    return render_template('register.html', title='Register', form=form)


@main.route("/account", methods=["GET", "POST"])
async def account():
    try:
        if not current_user.is_authenticated:
            flash('Please Log In First', 'error')
            return redirect(url_for('main.homepage'))
    except:
        db.session.rollback()
    return render_template('account.html', title='Account')