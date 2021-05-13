import discord
from discord.ext import commands
import asyncio
import discordtoken
from discordtoken import discord_token
import random
import praw
from texttoowo import text_to_owo
from redditmeme import reddit


testbot = commands.Bot(command_prefix="$")

filtered_words = ["fuck", "bullshit"]

@testbot.event
async def on_ready():
    print("Test bot ready to go")


@testbot.event
async def on_message(msg):
    for word in filtered_words:
        if word in msg.content:
            await msg.delete()
    
    await testbot.process_commands(msg)


@testbot.event
async def on_command_error(ctx,error):
    if isinstance(error,commands.MissingPermissions):
        await ctx.send("You are missing the required permissions to do that.")
    elif isinstance(error,commands.CommandInvokeError):
        await ctx.send("Message cannot be empty")
    elif isinstance(error,commands.CommandNotFound):
        await ctx.send("That command does not exist")
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

testbot.run(discord_token)