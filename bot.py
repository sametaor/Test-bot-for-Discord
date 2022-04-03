import nextcord
import asyncio
import json
import urllib
import os
import requests
import random
import aiosqlite
from dotenv import load_dotenv
from Cogsforbot.Twentyfortyeight.Events import Events
from nextcord.ext import commands, tasks, ipc
from texttoowo import text_to_owo
from redditmeme import reddit
from itertools import cycle
from weatherassets import *
from eightballresponses import outputs


async def getprefix(testbot, message):
    async with aiosqlite.connect("prefixes.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute('SELECT prefix FROM prefixes WHERE guild = ?', (message.guild.id,))
            data = await cursor.fetchone()
            if data:
                return data
            else:
                return "&"



class tachyonBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ipc = ipc.Server(self, secret_key="tachyonfirst")
    
    async def on_ipc_read(self):
        print("IPC is ready!")
    
    async def on_ipc_error(self, endpoint, error):
        print(endpoint, "raised", error)
    
    async def on_ready(self):
        print("Ready!")



testbot = tachyonBot(command_prefix="&", intents=nextcord.Intents.all())
testbot.remove_command("help")

load_dotenv('token.env')

status = cycle([
    'nextcord.py',
    '&help',
    'Snake',
    'Tictactoe',
    'Chess',
    'Connect-4',
    '[insert your favourite game here]',
    'When game',
    'Gamez on your phone',
    '↑↑↓↓←→←→BA Start',
    'Amogus',
    'Songs'
])

@tasks.loop(seconds=10)
async def status_swap():
    await testbot.change_presence(activity=nextcord.Game(next(status)))


@testbot.event
async def on_ready():
    print("Tachyon ready to roll")
    status_swap.start()
    async with aiosqlite.connect("prefixes.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute('CREATE TABLE IF NOT EXISTS prefixes (prefix TEXT, guild ID)')
        await db.commit()
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER , guild INTEGER)')
        await db.commit()

testbot.event(Events(testbot).on_reaction_add)


@testbot.event
async def on_member_join(member):
    channel = nextcord.utils.get(member.guild.channels, name='welcome')
    await channel.send(f"Hello there {member.mention}! A warm welcome to you for joining {member.guild.name}!")


@testbot.event
async def on_member_remove(member):
    channel = nextcord.utils.get(member.guild.channels, name='welcome')
    await channel.send(f"We will miss you, {member.mention}!")


@testbot.event
async def on_guild_join(guild):
    async with aiosqlite.connect("prefixes.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute('INSERT INTO prefixes (prefix, guild) VALUES (?, ?)', ('&', guild.id,))
        await db.commit()


@testbot.event
async def on_guild_leave(guild):
    async with aiosqlite.connect("prefixes.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute('SELECT prefix FROM prefixes WHERE guild = ?', (guild.id,))
            data = await cursor.fetchone()
            if data:
                await cursor.execute('DELETE FROM prefixes WHERE guild = ?', (guild.id,))
        await db.commit()


@testbot.event
async def on_message(msg):
    if msg.author != testbot.user and msg.content.startswith('&weather'):
        if len((msg.content.replace('&weather ', ''))) >= 1:
            location = msg.content.replace('&weather ', '')
            url = 'http://api.openweathermap.org/data/2.5/weather?q=' + location + '&appid=' + os.getenv('WEATHER_API_KEY') + '&units=metric'
            try:
                data = parse_data(json.loads(requests.get(url).content)['main'])
                await msg.channel.send(embed=weathermsg(data, location))
            except KeyError:
                await msg.channel.send(embed=error_message())

@testbot.event
async def on_command_error(ctx,error):
    if isinstance(error,commands.MissingPermissions):
        await ctx.send(embed=nextcord.Embed(title="You are missing the following required permissions to do that: ", description=f'\n'.join(f"{(perm)}".title() for perm in error.missing_permissions if perm).replace("_", " ")))
    elif isinstance(error,commands.CommandNotFound):
        if ctx.message.content.startswith("&weather"):
            pass
        elif ctx.message.content.startswith("&bsstart"):
            pass
        elif ctx.message.content.startswith("&bsplace"):
            pass
        elif ctx.message.content.startswith("&bsattack"):
            pass
        elif ctx.message.content.startswith("&bsquit"):
            pass
        else:
            await ctx.send("That command does not exist")
    elif isinstance(error,commands.MissingRequiredArgument):
        await ctx.send(f"You are missing a required argument: `{error.param}`")
    elif isinstance(error,commands.BadArgument):
        await ctx.send("Please enter the correct arguments")
    elif isinstance(error,commands.BotMissingPermissions):
        await ctx.send("I don't have the required permissions to perform that")
    elif isinstance(error,commands.CommandOnCooldown):
        await ctx.send(f"This command is still on cooldown for `{round(error.retry_after, 1)}`")
    elif isinstance(error,commands.TooManyArguments):
        await ctx.send("You have sent too many arguments, please send the specified number of arguments only")
    elif isinstance(error,commands.MissingAnyRole):
        await ctx.send("You don't have the required set of roles")
    elif isinstance(error,commands.BotMissingAnyRole):
        await ctx.send("I don't have the required set of roles for performing that")
    elif isinstance(error, commands.DisabledCommand):
        await ctx.send("This command has been disabled.")
        return
    else:
        raise error


@testbot.event
async def cog_command_error(ctx,error):
    if isinstance(error,commands.MissingPermissions):
        await ctx.send(embed=nextcord.Embed(title="You are missing the following required permissions to do that: ", description=f'\n'.join(f"{(perm)}".title() for perm in error.missing_permissions if perm).replace("_", " ")))
    elif isinstance(error,commands.CommandNotFound):
        await ctx.send("That command does not exist")
    elif isinstance(error,commands.MissingRequiredArgument):
        await ctx.send(f"You are missing a required argument: `{error.param}`")
    elif isinstance(error,commands.BadArgument):
        await ctx.send("Please enter the correct arguments")
    elif isinstance(error,commands.BotMissingPermissions):
        await ctx.send("I don't have the required permissions to perform that")
    elif isinstance(error,commands.CommandOnCooldown):
        await ctx.send(f"This command is still on cooldown for `{round(error.retry_after, 1)}`")
    elif isinstance(error,commands.TooManyArguments):
        await ctx.send("You have sent too many arguments, please send the specified number of arguments only")
    elif isinstance(error,commands.MissingAnyRole):
        await ctx.send("You don't have the required set of roles")
    elif isinstance(error,commands.BotMissingAnyRole):
        await ctx.send("I don't have the required set of roles for performing that")
    elif isinstance(error, commands.DisabledCommand):
        await ctx.send("This command has been disabled.")
        return
    else:
        raise error

@testbot.command(aliases=['8ball'])
async def eightball(ctx, *, question):
    await ctx.send(f':8ball: {random.choice(outputs)}')

@testbot.command()
async def meme(ctx):
    memeApi = urllib.request.urlopen('https://meme-api.herokuapp.com/gimme')
    memeData = json.load(memeApi)
    memeUrl = memeData['url']
    memeName = memeData['title']
    memeOP = memeData['author']
    memeSub = memeData['subreddit']
    memeLink = memeData['postLink']

    em = nextcord.Embed(title=memeName, url=memeLink, description=f"u/{memeOP}", colour=nextcord.Colour.random())
    em.set_image(url=memeUrl)
    em.set_footer(text=f"r/{memeSub}")
    await ctx.send(embed=em)

@testbot.command()
async def formuladank(ctx, f1meme="formuladank"):
    subreddit = reddit.subreddit(f1meme)
    all_subs = []

    hot = subreddit.hot(limit = 100)

    for submission in hot:
        all_subs.append(submission)

    random_sub = random.choice(all_subs)

    name = random_sub.title
    posturl = random_sub.permalink
    url = random_sub.url
    subredditname = random_sub.subreddit
    subredditicon = random_sub.subreddit.icon_img

    em = nextcord.Embed(title=name, url=f"https://www.reddit.com{posturl}")
    em.set_image(url=url)
    em.set_footer(icon_url=subredditicon, text=f"r/{subredditname}")

    await ctx.send(embed=em)

@testbot.command(aliases=["owo"])
async def owofy(ctx):
    c = ctx.message.content
    if ctx.message.content.startswith('&owofy'):
        c = c.replace('&owofy', '', 1)
    elif ctx.message.content.startswith('&owo'):
        c = c.replace('&owo', '', 1)
    await ctx.send(text_to_owo(c))

def check(message):
    try:
        int(message.content)
        return True
    except ValueError:
        return False

@testbot.command()
async def guess(context):
    await context.send('Pick a number between 1 and 10')
    number = random.randint(1,10)
    for guess in range(1,4):
        msg = await testbot.wait_for('message', check=check)
        attempt = int(msg.content)
        if attempt > number:
            await context.send(str(guess) + ' guesses used...')
            await asyncio.sleep(1)
            await context.send('Try going lower')
            await asyncio.sleep(1)
        elif attempt < number:
            await context.send(str(guess) + ' guesses used...')
            await asyncio.sleep(1)
            await context.send('Try going higher')
            await asyncio.sleep(1)
        else:
            await context.send('You guessed the number! You won!')
            break
    else:
        await context.send(f"You didn't get it. The correct number was {number}. Better luck next time!")

@testbot.command(aliases=["dice", "diceroll", "rd"])
async def rolldice(ctx):
    n = random.randrange(1, 7)
    await ctx.send(f"{n}🎲")

@testbot.command()
async def coinflip(ctx):
    choices = ["Heads", "Tails"]
    coin = random.choice(choices)
    await ctx.send(f"{coin}:coin:")

@testbot.command()
async def adduser(ctx, member: nextcord.Member):
    member = ctx.author
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute('SELECT id FROM users WHERE guild = ?', (ctx.guild.id,))
            data = await cursor.fetchone()
            if data:
                await cursor.execute('UPDATE users SET id = ? WHERE guild = ?', (member.id, ctx.guild.id,))
            else:
                await cursor.execute('INSERT INTO users (id, guild) VALUES (?, ?)', (member.id, ctx.guild.id,))
        await db.commit()

@testbot.command()
async def removeuser(ctx, member: nextcord.Member):
    member = ctx.author
    async with aiosqlite.connect("main.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute('SELECT id FROM users WHERE guild = ?', (ctx.guild.id,))
            data = await cursor.fetchone()
            if data:
                await cursor.execute('DELETE FROM users WHERE id = ? AND guild = ?', (member.id, ctx.guild.id,))
    await db.commit()

@testbot.command()
async def setprefix(ctx, *, prefix=None):
    if prefix is None:
        return
    
    async with aiosqlite.connect("prefixes.db") as db:
        async with db.cusror() as cursor:
            await cursor.execute('SELECT prefix FROM prefixes WHERE guild = ?', (ctx.guild.id,))
            data = await cursor.fetchone()
            if data:
                await cursor.execute('UPDATE prefixes set prefix = ? WHERE guild = ?', (prefix, ctx.guild.id,))
                await ctx.send(f'Updated prefix to `{prefix}`')
            else:
                await cursor.execute('INSERT INTO prefixes (prefix, guild) VALUES (?, ?)', ('&', ctx.guild.id,))
                if data:
                    await cursor.execute('UPDATE prefixes set prefix = ? WHERE guild = ?', (prefix, ctx.guild.id,))
                    await ctx.send(f'Updated prefix to `{prefix}`')
                else:
                    return
        await db.commit()

for folder in os.listdir("Cogsforbot"):
    if os.path.exists(os.path.join("Cogsforbot", folder, "cog.py")):
        testbot.load_extension(f"Cogsforbot.{folder}.cog")

@testbot.ipc.route()
async def get_guild_count(data):
    return len(testbot.guilds)

@testbot.ipc.route()
async def get_guild_ids(data):
    final = []
    for guild in testbot.guilds:
        final.append(guild.id)
    return final

@testbot.ipc.route()
async def get_guild(data):
    guild = testbot.get_guild(data.guild_id)
    if guild is None:
        return None
    
    guild_data = {
        "name" : guild.name,
        "id" : guild.id,
        "prefix" : "&"
    }
    return guild_data

testbot.ipc.start()

DISCORD_TOKEN = os.getenv("TOKEN")
try:
    testbot.run(DISCORD_TOKEN)
except:
    if testbot.is_ws_ratelimited == True:
        print("The bot is ratelimited currently, please wait for the ratelimit to be removed after a few hours")