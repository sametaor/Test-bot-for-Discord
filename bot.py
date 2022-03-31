import nextcord
import asyncio
import aiohttp
import json
import urllib
import os
import time
from io import BytesIO
from nextcord.enums import ChannelType
from dotenv import load_dotenv
from Cogsforbot.Twentyfortyeight.Events import Events
import requests
import random
import datetime
from nextcord import Member, Spotify
from typing import Optional
from nextcord.ext import commands, tasks
from texttoowo import text_to_owo
from redditmeme import reddit
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
    'Songs'
])
EMOJIS_TO_USE_FOR_CALCULATOR = {"1":"1️⃣", "2":"2️⃣", "3":"3️⃣", "4":"4️⃣", "5":"5️⃣", "6":"6️⃣", "7":"7️⃣", "8":"8️⃣", "9":"9️⃣", "0":"0️⃣", "+":"➕", "-":"➖","x":"✖️","÷":"➗",".":"▫"}
buttons = [
    [
        Button(style=ButtonStyle.grey, label='1'),
        Button(style=ButtonStyle.grey, label='2'),
        Button(style=ButtonStyle.grey, label='3'),
        Button(style=ButtonStyle.blurple, label='x'),
        Button(style=ButtonStyle.red, label='Exit')
    ],
    [
        Button(style=ButtonStyle.grey, label='4'),
        Button(style=ButtonStyle.grey, label='5'),
        Button(style=ButtonStyle.grey, label='6'),
        Button(style=ButtonStyle.blurple, label='÷'),
        Button(style=ButtonStyle.red, label='←')
    ],
    [
        Button(style=ButtonStyle.grey, label='7'),
        Button(style=ButtonStyle.grey, label='8'),
        Button(style=ButtonStyle.grey, label='9'),
        Button(style=ButtonStyle.blurple, label='+'),
        Button(style=ButtonStyle.red, label='Clear')
    ],
    [
        Button(style=ButtonStyle.grey, label='00'),
        Button(style=ButtonStyle.grey, label='0'),
        Button(style=ButtonStyle.grey, label='.'),
        Button(style=ButtonStyle.blurple, label='-'),
        Button(style=ButtonStyle.green, label='=')
    ],
]

disabled_buttons = [
    [
        Button(style=ButtonStyle.grey, label='1', disabled=True),
        Button(style=ButtonStyle.grey, label='2', disabled=True),
        Button(style=ButtonStyle.grey, label='3', disabled=True),
        Button(style=ButtonStyle.blurple, label='x', disabled=True),
        Button(style=ButtonStyle.red, label='Exit', disabled=True)
    ],
    [
        Button(style=ButtonStyle.grey, label='4', disabled=True),
        Button(style=ButtonStyle.grey, label='5', disabled=True),
        Button(style=ButtonStyle.grey, label='6', disabled=True),
        Button(style=ButtonStyle.blurple, label='÷', disabled=True),
        Button(style=ButtonStyle.red, label='←', disabled=True)
    ],
    [
        Button(style=ButtonStyle.grey, label='7', disabled=True),
        Button(style=ButtonStyle.grey, label='8', disabled=True),
        Button(style=ButtonStyle.grey, label='9', disabled=True),
        Button(style=ButtonStyle.blurple, label='+', disabled=True),
        Button(style=ButtonStyle.red, label='Clear', disabled=True)
    ],
    [
        Button(style=ButtonStyle.grey, label='00', disabled=True),
        Button(style=ButtonStyle.grey, label='0', disabled=True),
        Button(style=ButtonStyle.grey, label='.', disabled=True),
        Button(style=ButtonStyle.blurple, label='-', disabled=True),
        Button(style=ButtonStyle.green, label='=', disabled=True)
    ],
]

def calculator(exp):
    o = exp.replace('x', '*')
    o = o.replace('÷', '/')
    result = ''
    try:
        result = str(eval(o))
    except:
        result = 'An error occured'
    return result

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
    await channel.send(f"Hello there {member.mention}! A warm welcome to you for joining {member.guild.name}!")


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
        await ctx.send(embed=nextcord.Embed(title="You are missing the following required permissions to do that: ", description='\n'.join(error.missing_permissions)))
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

for folder in os.listdir("Cogsforbot"):
    if os.path.exists(os.path.join("Cogsforbot", folder, "cog.py")):
        testbot.load_extension(f"Cogsforbot.{folder}.cog")

DISCORD_TOKEN = os.getenv("TOKEN")
try:
    testbot.run(DISCORD_TOKEN)
except:
    if testbot.is_ws_ratelimited == True:
        print("The bot is ratelimited currently, please wait for the ratelimit to be removed after a few hours")