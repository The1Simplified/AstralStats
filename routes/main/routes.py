from flask import Blueprint, render_template

from routes.xbox.utils import get_user_search

main = Blueprint('main', __name__)

@main.route("/", methods=["GET", "POST"])
async def homepage():
    return render_template("homepage.html")


@main.route("/search/<string:platform>/<string:username>", methods=["GET", "POST"])
async def saerch(platform: str = "", username: str = ""):
    platform_string = f"color:var(--provider-color-{platform})"
    xbox_search = await get_user_search(username)

    return render_template("search.html", platform=platform, username=username, xbox_search=xbox_search, platform_string=platform_string)
