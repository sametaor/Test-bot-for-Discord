from re import IGNORECASE
from discord.ext.commands.errors import CommandNotFound
from weatherassets import error_message, parse_data, weathermsg
import discord
from discord.ext import commands
import asyncio
import json
import requests
from discordtoken import discord_token, api_key
import random
import praw
from texttoowo import text_to_owo
from redditmeme import reddit
from tictactoe import winningConditions, player1, player2, turn, gameOver, board
from weatherassets import *


testbot = commands.Bot(command_prefix="$")

filtered_words = ["fuck", "bullshit"]

@testbot.event
async def on_ready():
    print("Test bot ready to go")
    await testbot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='$help'))


@testbot.event
async def on_message(msg):
    for word in filtered_words:
        if word in msg.content:
            await msg.delete()

    await testbot.process_commands(msg)
    try:
        if msg.author != testbot.user and msg.content.startswith('$weather'):
            if len((msg.content.replace('$weather', ''))) >= 1:
                location = msg.content.replace('$weather ', '')
                url = f'http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric'
                try:
                    data = parse_data(json.loads(requests.get(url).content)['main'])
                    await msg.channel.send(embed=weathermsg(data, location))
                except KeyError:
                    await msg.channel.send(embed=error_message(location))
    except CommandNotFound:
        pass


@testbot.event
async def on_command_error(ctx,error):
    if isinstance(error,commands.MissingPermissions):
        await ctx.send("You are missing the required permissions to do that.")
    elif isinstance(error,commands.CommandInvokeError):
        await ctx.send("Message cannot be empty")
    elif isinstance(error,commands.CommandNotFound):
        pass
    elif isinstance(error,commands.MissingRequiredArgument):
        await ctx.send("Please enter the required arguments")
    else:
        raise error


@testbot.event
async def on_raw_reaction_add(payload):
    rolereactionID = 842021454279475220

    if rolereactionID ==payload.message_id:
        member = payload.member
        guild = member.guild

        emoji = payload.emoji.name
        if emoji == '🍎':
            role = discord.utils.get(guild.roles, name="Apple")
        elif emoji == '🥭':
            role = discord.utils.get(guild.roles, name="Mango")
        elif emoji == '🍇':
            role = discord.utils.get(guild.roles, name="Grapes")
        elif emoji == '🍐':
            role = discord.utils.get(guild.roles, name="Pear")
        await member.add_roles(role)

@testbot.event
async def on_raw_reaction_remove(payload):
    rolereactionID = 842021454279475220

    if rolereactionID ==payload.message_id:
        guild = await(testbot.fetch_guild(payload.guild_id))

        emoji = payload.emoji.name
        if emoji == '🍎':
            role = discord.utils.get(guild.roles, name="Apple")
        elif emoji == '🥭':
            role = discord.utils.get(guild.roles, name="Mango")
        elif emoji == '🍇':
            role = discord.utils.get(guild.roles, name="Grapes")
        elif emoji == '🍐':
            role = discord.utils.get(guild.roles, name="Pear")
        member = await(guild.fetch_member(payload.user_id))
        if member is not None:
            await member.remove_roles(role)
        else:
            print("Member not found")


@testbot.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount=2):
    await ctx.channel.purge(limit=amount)

@testbot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member,*, reason="No reason provided"):
    try:
        await member.send(f"You have been kicked from{ctx.guild.name} for the following reason: " + reason)
    except:
        await ctx.send("The member has their DMs closed.")
    await member.kick(reason=reason)

@testbot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, reason="No reason provided"):
    await member.send(f"You have been banned from {ctx.guild.name} for the following reason: " + reason)
    await ctx.send(member.name + " has been banned from {ctx.guild.name} for the following reason: " + reason)
    await member.ban(reason=reason)

@testbot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx,*,member):
    banned_users = await ctx.guild.bans()
    member_name, member_desc = member.split('#')
    for banned_entry in banned_users:
        user = banned_entry.user

        if(user.name, user.discriminator)==(member_name, member_desc):
            await ctx.guild.unban(user)
            await ctx.send(member_name + " has been unbanned from {ctx.guild.name}")
            return
    
    await ctx.send(member + " was not found.")

@testbot.command()
@commands.has_permissions(kick_members=True)
async def mute(ctx,member : discord.Member):
    muted_role = ctx.guild.get_role(839888159977242654)

    await member.add_roles(muted_role)

    await ctx.send(member.mention + " has been muted.")

@testbot.command()
@commands.has_permissions(kick_members=True)
async def unmute(ctx,member : discord.Member):
    muted_role = ctx.guild.get_role(839888159977242654)

    await member.remove_roles(muted_role)

    await ctx.send(member.mention + " has been unmuted.")

@testbot.command()
async def greet(ctx):
    await ctx.send(f"Hello you beautiful beautiful people, welcome to {ctx.guild.name}!")

@testbot.command()
async def sing(ctx):
    await ctx.send("She sell seashells on the seashore, but the value of these shells will fall...")

@testbot.command()
async def whois(ctx, member : discord.Member):
    embed = discord.Embed(title=member.name, description=member.mention, colour = discord.Colour.green())
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Joined: ", value=member.joined_at, inline=True)
    embed.add_field(name="Registered: ", value=member.created_at, inline=True)
    embed.add_filed(name="Top role: ", value=member.top_role, inline=True)
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by{ctx.author.name}")
    await ctx.send(embed=embed)

@testbot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def giverole(ctx):
    embed = discord.Embed(title="Reaction roles", description="Choose a role from the following set of reaction roles!", colour=discord.Colour.blue())
    msg = await ctx.send(embed=embed)
    #Apple
    await msg.add_reaction('🍎')
    #Mango
    await msg.add_reaction('🥭')
    #Grapes
    await msg.add_reaction('🍇')
    #Pear
    await msg.add_reaction('🍐')

@testbot.command()
async def meme(ctx, memes="memes"):
    subreddit = reddit.subreddit(memes)
    all_subs = []

    hot = subreddit.hot(limit = 100)

    for submission in hot:
        all_subs.append(submission)

    random_sub = random.choice(all_subs)

    name = random_sub.title
    url = random_sub.url

    em = discord.Embed(title=name)
    em.set_image(url=url)
    em.set_footer(icon_url="https://styles.redditmedia.com/t5_2qjpg/styles/communityIcon_wal7c12k77v61.png", text="r/memes")

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
    url = random_sub.url

    em = discord.Embed(title=name)
    em.set_image(url=url)
    em.set_footer(icon_url="https://styles.redditmedia.com/t5_3ndbi/styles/communityIcon_vez4sc4u1sr61.png", text="r/formuladank")
    
    await ctx.send(embed=em)

@testbot.command()
async def engrish(ctx, ripenglish="engrish"):
    subreddit = reddit.subreddit(ripenglish)
    all_subs = []

    hot = subreddit.hot(limit = 100)

    for submission in hot:
        all_subs.append(submission)

    random_sub = random.choice(all_subs)

    name = random_sub.title
    url = random_sub.url

    em = discord.Embed(title=name)
    em.set_image(url=url)
    em.set_footer(icon_url="https://styles.redditmedia.com/t5_2qmxz/styles/communityIcon_idhheje7gps21.png", text="r/engrish")

    await ctx.send(embed=em)

@testbot.command()
async def shitmcsuggest(ctx, shitmc="shittymcsuggestions"):
    subreddit = reddit.subreddit(shitmc)
    all_subs = []

    hot = subreddit.hot(limit = 100)

    for submission in hot:
        all_subs.append(submission)

    random_sub = random.choice(all_subs)

    name = random_sub.title
    post = random_sub.selftext
    url = random_sub.url

    em = discord.Embed(title=name, description=post)
    em.set_image(url=url)
    em.set_footer(icon_url="https://styles.redditmedia.com/t5_2vdeq/styles/communityIcon_7tn9yczajec41.png?width=256&s=5aaefc7f21d16683c8916c363eaabb910a8585c3", text="r/shittymcsuggestions")

    await ctx.send(embed=em)

@testbot.command()
async def verbose(ctx, verboseup="IncreasinglyVerbose"):
    subreddit = reddit.subreddit(verboseup)
    all_subs = []

    hot = subreddit.hot(limit = 100)

    for submission in hot:
        all_subs.append(submission)

    random_sub = random.choice(all_subs)

    name = random_sub.title
    url = random_sub.url

    em = discord.Embed(title=name)
    em.set_image(url=url)
    em.set_footer(icon_url="https://styles.redditmedia.com/t5_3i5tr/styles/communityIcon_2k48ka7t7se21.png?width=256&s=8fd6dc239fbce275b7ec4487426189d08e538e38", text="r/IncreasinglyVerbose")

    await ctx.send(embed=em)

@testbot.command()
async def owofy(ctx):
    c = ctx.message.content
    c = c.replace('$owofy', '', 1)
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

@testbot.command()
async def rolldice(ctx):
    n = random.randrange(1, 7)
    await ctx.send(f"{n}🎲")

@testbot.command()
async def coinflip(ctx):
    choices = ["Heads", "Tails"]
    coin = random.choice(choices)
    await ctx.send(f"{coin}:coin:")

@testbot.command()
async def tictactoe(ctx, p1 : discord.Member, p2 : discord.Member):
    global player1
    global player2
    global turn
    global gameOver
    global count

    if gameOver:
        global board
        await ctx.send(embed = discord.Embed(title="To see what each square's number is type $board"))
        board = ["⬜", "⬜", "⬜",
                 "⬜", "⬜", "⬜",
                 "⬜", "⬜", "⬜"]

        turn = ""
        gameOver = False
        count = 0


        player1 = p1
        player2 = p2

        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x ==8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]
            

        num =random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.send(f"It's {player1.mention}'s turn!")
        elif num == 2:
            turn = player2
            await ctx.send(f"It's {player2.mention}'s turn!")
    else:
        await ctx.send("⭕There is still an ongoing match of tictactoe, please wait for it to end❌")

@testbot.command()
async def place(ctx, pos : int):
    global turn
    global player1
    global player2
    global board
    global count

    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":x:"
            elif turn == player2:
                mark = ":o:"
            if 0 < pos < 10 and board[pos - 1] == "⬜":
                board[pos - 1] = mark
                count += 1

                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x ==8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]
                
                checkWinner(winningConditions, mark)
                if gameOver:
                    await ctx.send(mark + " wins!")
                elif count >= 9:
                    await ctx.send("It's a tie!")
                    tie()

                #switch turns
                if turn == player1:
                    turn = player2
                elif turn ==player2:
                    turn = player1
                
            else:
                await ctx.send("Be sure to choose an integer between 1 and 9 and an unmarked tile")
        else:
            await ctx.send("It is not your turn yet. Please wait for your turn.")
    else:
        await ctx.send('⭕There are no ongoing tictactoe matches going on. Use the "$tictactoe" command to start a new one!❌')

@testbot.command()
async def end(ctx):
  global gameOver
  if not gameOver:
    gameOver = True
    await ctx.send("Stopping current game...")
  else:
    await ctx.send("⭕There is currently no game running!❌")

def tie():
  global gameOver
  gameOver = True

def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True

@testbot.command()
async def board(ctx):
  embed = discord.Embed(title="What each square's number is", description = ":one::two::three:\n:four::five::six:\n:seven::eight::nine:")
  await ctx.send(embed = embed)

@tictactoe.error
async def tictactoe_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention two players for this command")
    if isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to mention/ping players (e.g <@839532962600714280>).")

@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please enter the position you'd like to mark")
    if isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to enter an integer.")

testbot.run(discord_token)