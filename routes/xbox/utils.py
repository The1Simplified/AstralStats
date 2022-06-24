import asyncio
import os
import sys
import aiohttp
import platform

from xbox import *
from xbox.webapi.api.client import XboxLiveClient
from xbox.webapi.authentication.manager import AuthenticationManager
from xbox.webapi.authentication.models import OAuth2TokenResponse

if 'windows' in platform.system().lower():
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

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


async def get_user_info(xuid: str = ""):
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

        return user_friends_sorted, user_data
