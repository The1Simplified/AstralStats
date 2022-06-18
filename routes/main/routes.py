from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route("/", methods=["GET", "POST"])
async def homepage():
    return render_template("homepage.html")


@main.route("/search/<string:platform>/<string:username>", methods=["GET", "POST"])
async def saerch(platform: str = "", username: str = ""):
    return render_template("search.html", platform=platform, search=username)