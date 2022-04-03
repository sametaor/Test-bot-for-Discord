import os
import nextcord
import aiosqlite
from nextcord.ext import ipc
from dotenv import load_dotenv
from quart import Quart, render_template, redirect, url_for, request
from quart_discord import DiscordOAuth2Session, requires_authorization, Unauthorized

load_dotenv("token.env")

app = Quart(__name__)
app.secret_key = "dababa362"
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "false"

app.config["DISCORD_CLIENT_ID"] = 839532962600714280
app.config["DISCORD_CLIENT_SECRET"] = os.getenv("SECRET")
app.config["DISCORD_REDIRECT_URI"] = "http://0.0.0.0:$PORT/callback"
app.config["DISCORD_BOT_TOKEN"] = os.getenv("TOKEN")

discord = DiscordOAuth2Session(app)

ipcClient = ipc.Client(secret_key="tachyonfirst")

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
    guildCount = await ipcClient.request("get_guild_count")
    guildIds = await ipcClient.request("get_guild_ids")
    try:
        userGuilds = await discord.fetch_guilds()
    except:
        return await redirect(url_for("login"))
    
    guilds = []
    for guild in userGuilds:
        if guild.permissions.manage_guild:
            guild.classColor = "greenBorder" if guild.id in guildIds else "redBorder"
            guilds.append(guild)
    
    guilds.sort(key=lambda x: x.classColor == "redBorder")
    
    return await render_template("dashboard.html", user=user, guildCount=guildCount, guilds=guilds)

@app.route("/dashboard/<int:guild_id>")
async def dashboardServer(guild_id):
    if not await discord.authorized:
        return redirect(url_for("login"))
    
    guild = await ipcClient.request("get_guild", guild_id=guild_id)
    if guild is None:
        return redirect(f'https://discord.com/oauth2/authorize?&client_id={app.config["DISCORD_CLIENT_ID"]}&scope=bot&permissions=8&guild_id={guild_id}&response_type=code&redirect_uri={app.config["DISCORD_REDIRECT_URI"]}')
    return await render_template("server.html", guildName= guild["name"], guild=guild, guildID=guild_id)

@app.route("/dashboard/<int:guild_id>/", methods=["POST"])
async def dashboardServerPOST(guild_id):
    if not await discord.authorized:
        return redirect(url_for("login"))
    
    guild = await ipcClient.request("get_guild", guild_id=guild_id)
    if guild is None:
        return redirect(f'https://discord.com/oauth2/authorize?&client_id={app.config["DISCORD_CLIENT_ID"]}&scope=bot&permissions=8&guild_id={guild_id}&response_type=code&redirect_uri={app.config["DISCORD_REDIRECT_URI"]}')
    
    newPrefix = await request.get_json()
    newPrefix = newPrefix["setPrefix"]
    
    async with aiosqlite.connect("prefixes.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute('SELECT prefix FROM prefixes WHERE guild = ?', (guild_id,))
            data = await cursor.fetchone()
            if data:
                await cursor.execute('UPDATE prefixes SET prefix = ? WHERE guild = ?', (newPrefix, guild_id,))
            else:
                await cursor.execute('INSERT INTO prefixes (prefix, guild) VALUES (? ,?)', (newPrefix, guild_id,))
        await db.commit()
            
    
    return await render_template("server.html", guildName= guild["name"], guild=guild, guildID = guild_id)
    
if __name__ == "__main__":
    app.run(debug=True)