import asyncio
import os
import pathlib
import string
import sys

from aiohttp import ClientResponseError, ClientSession
from flask import Flask, flash, render_template, redirect, url_for, request
from pydantic import ValidationError
from xbox import *
from xbox.webapi.api.client import XboxLiveClient
from xbox.webapi.authentication.manager import AuthenticationManager
from xbox.webapi.authentication.models import OAuth2TokenResponse

app = Flask(__name__)

client_id = os.getenv('MS_CLIENT_ID')
client_secret = os.getenv('MS_CLIENT_SECRET')
tokens_file = (str(pathlib.Path(__file__).parent.resolve()) + (f"\\tokens.json"))

#client_id = '640c09c8-8f82-47a3-aa70-6ab8441acfb4'
#client_secret = 'rF38Q~P64OssW3ZH1AnXr4l4zcxW_jOn1hr1Icr7' # 77e7672b-fb15-4bea-8f6f-936a5e16f179
#tokens_file = "C:/Users/Marcus/AppData/Local/OpenXbox/xbox/tokens.json"

@app.route('/', methods=['GET', 'POST'])
@app.route('/<string:gamertag>', methods=['GET', 'POST'])
async def homepage(gamertag: string = ""):
    async with ClientSession() as session:
        auth_mgr = AuthenticationManager(session, client_id, client_secret, "")
        try:
            with open(tokens_file, mode="r") as f:
                tokens = f.read()
            auth_mgr.oauth = OAuth2TokenResponse.parse_raw(tokens)
        except FileNotFoundError:
            exit(-1)
        try:
            await auth_mgr.refresh_tokens()
        except ClientResponseError:
            sys.exit(-1)
        with open(tokens_file, mode="w") as f:
            f.write(auth_mgr.oauth.json())
        xbl_client = XboxLiveClient(auth_mgr)
        if request.method == 'POST':
            gamertag = request.form['gamertag']
        if gamertag:
            try:
                xbl_profile = await xbl_client.profile.get_profile_by_gamertag(gamertag)
                friends_raw = await xbl_client.people.get_friends_by_xuid(xbl_profile.profile_users[0].id)
                friends_sorted = sorted(friends_raw.people, key=lambda d: d.presence_state)
                #parsed_profile = parse_profile(xbl_profile)
                
                friends_invert_sorted = friends_sorted[::-1]
                flag = False
                for i in friends_invert_sorted:
                    friends_of_friends = await xbl_client.people.get_friends_by_xuid(i.xuid)
                    for x in friends_of_friends.people:
                        if x.gamertag == gamertag:
                            flag = True
                            profile = x
                            break
                    if flag:
                        break

            except ClientResponseError:
                return render_template('profile_not_found.html', title='Home')
            except ValidationError or RuntimeError:
                flash("Please wait a little beofore searching again, our server is doo doo :)", 'success')
                return redirect(url_for('homepage'))
            return render_template('homepage.html', title=f'User: {gamertag}', profile=x, friends=friends_sorted)
        
    return render_template('homepage.html', title='Home')

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")
