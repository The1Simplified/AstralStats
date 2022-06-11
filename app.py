from waitress import serve

from flask import Flask, render_template, redirect, url_for, session
from flask_session import Session

app = Flask(__name__)
Session(app)

@app.route("/", methods=["GET", "POST"])
async def homepage():
    return render_template("homepage.html")

@app.route("/xbox", methods=["GET", "POST"])
async def xbox():
    return render_template("xbox.html")

@app.route("/xbox/user/<string:gamertag>", methods=["GET", "POST"])
async def xbox_user_account():
    return render_template("xbox.html")

@app.route("/playstation", methods=["GET", "POST"])
async def playstation():
    return render_template("playstation.html")

@app.route("/playstation/user/<string:gamertag>", methods=["GET", "POST"])
async def playstation_user_account():
    return render_template("playstation.html")

@app.route("/steam", methods=["GET", "POST"])
async def steam():
    return render_template("steam.html")

@app.route("/steam/user/<string:gamertag>", methods=["GET", "POST"])
async def steam_user_account():
    return render_template("steam.html")

if __name__ == "__main__":
    # app.run(host="localhost", port=5000)  # Dev
    serve(app, host="0.0.0.0", port=5000) # Production
