import asyncio
import os
import sys
import aiohttp

from xbox import *
from xbox.webapi.api.client import XboxLiveClient
from xbox.webapi.authentication.manager import AuthenticationManager
from xbox.webapi.authentication.models import OAuth2TokenResponse

try:
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
except AttributeError:
    pass

client_id = os.environ.get("MS_CLIENT_ID")
client_secret = os.environ.get("MS_CLIENT_SECRET")


async def get_user_search(username: str = ""):
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
        xbox_search = await xbl_client.usersearch.get_live_search(username)

        return xbox_search


async def get_user_info(xuid: str = "", client_token: str = ""):
    async with aiohttp.ClientSession() as session:
        auth_mgr = AuthenticationManager(session, client_id, client_secret, "")

        try:
            if len(client_token) < 1:
                tokens = os.environ.get("PRIMARY_SIGN_IN_TOKEN")
            else:
                tokens = client_token
            auth_mgr.oauth = OAuth2TokenResponse.parse_raw(tokens)
        except FileNotFoundError:
            exit(-1)

        try:
            await auth_mgr.refresh_tokens()
        except aiohttp.ClientResponseError:
            sys.exit(-1)

        token_refresh = ''
        if len(client_token) < 1:
            os.environ["PRIMARY_SIGN_IN_TOKEN"] = auth_mgr.oauth.json()
        else:
            token_refresh = auth_mgr.oauth.json()

        xbl_client = XboxLiveClient(auth_mgr)
        friends_raw = await xbl_client.people.get_friends_by_xuid(xuid)
        friends_invert_sorted = sorted(friends_raw.people,
                                       key=lambda d: d.presence_state)

        user_friends_sorted = friends_invert_sorted[::-1]
        flag = False
        for i in friends_invert_sorted:
            friends_of_friends = await xbl_client.people.get_friends_by_xuid(
                i.xuid)
            for x in friends_of_friends.people:
                if x.xuid == xuid:
                    flag = True
                    user_data = x
                    break
            if flag:
                break

        return user_friends_sorted, user_data, token_refresh


async def get_signin_url():
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
        auth_url = auth_mgr.generate_authorization_url()

        return auth_url


async def get_user_tokens(code):
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

        auth_mgr.request_tokens(code)

        oauth = await auth_mgr.refresh_oauth_token()
        user_token = await auth_mgr.request_user_token()
        xsts_token = await auth_mgr.request_xsts_token()

        tokens = {
            'oauth': str(oauth),
            'user_token': str(user_token),
            'xsts_token': str(xsts_token)
        }

        return tokens
