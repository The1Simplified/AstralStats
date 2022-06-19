from flask import Blueprint, render_template

import os
import sys
import aiohttp

from xbox import *
from xbox.webapi.api.client import XboxLiveClient
from xbox.webapi.authentication.manager import AuthenticationManager
from xbox.webapi.authentication.models import OAuth2TokenResponse

client_id = os.environ.get("MS_CLIENT_ID")
client_secret = os.environ.get("MS_CLIENT_SECRET")

main = Blueprint('main', __name__)

@main.route("/", methods=["GET", "POST"])
async def homepage():
    return render_template("homepage.html")


@main.route("/search/<string:platform>/<string:username>", methods=["GET", "POST"])
async def saerch(platform: str = "", username: str = ""):
    async with aiohttp.ClientSession() as session:
        auth_mgr = AuthenticationManager(session, client_id, client_secret, "")
        try:
            tokens = os.environ.get("PRIMARY_SIGN_IN_TOKEN")
            auth_mgr.oauth = OAuth2TokenResponse.parse_raw(tokens)
        except FileNotFoundError:
            exit(-1)
        try:
            await auth_mgr.refresh_tokens()
        except aiohttp.ClientResponseError:
            sys.exit(-1)
        os.environ["PRIMARY_SIGN_IN_TOKEN"] = auth_mgr.oauth.json()
        xbl_client = XboxLiveClient(auth_mgr)
        xbox_search_results = await xbl_client.usersearch.get_live_search(username)

    return render_template("search.html", platform=platform, search=username, xbox_search_results=xbox_search_results)
