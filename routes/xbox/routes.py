from __init__ import db
from aiohttp import ClientResponseError
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user
from pydantic import ValidationError
from models import User

from routes.xbox.utils import get_signin_url, get_user_info, get_user_tokens

xbox = Blueprint('xbox', __name__)


@xbox.route("/xbox", methods=["GET", "POST"])
async def main():
    return render_template("xbox.html")


@xbox.route("/xbox/xuid/<string:xuid>", methods=["GET", "POST"])
async def xbox_user_account(xuid: str = ""):
    try:
        client_token = ''
        if current_user.is_authenticated and len(current_user.xbox_token) > 1:
            client_token = current_user.xbox_token

        try:
            user_friends_sorted, user_data, token_refresh = await get_user_info(
                xuid, client_token)
            if current_user.is_authenticated and token_refresh:
                current_user.xbox_token = token_refresh
                db.session.commit()
        except ClientResponseError:
            flash("Sorry this account cannont be accessed: Error 403", 'error')
            return redirect(request.referrer)
        except ValidationError:
            flash(
                "Sorry try waiting a little before request a large account again: Error ValidationError",
                'error')
            return redirect(request.referrer)
    except:
        db.session.rollback()
    return render_template("xbox_user_account.html",
                           user_data=user_data,
                           user_friends_sorted=user_friends_sorted)


@xbox.route("/xbox/login", methods=["GET", "POST"])
async def login():
    try:
        if not current_user.is_authenticated:
            flash('Please Log In First', 'error')
            return redirect(url_for('main.homepage'))
    except:
        db.session.rollback()
    url_root = request.url_root
    return redirect(await get_signin_url() + f"{url_root}callback")


@xbox.route("/callback", methods=["GET", "POST"])
async def oauth_success():
    code = request.args.get('code', default='', type=None)
    try:
        if not current_user.is_authenticated:
            flash('Please Log In First', 'error')
            return redirect(url_for('main.homepage'))
        tokens = await get_user_tokens(code)
        user = User.query.get(int(current_user.id))
        user.xbox_token = tokens['oauth']
        db.session.commit()
        db.session.remove()
    except:
        db.session.rollback()
    return redirect(url_for('main.account'))
