import nextcord
import asyncio
import aiohttp
import json
import urllib
import os
import time
import nextcord.ext.commands as commands
import nextcord.ext.tasks as tasks
from io import BytesIO
from nextcord.enums import ChannelType
from dotenv import load_dotenv
from Cogsforbot.Twentyfortyeight.Events import Events
import requests
import random
import datetime
from nextcord import Member, Spotify
from typing import Optional
from texttoowo import text_to_owo
from itertools import cycle
from weatherassets import *
from eightballresponses import outputs


testbot = commands.Bot(command_prefix="&", intents=nextcord.Intents.all())
testbot.remove_command("help")

load_dotenv('token.env')
Button = nextcord.ui.Button
ButtonStyle = nextcord.ButtonStyle

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
    'Songs',
    'Battleship'
])


@tasks.loop(seconds=10)
async def status_swap():
    await testbot.change_presence(activity=nextcord.Game(next(status)))


@testbot.event
async def on_ready():
    print("Test bot ready to go")
    status_swap.start()

testbot.event(Events(testbot).on_reaction_add)


@testbot.event
async def on_member_join(member):
    channel = nextcord.utils.get(member.guild.channels, name='welcome')
    await channel.send(f"Hello there, {member.mention}! A warm welcome to you for joining {member.guild.name}!")


@testbot.event
async def on_member_remove(member):
    channel = nextcord.utils.get(member.guild.channels, name='welcome')
    await channel.send(f"We will miss you, {member.mention}!")


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
        elif ctx.message.content.startswith("&gsearch"):
            pass
        elif ctx.message.content.startswith("&gimgsearch"):
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

@testbot.command(aliases=["owo"])
async def owofy(ctx):
    c = ctx.message.content
    if ctx.message.content.startswith('&owofy'):
        c = c.replace('&owofy', '', 1)
    elif ctx.message.content.startswith('&owo'):
        c = c.replace('&owo', '', 1)
    await ctx.message.delete()
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
    diceembed = nextcord.Embed(title="🎲 Roll the Dice 🎲", description=f"{n}🎲", colour=nextcord.Colour.brand_green(), timestamp=ctx.message.created_at)
    await ctx.send(embed=diceembed)

@testbot.command()
async def coinflip(ctx):
    choices = ["Heads", "Tails"]
    coin = random.choice(choices)
    coinembed=nextcord.Embed(title=":coin: Coin Flip :coin:", description=f"{coin}:coin:", colour=nextcord.Colour.gold(), timestamp=ctx.message.created_at)
    await ctx.send(embed=coinembed)

for folder in os.listdir("Cogsforbot"):
    if os.path.exists(os.path.join("Cogsforbot", folder, "cog.py")):
        testbot.load_extension(f"Cogsforbot.{folder}.cog")

DISCORD_TOKEN = os.getenv("TOKEN")
try:
    testbot.run(DISCORD_TOKEN)
except:
    if testbot.is_ws_ratelimited == True:
        print("The bot is ratelimited currently, please wait for the ratelimit to be removed after a few hours")
