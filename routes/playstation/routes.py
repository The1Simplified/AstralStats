from flask import Blueprint
from routes.main.utils import render_template

playstation = Blueprint('playstation', __name__)


@playstation.route("/playstation", methods=["GET", "POST"])
async def main():
    return render_template("playstation.html")


@playstation.route("/playstation/user/<string:username>",
                   methods=["GET", "POST"])
async def playstation_user_account():
    return render_template("playstation_user_account.html")