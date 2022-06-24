from aiohttp import ClientResponseError
from flask import Blueprint, redirect, render_template, request, flash
from pydantic import ValidationError
from routes.xbox.utils import get_user_info

xbox = Blueprint('xbox', __name__)


@xbox.route("/xbox", methods=["GET", "POST"])
async def main():
    return render_template("xbox.html")


@xbox.route("/xbox/xuid/<string:xuid>", methods=["GET", "POST"])
async def xbox_user_account(xuid: str = ""):
    try:
        user_friends_sorted, user_data = await get_user_info(xuid)
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
