from aiohttp import ClientResponseError
from flask import Blueprint, redirect, render_template, request, flash
from flask_login import current_user
from pydantic import ValidationError
from routes.xbox.utils import get_user_info
from __init__ import db

xbox = Blueprint('xbox', __name__)


@xbox.route("/xbox", methods=["GET", "POST"])
async def main():
    return render_template("xbox.html")


@xbox.route("/xbox/xuid/<string:xuid>", methods=["GET", "POST"])
async def xbox_user_account(xuid: str = ""):
    
    client_token = ''
    #if current_user.is_authenticated and len(current_user.xbox_token) > 1:
    #    client_token = current_user.xbox_token
    
    
    try:
        user_friends_sorted, user_data, token_refresh = await get_user_info(xuid, client_token)
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
    return render_template("xbox_user_account.html",
                           user_data=user_data,
                           user_friends_sorted=user_friends_sorted)
