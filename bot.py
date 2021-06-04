import discord
import asyncio
import json
import requests
import random
from discord.ext import commands, tasks
from discordtoken import discord_token, api_key
from discord_components import *
from texttoowo import text_to_owo
from redditmeme import reddit
from itertools import cycle
from tictactoe import winningConditions, player1, player2, turn, gameOver, board
from weatherassets import *
from prsaw import RandomStuff
from eightballresponses import outputs
from connectfourassets import *


testbot = commands.Bot(command_prefix="$", intents=discord.Intents.all())
testbot.remove_command("help")

startup_extensions = ["Cogsforbot.Coghelp", "Cogsforbot.chess", "Cogsforbot.snakegameassets", "Cogsforbot.UrbanDictionary", "Cogsforbot.Wikisearch"]

filtered_words = ['fuck', 'bullshit']

rs = RandomStuff(async_mode=True)

status = cycle([
    'discord.py',
    '$help',
    'Snake',
    'Tictactoe',
    'Chess',
    '[insert your favourite game here]'
])

@tasks.loop(seconds=5)
async def status_swap():
    await testbot.change_presence(activity=discord.Game(next(status)))


@testbot.event
async def on_ready():
    print("Test bot ready to go")
    status_swap.start()
    DiscordComponents(testbot)


@testbot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.channels, name='welcome')
    await channel.send(f"Hello there {member.mention}! A warm welcome to you for joining {member.guild.name}!")

    with open('users.json', 'r') as f:
        users = json.load(f)
    
    await update_data(users, member)

    with open('users.json', 'w') as f:
        json.dump(users, f, indent=4)


@testbot.event
async def on_member_remove(member):
    channel = discord.utils.get(member.guild.channels, name='goodbye')
    await channel.send(f"We will miss you, {member.mention}!")


@testbot.event
async def on_message(msg):
    if testbot.user == msg.author:
        return
    for word in filtered_words:
        if word in msg.content:
            await msg.delete()
    
    if msg.channel.name == 'ai-chat':
            response = await rs.get_ai_response(msg.content)
            await msg.reply(response)
        
    await testbot.process_commands(msg)   
    
    if msg.author != testbot.user and msg.content.startswith('$weather'):
        if len((msg.content.replace('$weather ', ''))) >= 1:
            location = msg.content.replace('$weather ', '')
            url = 'http://api.openweathermap.org/data/2.5/weather?q=' + location + '&appid=' + api_key + '&units=metric'
            try:
                data = parse_data(json.loads(requests.get(url).content)['main'])
                await msg.channel.send(embed=weathermsg(data, location))
            except KeyError:
                await msg.channel.send(embed=error_message(location))
    
    if msg.author.bot == False:
        with open('users.json', 'r') as f:
            users = json.load(f)
        
        await update_data(users, msg.author)
        await add_experience(users, msg.author, 5)
        await level_up(users, msg.author, msg)

        with open('users.json', 'w') as f:
            json.dump(users, f, indent=4)
    
    if msg.content == '$dev':
        await msg.channel.send(
            "Button Command Ran!",
            components =[[
                Button(style=ButtonStyle.URL, label="See my progress!", url="https://github.com/sametaor/Test-bot-for-Discord/tree/master"),
                Button(style=ButtonStyle.URL, label="Report issues!", url="https://github.com/sametaor/Test-bot-for-Discord/issues")
            ]],
        )
        res = await testbot.wait_for("button_click")
        if res.channel == msg.channel:
            await res.respond(
                type=InteractionType.ChannelMessageWithSource,
                content=f'{res.component.label} clicked'
            )

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
    
    if payload.member.bot:
        pass

    else:
        with open('giverole.json') as react_file:
            data = json.load(react_file)
            for x in data:
                if str(x['emoji']) == payload.emoji.name:
                    role = discord.utils.get(testbot.get_guild(payload.guild_id).roles, id=x['role_id'])

                    await payload.member.add_roles(role)


@testbot.event
async def on_raw_reaction_remove(payload):
    with open('giverole.json') as react_file:
        data = json.load(react_file)
        for x in data:
            if str(x['emoji']) == payload.emoji.name:
                role = discord.utils.get(testbot.get_guild(payload.guild_id).roles, id=x['role_id'])

                await testbot.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(role)


@testbot.group(invoke_without_command=True)
async def help(ctx):
    em = discord.Embed(title="May I help you?", description="Use $help <command> for detailed info of a command", colour=ctx.author.colour)
    em.add_field(name="Moderation", value = "purge, kick, ban, unban, mute, unmute, tempmute, lockdown, unlock, slowmode, giverole, nickset, whois")
    em.add_field(name="Reddit", value="meme, formuladank, crapmcsuggest, verbose, engrish")
    em.add_field(name="Fun", value="owofy, guess, rolldice, coinflip, sing, 8ball")
    em.add_field(name="Games", value="tictactoe, place, board, end")
    em.add_field(name="Additional help:", value="addhelp")
    em.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author.name}")
    await ctx.send(embed=em)

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
@commands.has_permissions(manage_messages=True)
async def warn(ctx, member : discord.Member, *, reason=None):
    if member is None:
        await ctx.send('Please provide a member.')
    elif member == testbot.user:
        await ctx.send('You cannot warn a bot member.')
    elif member == ctx.author:
        await ctx.send('You cannot warn yourself.')
    else:
        await ctx.message.delete()
        try:
            await member.send(f'You have been warned in {ctx.guild.name} for the following reason: {reason}')
        except:
            await ctx.send("Couldn't send warn message because member has their DMs closed")
        
        embed = discord.Embed(title="Warn", description=f'{member.mention}', colour = discord.Colour.red())
        embed.add_field(name="Reason:", value=f'{reason}')
        embed.add_field(name="Warned by:", value=f'{ctx.author.mention}', inline=True)
        await ctx.send(embed=embed)

@testbot.command()
@commands.has_permissions(manage_messages=True)
async def mute(ctx,member : discord.Member, *, reason=None):
    guild = ctx.guild
    muted_role = discord.utils.get(guild.roles, name="Muted")

    if not muted_role:
        muted_role = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(muted_role, speak=False, send_messages=False, stream=False, attach_files=False, mention_everyone=False, external_emojis=False, connect=False, read_messages=False)
    
    await member.add_roles(muted_role, reason=reason)
    await ctx.send(f"{member.mention} has been muted for the following reason: {reason}.")
    await member.send(f"You were muted in {guild.name} for the following reason: {reason}.")

@testbot.command()
@commands.has_permissions(manage_messages=True)
async def unmute(ctx,member : discord.Member):
    guild = ctx.guild
    mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

    await member.remove_roles(mutedRole)
    await ctx.send(f"{member.mention} has been unmuted.")
    await member.send(f"You were unmuted in {guild.name}.")

@testbot.command()
async def tempmute(ctx, member: discord.Member=None, time=None, *, reason=None):
    if not member:
        await ctx.send("You must mention a member to mute!")
    elif not time:
        await ctx.send("You must mention a time!")
    else:
        if not reason:
            reason="No reason given"
        #Now timed mute manipulation
    try:
        time_interval = time[:-1] #Gets the numbers from the time argument, start to -1
        duration = time[-1] #Gets the timed manipulation, s, m, h, d
        if duration == "s":
            time_interval = time_interval * 1
        elif duration == "m":
            time_interval = time_interval * 60
        elif duration == "h":
            time_interval = time_interval * 60 * 60
        elif duration == "d":
            time_interval = time_interval * 86400
        else:
            await ctx.send("Invalid duration input")
            return
    except Exception as e:
        print(e)
        await ctx.send("Invalid time input")
        return
    guild = ctx.guild
    Muted = discord.utils.get(guild.roles, name="Muted")
    if not Muted:
        Muted = await guild.create_role(name="Muted")
        for channel in guild.channels:
            await channel.set_permissions(Muted, speak=False, send_messages=False, read_message_history=True, read_messages=False)
    else:
        await member.add_roles(Muted, reason=reason)
        muted_embed = discord.Embed(title="Tempmuted a user", description=f"{member.mention} Was muted for {reason} for {time}", colour=discord.Colour.dark_red())
        await ctx.send(embed=muted_embed)
        await asyncio.sleep(int(time_interval))
        await member.remove_roles(Muted)
        unmute_embed = discord.Embed(title='Tempmute over!', description=f'{member.mention} has been unmuted for {reason} after {time}', colour=discord.Colour.green())
        await ctx.send(embed=unmute_embed)

@testbot.command()
@commands.has_permissions(manage_messages=True)
async def lockdown(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send(ctx.channel.mention + "is now set to lockdown mode.")

@testbot.command()
@commands.has_permissions(manage_messages=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("Lockdown mode is now removed for " + ctx.channel.mention)

@testbot.command()
@commands.has_permissions(manage_messages=True)
async def slowmode(ctx, seconds : int):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"The slowmode is now set to {seconds} seconds.")

@testbot.command(pass_context=True)
async def nickset(ctx, member : discord.Member, nick):
    if member == ctx.author:
        await member.edit(nick=nick)
        await ctx.send(f"Nickname changed for {member.mention} ")
    elif member != ctx.author:
        await ctx.send("You cannot change others' nicknamess without the required permissions. Only mention your own name.")

@testbot.command()
async def sing(ctx):
    await ctx.send("She sells seashells on the seashore, but the value of these shells will fall...")

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

@testbot.command()
async def avatar(ctx, member : discord.Member = None):
    if not member:
        member = ctx.message.author
    avatar = member.avatar_url
    embed = discord.Embed(title=member.name, colour=discord.Colour.blue())
    embed.set_image(url=avatar)
    embed.set_footer(icon_url=ctx.author.avatar_url, text=f"Requested by {ctx.author.name}")
    await ctx.send(embed=embed)

@testbot.command(aliases=['8ball'])
async def eightball(ctx, *, question):
    await ctx.send(f':8ball: {random.choice(outputs)}')
@testbot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def giverole(ctx, emoji,role : discord.Role,*,message):
    embed = discord.Embed(description=message)
    rolemsg = await ctx.channel.send(embed=embed)
    await rolemsg.add_reaction(emoji)

    with open('giverole.json') as json_file:
        data = json.load(json_file)

        new_react_role = {
            'role_name' : role.name,
            'role_id' : role.id,
            'emoji' : emoji,
            'message_id' : rolemsg.id
        }

        data.append(new_react_role)
    
    with open('giverole.json','w') as j:
        json.dump(data,j,indent=4)


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
async def crapmcsuggest(ctx, shitmc="shittymcsuggestions"):
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

async def update_data(users, user):
    if not f'{user.id}' in users:
        users[f'{user.id}'] = {}
        users[f'{user.id}']['experience'] = 0
        users[f'{user.id}']['level'] = 1

async def add_experience(users, user, exp):
    users[f'{user.id}']['experience'] += exp

async def level_up(users, user, message):
    with open('levels.json', 'r') as g:
        levels = json.load(g)
    experience = users[f'{user.id}']['experience']
    lvl_start = users[f'{user.id}']['level']
    lvl_end = int(experience ** (1/4))
    if lvl_start < lvl_end:
        await message.channel.send(f'{user.mention} has levelled up! LEVEL - {lvl_end}')
        users[f'{user.id}']['level'] = lvl_end

@testbot.command()
async def rank(ctx, member : discord.Member):
    if not member:
        id = ctx.message.author.id
        with open('users.json', 'r') as f:
            users = json.load(f)
        lvl = users[str(id)]['level']
        await ctx.send(f'You are at level {lvl}!')
    else:
        id =  member.id
        with open('users.json', 'r') as f:
            users = json.load(f)
        lvl = users[str(id)]['level']
        await ctx.send(f'{member} is at level {lvl}!')

@testbot.group(invoke_without_command=True)
@commands.guild_only()
@commands.has_guild_permissions(manage_channels=True)
@commands.bot_has_guild_permissions(manage_channels=True)
async def new(ctx):
    await ctx.send("Invalid sub-command passed.")

@new.command()
@commands.guild_only()
@commands.has_guild_permissions(manage_channels=True)
@commands.bot_has_guild_permissions(manage_channels=True)
async def category(ctx, role: discord.Role, *, name):
    overwrites = {
    ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
    ctx.guild.me: discord.PermissionOverwrite(read_messages=True),
    role: discord.PermissionOverwrite(read_messages=True)
    }
    category = await ctx.guild.create_category(name=name, overwrites=overwrites)
    await ctx.send(f"Hey dude, I made {category.name} for ya!")
    
@new.command()
@commands.guild_only()
@commands.has_guild_permissions(manage_channels=True)
@commands.bot_has_guild_permissions(manage_channels=True)
async def channel(ctx, role: discord.Role, *, name):
    overwrites = {
    ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
    ctx.guild.me: discord.PermissionOverwrite(read_messages=True),
    role: discord.PermissionOverwrite(read_messages=True)
    }
    channel = await ctx.guild.create_text_channel(name=name, overwrites=overwrites)
    await ctx.send(f"Hey dude, I made {channel.name} for ya!")

@testbot.command(aliases=['connect'])
async def connect4(ctx,p1:discord.Member,p2:discord.Member):
    global player1
    global player2
    global gameOver
    global turn
    global modes

    if gameOver:
        global board
        global numturn
        board = [
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0]
        ]
        player1 = p1.name
        player2 = p2.name

        board_render = []
        count_render = 0
        num = random.randint(1,2)
        if num == 1:
            numturn = 1
            turn = player1
        elif num == 2:
            numturn = 2
            turn = player2
        for count, i in enumerate(board):
            if ([0, 0, 0, 0, 0, 0, 0, 0]== i) and count_render <= 3:
                count_render +=1
                board_render.append(i)
            elif count_render <= 3:
                board_render.append(i)
            
        board_render.reverse()
        await ctx.send(render(board_render))
        await ctx.send("{}'s Turn!".format(turn))
        board_render.reverse()
        gameOver = False
    else:
        await ctx.send("A Connect-4 game is already going on.")

@testbot.command(aliases=['p'])
async def c4place(ctx,num:int):
    global player1
    global player2
    global gameOver
    global turn
    global modes

    if not gameOver:
        global board
        global numturn

        counts = 0
        count_render = 0
        board_render = []
        count_tie = 0
        if turn == ctx.author.name:
            for count, i in enumerate(board):
                if ([0, 0, 0, 0, 0, 0, 0, 0]== i) and count_render <= 3:
                    count_render +=1
                    board_render.append(i)
                elif count_render <= 3:
                    board_render.append(i)
            for count, i in enumerate(board):
                if i[num-1] == 0:
                    counts += 1
                    board[count][num-1] = numturn
                    win = windetect(board,turn)
                    if win:
                        board_render.reverse()
                        line = ''
                        await ctx.send(render(board_render))
                        gameOver = True
                            # time.sleep(0.3)
                        await ctx.send("{} wins!".format(turn))
                        await ctx.send(":partying_face: Congratulations!")
                        board_render.reverse()
                        return
                    if turn == player1:
                        numturn= 2
                        turn = player2
                    else:
                        numturn = 1
                        turn = player1
                    board_render.reverse()
                    for i in board:
                        print(i)
                    line = ''
                    await ctx.send(render(board_render))
                    await ctx.send("{} Turn!".format(turn))
                    board_render.reverse()
                    return
                for y in i:
                    if y == 0:
                        count_tie += 1
                if count_tie == 0:
                    counts += 1
                    if modes == 1:
                        await ctx.send(render(board_render))
                    elif modes == 2:
                        await ctx.send(embed=render(board_render))
                    await ctx.send("Tie!")
                    return
        else:
            await ctx.send("It's not your turn")
            counts += 1
        if counts == 0:
            await ctx.send("That column is full, please select another column.")
    else:
        await ctx.send("Please start with $connect4 command.")

def render(board_render):
    line=''
    global modes
    for count,x in enumerate(board_render):
        for y in x:
            if y == 0:
                line += (":white_medium_square:" + ' ')
            elif y == 1:
                line += (":red_circle:" + ' ')
            elif y == 2:
                line += (":yellow_circle:" + ' ')
        if count <= len(board_render)-2:
            line += "\n"
    return line


def windetect(board,turn):
    global numturn
    boardHeight = len(board)
    boardWidth = len(board[0])
    tile = numturn

    # check horizontal spaces
    for y in range(boardHeight):
        for x in range(boardWidth - 3):
            if board[x][y] == tile and board[x+1][y] == tile and board[x+2][y] == tile and board[x+3][y] == tile:
                return True
    
    # check vertical spaces
    for x in range(boardWidth):
        for y in range(boardHeight - 3):
            if board[x][y] == tile and board[x][y+1] == tile and board[x][y+2] == tile and board[x][y+3] == tile:
                return True
    
    # check / diagonal spaces
    for x in range(boardWidth - 3):
        for y in range(3, boardHeight):
            if board[x][y] == tile and board[x+1][y-1] == tile and board[x+2][y-2] == tile and board[x+3][y-3] == tile:
                return True

    # check \ diagonal spaces
    for x in range(boardWidth - 3):
        for y in range(boardHeight - 3):
            if board[x][y] == tile and board[x+1][y+1] == tile and board[x+2][y+2] == tile and board[x+3][y+3] == tile:
                return True
    return False   

@testbot.command()
async def c4stop(ctx):
    global gameOver
    if not gameOver:
        gameOver = True
        await ctx.send("The game has been stopped.")
    else:
        await ctx.send("The Game has ended.")

@testbot.command()
async def c4mode(ctx,mode):
    global modes
    if mode == '1':
        modes = 1
        await ctx.send("Changed to mode 1.")
    if mode == '2':
        modes = 2
        await ctx.send("Changed to mode 2.")

@c4mode.error
async def mode_error(ctx,error):
    global modes
    text = "Mode:\n    1. Play in 1 device\n    2. Play with your friend\nCurrent: {}".format(modes)
    if isinstance(error,commands.MissingRequiredArgument):
        await ctx.send(text)

@help.command()
async def new(ctx):
    em = discord.Embed(title="New", description="Use this command to add a new channel with a specified name and role or member permission.", colour=discord.Colour.green())
    em.add_field(name="**Syntax**", value="$new <channel or category> <@role or @member> <name of channel or category>")
    await ctx.send(embed=em)

@help.command()
async def connect4(ctx):
    em = discord.Embed(title="Connect-4", description="Starts a game of Connect-4 with a mentioned member.", colour=discord.Colour.green())
    em.add_field(name="**Syntax**", value="$connect4 <@player1> <@player2>")
    await ctx.send(embed=em)

@help.command()
async def c4place(ctx):
    em = discord.Embed(title="Place", description="Use this to place a dot in a connect 4 board.", colour=discord.Colour.green())
    em.add_field(name="**Syntax**", value="$c4place <column>")
    await ctx.send(embed=em)

@help.command()
async def c4stop(ctx):
    em = discord.Embed(title="Stop", description="Use this to stop a Connect-4 game.", colour=discord.Colour.green())
    em.add_field(name="**Syntax**", value="$c4stop")
    await ctx.send(embed=em)

@help.command()
async def c4mode(ctx):
    em = discord.Embed(title="Mode", description="Use this to change your mode from singeplayer to multiplayer for Connect-4", colour=discord.Colour.green())
    em.add_field(name="**Syntax**", value="$c4mode <Put either mode 1 or 2>")
    await ctx.send(embed=em)

@help.command()
async def purge(ctx):
    em = discord.Embed(title="purge", description="Clears the last sent msgs in a channel.", colour=discord.Colour.green())
    em.add_field(name="**Syntax**", value="$purge <number of msgs to be deleted>")
    await ctx.send(embed=em)

@help.command()
async def kick(ctx):
    em = discord.Embed(title="kick", description="Kicks the specified member out of a server.", colour=discord.Colour.green())
    em.add_field(name="**Syntax**", value="$kick <@member> <reason>")
    await ctx.send(embed=em)

@help.command()
async def ban(ctx):
    em = discord.Embed(title="ban", description="Bans the specified member from a server.", colour=discord.Colour.green())
    em.add_field(name="**Syntax**", value="$ban <@member> <reason>")
    await ctx.send(embed=em)

@help.command()
async def unban(ctx):
    em = discord.Embed(title="unban", description="Unbans a user from a server.", colour=discord.Colour.green())
    em.add_field(name="**Syntax**", value="$unban <username> ")
    await ctx.send(embed=em)

@help.command()
async def mute(ctx):
    em = discord.Embed(title="mute", description="Mutes the specified member in a server.", colour=discord.Colour.green())
    em.add_field(name="**Syntax**", value="$mute <@member> <reason>")
    await ctx.send(embed=em)

@help.command()
async def unmute(ctx):
    em = discord.Embed(title="unmute", description="Unmutes the specified member in a server.", colour=discord.Colour.green())
    em.add_field(name="**Syntax**", value="$unmute <@member>")
    await ctx.send(embed=em)

@help.command()
async def tempmute(ctx):
    em = discord.Embed(title="tempmute", description="Temporarily mutes the specified member for a specified amount of time in a server.", colour=discord.Colour.green())
    em.add_field(name="**Syntax**", value="$tempmute <@member> <time> <reason>")
    await ctx.send(embed=em)

@help.command()
async def lockdown(ctx):
    em = discord.Embed(title="lockdown", description="Locks the specified channel to stop members from messaging.", colour=discord.Colour.green())
    em.add_field(name="**Syntax**", value="$lockdown")
    await ctx.send(embed=em)

@help.command()
async def unlock(ctx):
    em = discord.Embed(title="unlock", description="Unlocks the specified channel to allow members to send messages.", colour=discord.Colour.green())
    em.add_field(name="**Syntax**", value="$unlock")
    await ctx.send(embed=em)

@help.command()
async def slowmode(ctx):
    em = discord.Embed(title="slowmode", description="Applies a specified amount of slowmode in the specified channel.", colour=discord.Colour.green())
    em.add_field(name="**Syntax**", value="$slowmode <time in seconds>")
    await ctx.send(embed=em)

@help.command()
async def nickset(ctx):
    em = discord.Embed(title="nickset", description="Lets one set a custom nickname in the server.", colour=discord.Colour.green())
    em.add_field(name="**Syntax**", value="$nickset <@member> <preferred nickname>")
    await ctx.send(embed=em)

@help.command()
async def sing(ctx):
    em = discord.Embed(title="sing", description="Makes the bot sing a line off of the song Money Game Part2 by Ren.", colour=discord.Colour.green())
    em.add_field(name="**Syntax**", value="$sing")
    await ctx.send(embed=em)

@help.command()
async def whois(ctx):
    em = discord.Embed(title="whois", description="Lets one view the user info of the specified user.", colour=discord.Colour.green())
    em.add_field(name="**Syntax**", value="$whois <@member>")
    await ctx.send(embed=em)

@help.command()
async def meme(ctx):
    em = discord.Embed(title="meme", description="Sends content from r/memes.", colour=discord.Colour.green())
    em.add_field(name="**Syntax**", value="$meme")
    await ctx.send(embed=em)

@help.command()
async def formuladank(ctx):
    em = discord.Embed(title="formuladank", description="Sends content from r/formuladank.", colour=discord.Colour.green())
    em.add_field(name="**Syntax**", value="$formuladank")
    await ctx.send(embed=em)

@help.command()
async def crapmcsuggest(ctx):
    em = discord.Embed(title="crapmcsuggest", description="Sends content from r/shittymcsuggestions.", colour=discord.Colour.green())
    em.add_field(name="**Syntax**", value="$crapmcsuggest")
    await ctx.send(embed=em)

@help.command()
async def verbose(ctx):
    em = discord.Embed(title="verbose", description="Sends content from r/IncreasinglyVerbose.", colour=discord.Colour.green())
    em.add_field(name="**Syntax**", value="$verbose")
    await ctx.send(embed=em)

@help.command()
async def engrish(ctx):
    em = discord.Embed(title="engrish", description="Sends content from r/engrish.", colour=discord.Colour.green())
    em.add_field(name="**Syntax**", value="$engrish")
    await ctx.send(embed=em)

@help.command()
async def owofy(ctx):
    em = discord.Embed(title="purge", description="Decorates the specified text with cursed OwOs.", colour=discord.Colour.green())
    em.add_field(name="**Syntax**", value="$owofy <text>")
    await ctx.send(embed=em)

@help.command()
async def guess(ctx):
    em = discord.Embed(title="guess", description="Starts a guessing game with three turns.", colour=discord.Colour.green())
    em.add_field(name="**Syntax**", value="$guess")
    await ctx.send(embed=em)

@help.command()
async def rolldice(ctx):
    em = discord.Embed(title="rolldice", description="Gives a random face of a dice.", colour=discord.Colour.green())
    em.add_field(name="**Syntax**", value="$rolldice")
    await ctx.send(embed=em)

@help.command()
async def coinflip(ctx):
    em = discord.Embed(title="coinflip", description="Gives either Heads or Tails face of a coin.", colour=discord.Colour.green())
    em.add_field(name="**Syntax**", value="$coinflip")
    await ctx.send(embed=em)

@help.command()
async def tictactoe(ctx):
    em = discord.Embed(title="tictactoe", description="Starts a match of tictactoe with another mentioned member.", colour=discord.Colour.green())
    em.add_field(name="**Syntax**", value="$tictactoe <@member1> <@member2>")
    await ctx.send(embed=em)

@help.command()
async def place(ctx):
    em = discord.Embed(title="place(related to tictactoe)", description="Used to define positions for either a ❌ or a ⭕.", colour=discord.Colour.green())
    em.add_field(name="**Syntax**", value="$place <position>")
    await ctx.send(embed=em)

@help.command()
async def board(ctx):
    em = discord.Embed(title="board(related to tictactoe)", description="Used to show the positions on the tictactoe board.", colour=discord.Colour.green())
    em.add_field(name="**Syntax**", value="$board")
    await ctx.send(embed=em)

@help.command()
async def eightball(ctx):
    em = discord.Embed(title="8ball", description="Use this to ask a question and the bot will give a random answer to that.", colour=discord.Colour.green())
    em.add_field(name="**Syntax**", value="$8ball <question or text>")
    await ctx.send(embed=em)

if __name__ == "__main__":  # When script is loaded, this will run
    for extension in startup_extensions:
        try:
            testbot.load_extension(extension)  # Loads cogs successfully
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))  # Failed to load cog, with error

testbot.run(discord_token)
