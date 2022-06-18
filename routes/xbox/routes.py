from flask import Blueprint, render_template

xbox = Blueprint('xbox', __name__)


@xbox.route("/xbox", methods=["GET", "POST"])
async def main():
    return render_template("xbox.html")


@xbox.route("/xbox/user/<string:username>", methods=["GET", "POST"])
async def xbox_user_account():
    return render_template("xbox_user_account.html")