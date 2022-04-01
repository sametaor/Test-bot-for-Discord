import os
import nextcord
from nextcord.ext import ipc
from dotenv import load_dotenv
from quart import Quart, render_template, redirect, url_for
from quart_discord import DiscordOAuth2Session, requires_authorization, Unauthorized

load_dotenv("token.env")
app = Quart(__name__)
app.secret_key = b'something'
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"

app.config["DISCORD_CLIENT_ID"] = 839532962600714280
app.config["DISCORD_CLIENT_SECRET"] = os.getenv("SECRET")
app.config["DISCORD_REDIRECT_URI"] = "http://127.0.0.1:5000/callback"
app.config["DISCORD_BOT_TOKEN"] = os.getenv("TOKEN")

discord = DiscordOAuth2Session(app)

@app.route("/login/")
async def login():
    return await discord.create_session()

@app.route("/callback/")
async def callback():
    try:
        await discord.callback()
    except:
        return redirect(url_for("login"))
    return redirect(url_for("dashboard"))

@app.route("/")
async def index():
    return await render_template("index.html")

@app.route("/dashboard/")
async def dashboard():
    user = await discord.fetch_user()
    return await render_template("dashboard.html", user=user)

if __name__ == "__main__":
    app.run(debug=True)