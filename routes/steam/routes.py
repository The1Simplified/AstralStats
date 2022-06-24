from flask import Blueprint
from routes.main.utils import render_template

steam = Blueprint('steam', __name__)


@steam.route("/steam", methods=["GET", "POST"])
async def main():
    return render_template("steam.html")


@steam.route("/steam/user/<string:username>", methods=["GET", "POST"])
async def steam_user_account():
    return render_template("steam_user_account.html")