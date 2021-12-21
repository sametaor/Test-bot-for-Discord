import nextcord as discord
import asyncio
import fandom
import aiohttp
import json
import urllib
import os
from io import BytesIO
from discord.enums import ChannelType
from prsaw.PRSAW import RandomStuffV4
from dotenv import load_dotenv
import requests
import random
import datetime
from discord import Member
from typing import Optional
from nextcord.ext import commands, tasks
from discordsecrets import api_key, ai_api_key
from texttoowo import text_to_owo
from redditmeme import reddit
from itertools import cycle
from tictactoe import winningConditions, player1, player2, turn, gameOver, board
from weatherassets import *
from eightballresponses import outputs
from connectfourassets import *


testbot = commands.Bot(command_prefix="&", intents=discord.Intents.all())
testbot.remove_command("help")

rs = RandomStuffV4(async_mode=True, api_key=ai_api_key)

load_dotenv('token.env')
Button = discord.ui.Button
ButtonStyle = discord.ButtonStyle

status = cycle([
    'discord.py',
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
    await testbot.change_presence(activity=discord.Game(next(status)))


@testbot.event
async def on_ready():
    print("Test bot ready to go")
    status_swap.start()


@testbot.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.channels, name='welcome')
    await channel.send(f"Hello there {member.mention}! A warm welcome to you for joining {member.guild.name}!")


@testbot.event
async def on_member_remove(member):
    channel = discord.utils.get(member.guild.channels, name='welcome')
    await channel.send(f"We will miss you, {member.mention}!")


@testbot.event
async def on_message(msg):
    message = msg.content
    key = ai_api_key
    header = {"x-api-key": key}
    type = "stable"
    params = {'type':type , 'message':message}
    if testbot.user == msg.author:
        return

    if not msg.author.bot:
        if msg.channel.name == 'ai-chat':
            if msg.author != testbot.user and "fax" in msg.content:
                await msg.add_reaction(emoji="📠")
            if msg.author != testbot.user and "hmm" in msg.content or "Hmm" in msg.content:
                await msg.add_reaction(emoji="🤔")

            if msg.author != testbot.user and "ok and?" in msg.content or "Ok and?" in msg.content:
                await msg.reply("I forgor 💀....Wait! I rember 😀")

            if msg.author != testbot.user and "I forgor" in msg.content or "I Forgor" in msg.content:
                await msg.add_reaction(emoji="💀")

            if msg.author != testbot.user and "I rember" in msg.content or "I Rember" in msg.content:
                await msg.add_reaction(emoji="😀")

            if msg.author != testbot.user and "dead chat" in msg.content or "Dead chat" in msg.content:
                await msg.reply("Howdy 🤠")

            if msg.author != testbot.user and "Get it?" in msg.content:
                await msg.reply("https://tenor.com/view/ba-dum-tsss-drum-band-gif-7320811")

            if msg.author != testbot.user and "mistake" in msg.content:
                await msg.reply("https://tenor.com/view/bobross-art-gif-4621523")

            if msg.author != testbot.user and msg.content == "XD" or msg.content == "xD":
                await msg.reply("https://tenor.com/view/muta-laugh-gif-18813278")

            if msg.author != testbot.user and msg.content == "h" or msg.content == "H":
                await msg.reply("https://tenor.com/view/h-apple-apple-h-apple-gif-18834689")

            if msg.author != testbot.user and msg.content == "hello there" or msg.content == "Hello there":
                await msg.reply("https://tenor.com/view/hello-there-general-kenobi-star-wars-grevious-gif-17774326")
            if msg.author != testbot.user and "9 + 10" in msg.content or "9+10" in msg.content or "9 +10" in msg.content or "9+ 10" in msg.content:
                await msg.reply('"21"\n"U stupid!"')
            async with aiohttp.ClientSession(headers=header) as session:
                async with session.get(url='https://api.pgamerx.com/v3/ai/response', params=params) as resp:
                    text = await resp.json()
                    await msg.reply(text[0]['message'])

    await testbot.process_commands(msg)

    if msg.author != testbot.user and msg.content.startswith('&weather'):
        if len((msg.content.replace('&weather ', ''))) >= 1:
            location = msg.content.replace('&weather ', '')
            url = 'http://api.openweathermap.org/data/2.5/weather?q=' + location + '&appid=' + api_key + '&units=metric'
            try:
                data = parse_data(json.loads(requests.get(url).content)['main'])
                await msg.channel.send(embed=weathermsg(data, location))
            except KeyError:
                await msg.channel.send(embed=error_message())

    for file in msg.attachments:
        if file.filename.endswith((".exe", ".dll", ".xlsx")):
            await msg.delete()
            await msg.channel.send("No .exe, .dll or .xlsx files allowed!")

@testbot.event
async def on_command_error(ctx,error):
    if isinstance(error,commands.MissingPermissions):
        await ctx.send("You are missing the required permissions to do that.")
    elif isinstance(error,commands.CommandNotFound):
        if ctx.message.content.startswith("&weather"):
            pass
        else:
            await ctx.send("That command does not exist")
    elif isinstance(error,commands.MissingRequiredArgument):
        await ctx.send("Please enter the required arguments")
    elif isinstance(error,commands.BadArgument):
        await ctx.send("Please enter the correct arguments")
    elif isinstance(error,commands.BotMissingPermissions):
        await ctx.send("I don't have the required permissions to perform that")
    elif isinstance(error,commands.CommandOnCooldown):
        await ctx.send("This command is still on cooldown")
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
async def on_raw_reaction_add(payload):

    if payload.member.bot:
        pass

    else:
        with open('giverole.json') as react_file:
            data = json.load(react_file)
            for x in data:
                if x['emoji'] == payload.emoji.name and x['message_id'] == payload.message_id:
                    role = discord.utils.get(testbot.get_guild(payload.guild_id).roles, id=x['role_id'])

                    await payload.member.add_roles(role)


@testbot.event
async def on_raw_reaction_remove(payload):

    with open('giverole.json') as react_file:
        data = json.load(react_file)
        for x in data:
            if x['emoji'] == payload.emoji.name and x['message_id'] == payload.message_id:
                role = discord.utils.get(testbot.get_guild(payload.guild_id).roles, id=x['role_id'])

                await testbot.get_guild(payload.guild_id).get_member(payload.user_id).remove_roles(role)

@testbot.command(description="Toggles commands to be enabled or disabled")
@commands.has_guild_permissions(ban_members=True)
async def toggle(ctx, *, command):
    command = testbot.get_command(command)
    if command == None:
        await ctx.send("Command not found")
    elif ctx.command == command:
        await ctx.send("You cannot disable this command")
    else:
        command.enabled = not command.enabled
        togglecommand = "enabled" if command.enabled else "disabled"
        await ctx.send(f"{command.qualified_name} command has been {togglecommand}.")

@testbot.command(aliases=["clear", "delete"])
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount=2):
    await ctx.channel.purge(limit=amount)

@testbot.command(aliases=["remove"])
@commands.has_permissions(kick_members=True)
async def kick(ctx, target : Optional[Member],*, reason="No reason provided"):
    target = target or ctx.author
    if target == ctx.author:
        await ctx.send("You cannot kick yourself")
    else:
        try:
            await target.send(f"You have been kicked from{ctx.guild.name} for the following reason: " + reason)
        except:
            await ctx.send("The member has their DMs closed.")
        await target.kick(reason=reason)

@testbot.command(brief="Bans members from the server")
@commands.has_permissions(ban_members=True)
async def ban(ctx, target : Optional[Member], reason="No reason provided"):
    target = target or ctx.author
    if target == ctx.author:
        await ctx.send("You cannot ban yourself")
    else:
        await target.send(f"You have been banned from {ctx.guild.name} for the following reason: " + reason)
        await ctx.send(target.name + f" has been banned from {ctx.guild.name} for the following reason: " + reason)
        await target.ban(reason=reason)

@testbot.command()
@commands.has_permissions(ban_members=True)
async def unban(ctx,*,member):
    banned_users = await ctx.guild.bans()
    member_name, member_desc = member.split('#')
    for banned_entry in banned_users:
        user = banned_entry.user

        if(user.name, user.discriminator)==(member_name, member_desc):
            await ctx.guild.unban(user)
            await ctx.send(member_name + f" has been unbanned from {ctx.guild.name}")
            return

    await ctx.send(member + " was not found.")

@testbot.command()
@commands.has_permissions(manage_messages=True)
async def warn(ctx, target : Optional[Member], *, reason=None):
    target = target or ctx.author
    if target is None:
        await ctx.send('Please provide a member.')
    elif target == testbot.user:
        await ctx.send('You cannot warn a bot member.')
    elif target == ctx.author:
        await ctx.send('You cannot warn yourself.')
    else:
        await ctx.message.delete()
        try:
            await target.send(f'You have been warned in {ctx.guild.name} for the following reason: {reason}')
        except:
            await ctx.send("Couldn't send warn message because member has their DMs closed")

        embed = discord.Embed(title="Warn", description=f'{target.mention}', colour = discord.Colour.red())
        embed.add_field(name="Reason:", value=f'{reason}')
        embed.add_field(name="Warned by:", value=f'{ctx.author.mention}', inline=False)
        await ctx.send(embed=embed)

@testbot.command()
@commands.has_permissions(manage_messages=True)
async def mute(ctx,target : Optional[Member], *, reason=None):
    guild = ctx.guild
    target = target or ctx.author
    muted_role = discord.utils.get(guild.roles, name="Muted")

    if not muted_role:
        muted_role = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(muted_role, speak=False, send_messages=False, stream=False, attach_files=False, mention_everyone=False, external_emojis=False, connect=False, read_messages=False)
    if target == ctx.author:
        await ctx.send("You cannot mute yourself")
    else:
        await target.add_roles(muted_role, reason=reason)
        await ctx.send(f"{target.mention} has been muted for the following reason: {reason}.")
        await target.send(f"You were muted in {guild.name} for the following reason: {reason}.")

@testbot.command()
@commands.has_permissions(manage_messages=True)
async def unmute(ctx,target : Optional[Member]):
    guild = ctx.guild
    target = target or ctx.author
    mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

    await target.remove_roles(mutedRole)
    await ctx.send(f"{target.mention} has been unmuted.")
    await target.send(f"You were unmuted in {guild.name}.")

@testbot.command()
async def tempmute(ctx, target : Optional[Member]=None, time=None, *, reason=None):
    if target == None:
        await ctx.send("You must mention a member to mute!")
    elif target == ctx.author:
        await ctx.send("You cannot tempmute yourself!")
    elif not time:
        await ctx.send("You must mention a time!")
    else:
        if not reason:
            reason="No reason"
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
        await target.add_roles(Muted, reason=reason)
        muted_embed = discord.Embed(title="Tempmuted a user", description=f"{target.mention} Was muted for {reason} for {time}", colour=discord.Colour.dark_red())
        await ctx.send(embed=muted_embed)
        await asyncio.sleep(int(time_interval))
        await target.remove_roles(Muted)
        unmute_embed = discord.Embed(title='Tempmute over!', description=f'{target.mention} has been unmuted for {reason} after {time}', colour=discord.Colour.green())
        await ctx.send(embed=unmute_embed)

@testbot.command(aliases=["lock", "ld"])
@commands.has_permissions(manage_messages=True)
async def lockdown(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send(ctx.channel.mention + "is now set to lockdown mode.")

@testbot.command(aliases=["ul"])
@commands.has_permissions(manage_messages=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send("Lockdown mode is now removed for " + ctx.channel.mention)

@testbot.command(aliases=["sm", "slow"])
@commands.has_permissions(manage_messages=True)
async def slowmode(ctx, seconds : int):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"The slowmode is now set to {seconds} seconds.")

@testbot.command(pass_context=True)
@commands.has_permissions(manage_nicknames=True)
async def nickset(ctx, target : Optional[Member], nick):
        await target.edit(nick=nick)
        await ctx.send(f"Nickname changed for {target.mention}.")

@testbot.command(pass_context=True)
async def ping(ctx):
    """ Pong! """
    before = time.monotonic()
    pingembed = discord.Embed(title="Pong!🏓", description="", colour=discord.Colour.blue())
    message = await ctx.send(embed=pingembed)
    ping = (time.monotonic() - before) * 1000
    editpingembed = discord.Embed(title="Pong!🏓", description=f"`{int(ping)} ms`", colour=discord.Colour.blue())
    await message.edit(embed=editpingembed)

@testbot.command()
@commands.has_permissions(read_message_history=True)
async def firstmsg(ctx):
    async for message in ctx.channel.history(limit=1, oldest_first=True):
        await ctx.send(f"{message.content} - {message.author}")

@testbot.command()
@commands.has_permissions(read_message_history=True)
async def search(ctx, *, keyword: str):
    async for message in ctx.channel.history(limit=10, oldest_first=True):
        if keyword in message.content:
            embed = discord.Embed()
            embed.description = f"[{message.content}]({message.jump_url})"
            await ctx.send(embed=embed)

@testbot.command(aliases=["whois", "ui", "memberinfo", "user", "member"])
async def userinfo(ctx, target : Optional[Member]):
    target = target or ctx.author or discord.User
    target1 = target.mention.replace("<", "")
    target1 = target1.replace(">", "")
    target1 = target1.replace("@", "")
    target1 = target1.replace("!", "")
    target2 = await testbot.fetch_user(target1)
    if target == testbot.user:
        await ctx.send('Please use "&botinfo" to know more about me 🙂!')
    else:
        if target2.banner != None:
            embed = discord.Embed(title=target, description=f"{target.mention} | **__{discord.PartialEmoji(name='IDcard', id=868046662306770985, animated=False)} ID: __** {target.id}", colour = target.colour, timestamp=ctx.message.created_at)
            embed.add_field(name=f"__{discord.PartialEmoji(name='Top_Role', id=869212283941834764, animated=False)} Top role: __", value=target.top_role.mention, inline=True)
            embed.add_field(name=f"__{discord.PartialEmoji(name='Humanbot', id=869219560488829008, animated=False)} Bot: __", value = bool(target.bot), inline=True)
            embed.add_field(name=f"__{discord.PartialEmoji(name='Booster', id=869228744462708856, animated=False)} Booster: __", value=bool(target.premium_since), inline=True)
            embed.add_field(name=f"__{discord.PartialEmoji(name='UserJoin', id=869220716468387910, animated=False)} Joined on: __", value=datetime.date.strftime(target.joined_at, '%a, %d/%m/%Y %H:%M:%S'), inline=True)
            embed.add_field(name=f"__{discord.PartialEmoji(name='UserRegister', id=869222509902442528, animated=False)} Registered on: __", value=datetime.date.strftime(target.created_at, '%a, %d/%m/%Y %H:%M:%S'), inline=True)
            embed.add_field(name=f"__{discord.PartialEmoji(name='Activity', id=869225549917220874, animated=False)} Activity: __", value=f"{str(target.activity.type).split('.')[-1].title() if target.activity else 'N/A'} | {target.activity.name if target.activity else 'N/A'}", inline=False)
            embed.add_field(name=f"__{discord.PartialEmoji(name='Status', id=869226936197591070, animated=False)} Status: __", value=str(target.status).upper(), inline=True)
            embed.add_field(name=f"__{discord.PartialEmoji(name='Nickname', id=869227972496871466, animated=False)} Nickname: __", value=target.nick, inline=True)
            embed.add_field(name=f"__{discord.PartialEmoji(name='Roles', id=869214008077602856, animated=False)} Roles({len(target.roles)}): __",value='|'.join(role.mention for role in target.roles), inline=False)
            embed.add_field(name=f"__{discord.PartialEmoji(name='UserPerms', id=871662256709062676, animated=False)} Permissions: __", value=', '.join(f"{(perm[0])}".title() for perm in target.guild_permissions if perm[1]).replace("_", " "), inline=True)
            embed.add_field(name=f"__{discord.PartialEmoji(name='Badge', id=875656242855559199, animated=False)} Badges: __", value='\n'.join(((((((((((((((((((((((((((f'{x}'.replace("'", "")).replace(", ", ": ")).replace("(", "")).replace(")", "")).title()).replace("True", "✅")).replace("False", "❌")).replace("Staff", f"{discord.PartialEmoji(name='StaffDiscord', id=875627848482832464, animated=False)} Staff")).replace("Partner", f"{discord.PartialEmoji(name='PartnerDiscord', id=875628049595527208, animated=False)} Partner")).replace("Hypesquad", f"{discord.PartialEmoji(name='HypesquadDiscord', id=875638722526347305, animated=False)} Hypesquad")).replace("Bug_Hunter", f"{discord.PartialEmoji(name='BughunterDiscord', id=875638745360138262, animated=False)} Bug_Hunter")).replace("Hypesquad_Bravery", f"{discord.PartialEmoji(name='BraveryLogo', id=875638856517570601, animated=False)} Hypesquad_Bravery")).replace("Hypesquad_Brilliance", f"{discord.PartialEmoji(name='BrillianceLogo', id=875638884443226133,)} Hypesquad_Brilliance")).replace("Hypesquad_Balance", f"{discord.PartialEmoji(name='BalanceLogo', id=875638903456034826, animated=False)} Hypesquad_Balance")).replace("Early_Supporter", f"{discord.PartialEmoji(name='EarlySupporter', id=875639057697353728, animated=False)} Early_Supporter")).replace("Team_User", f"{discord.PartialEmoji(name='TeamUser', id=875639157622460416, animated=False)} Team_User")).replace("System", f"{discord.PartialEmoji(name='SystemDiscord', id=875639240006959105, animated=False)} System")).replace("Bug_Hunter_Level_2", f"{discord.PartialEmoji(name='BugHunterlv2', id=875639279810912266, animated=False)} Bug_Hunter_Level_2")).replace("Verified_Bot", f"{discord.PartialEmoji(name='BotUser', id=875639837032583209, animated=False)} Verified_Bot")).replace("Verified_Bot_Developer", f"{discord.PartialEmoji(name='VerifiedBotdev', id=875656092120674346, animated=False)} Verified_Bot_Developer")).replace(f"{discord.PartialEmoji(name='HypesquadDiscord', id=875638722526347305, animated=False)} {discord.PartialEmoji(name='BraveryLogo', id=875638856517570601, animated=False)} Hypesquad_Bravery", f"{discord.PartialEmoji(name='BraveryLogo', id=875638856517570601, animated=False)} Hypesquad_Bravery")).replace(f"{discord.PartialEmoji(name='HypesquadDiscord', id=875638722526347305, animated=False)} {discord.PartialEmoji(name='BrillianceLogo', id=875638884443226133,)} Hypesquad_Brilliance", f"{discord.PartialEmoji(name='BrillianceLogo', id=875638884443226133,)} Hypesquad_Brilliance")).replace(f"{discord.PartialEmoji(name='HypesquadDiscord', id=875638722526347305, animated=False)} {discord.PartialEmoji(name='BalanceLogo', id=875638903456034826, animated=False)} Hypesquad_Balance", f"{discord.PartialEmoji(name='BalanceLogo', id=875638903456034826, animated=False)} Hypesquad_Balance")).replace(f"{discord.PartialEmoji(name='BughunterDiscord', id=875638745360138262, animated=False)} {discord.PartialEmoji(name='BugHunterlv2', id=875639279810912266, animated=False)} Bug_Hunter_Level_2", f"{discord.PartialEmoji(name='BugHunterlv2', id=875639279810912266, animated=False)} Bug_Hunter_Level_2")).replace(f"{discord.PartialEmoji(name='BotUser', id=875639837032583209, animated=False)} {discord.PartialEmoji(name='VerifiedBotdev', id=875656092120674346, animated=False)} Verified_Bot_Developer", f"{discord.PartialEmoji(name='VerifiedBotdev', id=875656092120674346, animated=False)} Verified_Bot_Developer")).replace("_", " ")).replace(f"{discord.PartialEmoji(name='HypesquadDiscord', id=875638722526347305, animated=False)} Hypesquad", f"{discord.PartialEmoji(name='HypesquadDiscord', id=875638722526347305, animated=False)} Hypesquad Events") for x in target.public_flags), inline=False)
            embed.set_thumbnail(url=target.avatar.url)
            embed.set_image(url = target2.banner)
            embed.set_footer(icon_url=ctx.author.avatar.url, text=f"Requested by {ctx.author.name}")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title=target, description=f"{target.mention} | **__{discord.PartialEmoji(name='IDcard', id=868046662306770985, animated=False)} ID: __** {target.id}", colour = target.colour, timestamp=ctx.message.created_at)
            embed.add_field(name=f"__{discord.PartialEmoji(name='Top_Role', id=869212283941834764, animated=False)} Top role: __", value=target.top_role.mention, inline=True)
            embed.add_field(name=f"__{discord.PartialEmoji(name='Humanbot', id=869219560488829008, animated=False)} Bot: __", value = bool(target.bot), inline=True)
            embed.add_field(name=f"__{discord.PartialEmoji(name='Booster', id=869228744462708856, animated=False)} Booster: __", value=bool(target.premium_since), inline=True)
            embed.add_field(name=f"__{discord.PartialEmoji(name='UserJoin', id=869220716468387910, animated=False)} Joined on: __", value=datetime.date.strftime(target.joined_at, '%a, %d/%m/%Y %H:%M:%S'), inline=True)
            embed.add_field(name=f"__{discord.PartialEmoji(name='UserRegister', id=869222509902442528, animated=False)} Registered on: __", value=datetime.date.strftime(target.created_at, '%a, %d/%m/%Y %H:%M:%S'), inline=True)
            embed.add_field(name=f"__{discord.PartialEmoji(name='Activity', id=869225549917220874, animated=False)} Activity: __", value=f"{str(target.activity.type).split('.')[-1].title() if target.activity else 'N/A'} | {target.activity.name if target.activity else 'N/A'}", inline=False)
            embed.add_field(name=f"__{discord.PartialEmoji(name='Status', id=869226936197591070, animated=False)} Status: __", value=str(target.status).upper(), inline=True)
            embed.add_field(name=f"__{discord.PartialEmoji(name='Nickname', id=869227972496871466, animated=False)} Nickname: __", value=target.nick, inline=True)
            embed.add_field(name=f"__{discord.PartialEmoji(name='Roles', id=869214008077602856, animated=False)} Roles({len(target.roles)}): __",value='|'.join(role.mention for role in target.roles), inline=False)
            embed.add_field(name=f"__{discord.PartialEmoji(name='UserPerms', id=871662256709062676, animated=False)} Permissions: __", value=', '.join(f"{(perm[0])}".title() for perm in target.guild_permissions if perm[1]).replace("_", " "), inline=True)
            embed.add_field(name=f"__{discord.PartialEmoji(name='Badge', id=875656242855559199, animated=False)} Badges: __", value='\n'.join(((((((((((((((((((((((((((f'{x}'.replace("'", "")).replace(", ", ": ")).replace("(", "")).replace(")", "")).title()).replace("True", "✅")).replace("False", "❌")).replace("Staff", f"{discord.PartialEmoji(name='StaffDiscord', id=875627848482832464, animated=False)} Staff")).replace("Partner", f"{discord.PartialEmoji(name='PartnerDiscord', id=875628049595527208, animated=False)} Partner")).replace("Hypesquad", f"{discord.PartialEmoji(name='HypesquadDiscord', id=875638722526347305, animated=False)} Hypesquad")).replace("Bug_Hunter", f"{discord.PartialEmoji(name='BughunterDiscord', id=875638745360138262, animated=False)} Bug_Hunter")).replace("Hypesquad_Bravery", f"{discord.PartialEmoji(name='BraveryLogo', id=875638856517570601, animated=False)} Hypesquad_Bravery")).replace("Hypesquad_Brilliance", f"{discord.PartialEmoji(name='BrillianceLogo', id=875638884443226133,)} Hypesquad_Brilliance")).replace("Hypesquad_Balance", f"{discord.PartialEmoji(name='BalanceLogo', id=875638903456034826, animated=False)} Hypesquad_Balance")).replace("Early_Supporter", f"{discord.PartialEmoji(name='EarlySupporter', id=875639057697353728, animated=False)} Early_Supporter")).replace("Team_User", f"{discord.PartialEmoji(name='TeamUser', id=875639157622460416, animated=False)} Team_User")).replace("System", f"{discord.PartialEmoji(name='SystemDiscord', id=875639240006959105, animated=False)} System")).replace("Bug_Hunter_Level_2", f"{discord.PartialEmoji(name='BugHunterlv2', id=875639279810912266, animated=False)} Bug_Hunter_Level_2")).replace("Verified_Bot", f"{discord.PartialEmoji(name='BotUser', id=875639837032583209, animated=False)} Verified_Bot")).replace("Verified_Bot_Developer", f"{discord.PartialEmoji(name='VerifiedBotdev', id=875656092120674346, animated=False)} Verified_Bot_Developer")).replace(f"{discord.PartialEmoji(name='HypesquadDiscord', id=875638722526347305, animated=False)} {discord.PartialEmoji(name='BraveryLogo', id=875638856517570601, animated=False)} Hypesquad_Bravery", f"{discord.PartialEmoji(name='BraveryLogo', id=875638856517570601, animated=False)} Hypesquad_Bravery")).replace(f"{discord.PartialEmoji(name='HypesquadDiscord', id=875638722526347305, animated=False)} {discord.PartialEmoji(name='BrillianceLogo', id=875638884443226133,)} Hypesquad_Brilliance", f"{discord.PartialEmoji(name='BrillianceLogo', id=875638884443226133,)} Hypesquad_Brilliance")).replace(f"{discord.PartialEmoji(name='HypesquadDiscord', id=875638722526347305, animated=False)} {discord.PartialEmoji(name='BalanceLogo', id=875638903456034826, animated=False)} Hypesquad_Balance", f"{discord.PartialEmoji(name='BalanceLogo', id=875638903456034826, animated=False)} Hypesquad_Balance")).replace(f"{discord.PartialEmoji(name='BughunterDiscord', id=875638745360138262, animated=False)} {discord.PartialEmoji(name='BugHunterlv2', id=875639279810912266, animated=False)} Bug_Hunter_Level_2", f"{discord.PartialEmoji(name='BugHunterlv2', id=875639279810912266, animated=False)} Bug_Hunter_Level_2")).replace(f"{discord.PartialEmoji(name='BotUser', id=875639837032583209, animated=False)} {discord.PartialEmoji(name='VerifiedBotdev', id=875656092120674346, animated=False)} Verified_Bot_Developer", f"{discord.PartialEmoji(name='VerifiedBotdev', id=875656092120674346, animated=False)} Verified_Bot_Developer")).replace("_", " ")).replace(f"{discord.PartialEmoji(name='HypesquadDiscord', id=875638722526347305, animated=False)} Hypesquad", f"{discord.PartialEmoji(name='HypesquadDiscord', id=875638722526347305, animated=False)} Hypesquad Events") for x in target.public_flags), inline=False)
            embed.set_thumbnail(url=target.avatar.url)
            embed.set_footer(icon_url=ctx.author.avatar.url, text=f"Requested by {ctx.author.name}")
            await ctx.send(embed=embed)

@testbot.command(aliases=["bot"])
async def botinfo(ctx):
    target = ctx.guild.me
    botappinfo = await testbot.application_info()
    botembed = discord.Embed(title=target, description=f"{target.mention} | **__{discord.PartialEmoji(name='IDcard', id=868046662306770985, animated=False)} ID: __** {target.id}", colour = target.colour, timestamp=ctx.message.created_at)
    botembed.add_field(name=f"__{discord.PartialEmoji(name='Top_Role', id=869212283941834764, animated=False)} Top role: __", value=target.top_role.mention, inline=True)
    botembed.add_field(name=f"__{discord.PartialEmoji(name='Humanbot', id=869219560488829008, animated=False)} Bot: __", value = bool(target.bot), inline=True)
    botembed.add_field(name=f"__{discord.PartialEmoji(name='Booster', id=869228744462708856, animated=False)} Booster: __", value=bool(target.premium_since), inline=True)
    botembed.add_field(name=f"__{discord.PartialEmoji(name='UserJoin', id=869220716468387910, animated=False)} Joined: __", value=datetime.date.strftime(target.joined_at, '%a, %d/%m/%Y %H:%M:%S'), inline=True)
    botembed.add_field(name=f"__{discord.PartialEmoji(name='UserRegister', id=869222509902442528, animated=False)} Registered: __", value=datetime.date.strftime(target.created_at, '%a, %d/%m/%Y %H:%M:%S'), inline=True)
    botembed.add_field(name=f"__{discord.PartialEmoji(name='Activity', id=869225549917220874, animated=False)} Activity: __", value=f"{str(target.activity.type).split('.')[-1].title() if target.activity else 'N/A'} | {target.activity.name if target.activity else 'N/A'}", inline=False)
    botembed.add_field(name=f"__{discord.PartialEmoji(name='Status', id=869226936197591070, animated=False)}  Status: __", value=str(target.status).upper(), inline=True)
    botembed.add_field(name=f"__{discord.PartialEmoji(name='Nickname', id=869227972496871466, animated=False)} Nickname: __", value=target.nick, inline=True)
    botembed.add_field(name=f"__{discord.PartialEmoji(name='Roles', id=869214008077602856, animated=False)} Roles({len(target.roles)}): __",value='|'.join(role.mention for role in target.roles), inline=False)
    botembed.add_field(name=f"__{discord.PartialEmoji(name='DiscordPython', id=876495517960527912, animated=False)} Discord.py version: __", value=((f"{discord.__version__}| {discord.version_info[3]} release").title()).replace("Final", "Stable"), inline=True)
    botembed.add_field(name=f"__{discord.PartialEmoji(name='Server', id=876495661179211816, animated=False)} Servers: __", value=len(testbot.guilds), inline=True)
    botembed.add_field(name=f"__{discord.PartialEmoji(name='UserPerms', id=871662256709062676, animated=False)} Permissions: __", value=', '.join(f"{(perm[0])}".title() for perm in target.guild_permissions if perm[1]).replace("_", " "), inline=False)
    botembed.add_field(name=f"__{discord.PartialEmoji(name='Badge', id=875656242855559199, animated=False)} Badges: __", value='\n'.join(((((((((((((((((((((((((((f'{x}'.replace("'", "")).replace(", ", ": ")).replace("(", "")).replace(")", "")).title()).replace("True", "✅")).replace("False", "❌")).replace("Staff", f"{discord.PartialEmoji(name='StaffDiscord', id=875627848482832464, animated=False)} Staff")).replace("Partner", f"{discord.PartialEmoji(name='PartnerDiscord', id=875628049595527208, animated=False)} Partner")).replace("Hypesquad", f"{discord.PartialEmoji(name='HypesquadDiscord', id=875638722526347305, animated=False)} Hypesquad")).replace("Bug_Hunter", f"{discord.PartialEmoji(name='BughunterDiscord', id=875638745360138262, animated=False)} Bug_Hunter")).replace("Hypesquad_Bravery", f"{discord.PartialEmoji(name='BraveryLogo', id=875638856517570601, animated=False)} Hypesquad_Bravery")).replace("Hypesquad_Brilliance", f"{discord.PartialEmoji(name='BrillianceLogo', id=875638884443226133,)} Hypesquad_Brilliance")).replace("Hypesquad_Balance", f"{discord.PartialEmoji(name='BalanceLogo', id=875638903456034826, animated=False)} Hypesquad_Balance")).replace("Early_Supporter", f"{discord.PartialEmoji(name='EarlySupporter', id=875639057697353728, animated=False)} Early_Supporter")).replace("Team_User", f"{discord.PartialEmoji(name='TeamUser', id=875639157622460416, animated=False)} Team_User")).replace("System", f"{discord.PartialEmoji(name='SystemDiscord', id=875639240006959105, animated=False)} System")).replace("Bug_Hunter_Level_2", f"{discord.PartialEmoji(name='BugHunterlv2', id=875639279810912266, animated=False)} Bug_Hunter_Level_2")).replace("Verified_Bot", f"{discord.PartialEmoji(name='BotUser', id=875639837032583209, animated=False)} Verified_Bot")).replace("Verified_Bot_Developer", f"{discord.PartialEmoji(name='VerifiedBotdev', id=875656092120674346, animated=False)} Verified_Bot_Developer")).replace(f"{discord.PartialEmoji(name='HypesquadDiscord', id=875638722526347305, animated=False)} {discord.PartialEmoji(name='BraveryLogo', id=875638856517570601, animated=False)} Hypesquad_Bravery", f"{discord.PartialEmoji(name='BraveryLogo', id=875638856517570601, animated=False)} Hypesquad_Bravery")).replace(f"{discord.PartialEmoji(name='HypesquadDiscord', id=875638722526347305, animated=False)} {discord.PartialEmoji(name='BrillianceLogo', id=875638884443226133,)} Hypesquad_Brilliance", f"{discord.PartialEmoji(name='BrillianceLogo', id=875638884443226133,)} Hypesquad_Brilliance")).replace(f"{discord.PartialEmoji(name='HypesquadDiscord', id=875638722526347305, animated=False)} {discord.PartialEmoji(name='BalanceLogo', id=875638903456034826, animated=False)} Hypesquad_Balance", f"{discord.PartialEmoji(name='BalanceLogo', id=875638903456034826, animated=False)} Hypesquad_Balance")).replace(f"{discord.PartialEmoji(name='BughunterDiscord', id=875638745360138262, animated=False)} {discord.PartialEmoji(name='BugHunterlv2', id=875639279810912266, animated=False)} Bug_Hunter_Level_2", f"{discord.PartialEmoji(name='BugHunterlv2', id=875639279810912266, animated=False)} Bug_Hunter_Level_2")).replace(f"{discord.PartialEmoji(name='BotUser', id=875639837032583209, animated=False)} {discord.PartialEmoji(name='VerifiedBotdev', id=875656092120674346, animated=False)} Verified_Bot_Developer", f"{discord.PartialEmoji(name='VerifiedBotdev', id=875656092120674346, animated=False)} Verified_Bot_Developer")).replace("_", " ")).replace(f"{discord.PartialEmoji(name='HypesquadDiscord', id=875638722526347305, animated=False)} Hypesquad", f"{discord.PartialEmoji(name='HypesquadDiscord', id=875638722526347305, animated=False)} Hypesquad Events") for x in target.public_flags), inline=False)
    botembed.add_field(name=f"__{discord.PartialEmoji(name='Botcreator', id=876496012393476116, animated=False)} Creator: __", value=botappinfo.owner, inline=True)
    botembed.add_field(name="__Codename: __", value=botappinfo.name, inline=True)
    botembed.set_thumbnail(url=botappinfo.icon.url)
    botembed.set_footer(icon_url=ctx.author.avatar.url, text=f"Requested by {ctx.author.name}")
    await ctx.send(embed=botembed)

@testbot.command(aliases=["si","guildinfo", "guild", "server"])
@commands.has_permissions(embed_links=True)
async def serverinfo(ctx):
    guild = ctx.guild
    statuses = [len(list(filter(lambda m: str(m.status) == "online", ctx.guild.members))),
					len(list(filter(lambda m: str(m.status) == "idle", ctx.guild.members))),
					len(list(filter(lambda m: str(m.status) == "dnd", ctx.guild.members))),
					len(list(filter(lambda m: str(m.status) == "offline", ctx.guild.members)))]
    guildembed = discord.Embed(title=guild.name, description=f"**{discord.PartialEmoji(name='Serverdesc', id=871586961188610079, animated=False)} Description: ** {guild.description}", colour = ctx.guild.owner.colour, timestamp=ctx.message.created_at)
    guildembed.add_field(name=f"{discord.PartialEmoji(name='ServerID', id=871583345363021854, animated=False)} ID: ", value=guild.id, inline=True)
    guildembed.add_field(name=f"{discord.PartialEmoji(name='Servercreation', id=871591082260058123, animated=False)} Created on: ", value = datetime.date.strftime(guild.created_at, '%a, %d/%m/%Y %H:%M:%S'), inline=True)
    guildembed.add_field(name=f"{discord.PartialEmoji(name='Serverroles', id=871615599091007519, animated=False)} Roles({len(guild.roles)}): ", value='|'.join(role.mention for role in guild.roles), inline=False)
    guildembed.set_thumbnail(url=guild.icon.url)
    guildembed.add_field(name=f"{discord.PartialEmoji(name='Emojiblob', id=871715724693999677, animated=False)} Emojis({int(len(guild.emojis))}): ", value=f"{''.join(str(emote) for emote in guild.emojis[0:32])} and more", inline=False)
    guildembed.add_field(name=f"{discord.PartialEmoji(name='Membercount', id=871616325108248586, animated=False)} Membercount: ", value=f"`{guild.member_count}` Members", inline=True)
    guildembed.add_field(name=f"{discord.PartialEmoji(name='Human', id=871617153495859230, animated=False)} Humans: ", value =f"`{len(list(filter(lambda m: not m.bot, guild.members)))}` Human(s)", inline=True)
    guildembed.add_field(name=f"{discord.PartialEmoji(name='Bot', id=871620978462048317, animated=False)} Bots: ", value=f"`{len(list(filter(lambda m: m.bot, guild.members)))}` Bot(s)", inline=True)
    guildembed.add_field(name=f"{discord.PartialEmoji(name='Banhammer', id=871624353681399898, animated=False)} Member bans: ", value=len(await guild.bans()), inline=True)
    guildembed.add_field(name=f"{discord.PartialEmoji(name='Nitroboost', id=871624854288351242, animated=False)} Nitro boost level: ", value=f"Level {guild.premium_tier}", inline=True)
    guildembed.add_field(name=f"{discord.PartialEmoji(name='Booster', id=869228744462708856, animated=False)} Boosts: ", value=guild.premium_subscription_count, inline=True)
    guildembed.add_field(name=f"{discord.PartialEmoji(name='Statuses', id=872498901842788453, animated=False)} Statuses: ", value=f"{discord.PartialEmoji(name='Useronline', id=871985942741782539, animated=False)} {statuses[0]} {discord.PartialEmoji(name='Useridle', id=871985959737102367, animated=False)} {statuses[1]} {discord.PartialEmoji(name='Userdnd', id=871986111843532852, animated=False)} {statuses[2]} {discord.PartialEmoji(name='Useroffline', id=871986172346376252, animated=False)} {statuses[3]}", inline=True)
    guildembed.add_field(name=f"{discord.PartialEmoji(name='Serververify', id=871978151058751528, animated=False)} Verification level: ", value=str(guild.verification_level).title(), inline=True)
    guildembed.add_field(name=f"{discord.PartialEmoji(name='Textchannel', id=871628497414684682, animated=False)} Text channels({len(guild.text_channels)}): ", value='|'.join(channel.mention for channel in guild.text_channels), inline=False)
    guildembed.add_field(name=f"{discord.PartialEmoji(name='Voicechannel', id=871632753186177055, animated=False)} Voice channels({len(guild.voice_channels)}): ", value='|'.join(channel.mention for channel in guild.voice_channels), inline=False)
    guildembed.add_field(name=f"{discord.PartialEmoji(name='Category', id=871636437609639977, animated=False)} Channel categories({len(guild.categories)}): ", value=' | '.join(category.mention for category in guild.categories), inline=False)
    guildembed.add_field(name=f"{discord.PartialEmoji(name='Serverregion', id=871638602843553792, animated=False)} Region: ", value=str(guild.region).title(), inline=True)
    guildembed.add_field(name=f"{discord.PartialEmoji(name='Serverowner', id=871641007400300574, animated=False)} Owner: ", value=guild.owner.mention, inline=True)
    guildembed.add_field(name=f"{discord.PartialEmoji(name='Serverfeature', id=875656634280579082, animated=False)} Features: ", value='\n'.join(f"{discord.PartialEmoji(name='MemberEnter', id=875359683517509633, animated=False)} **`{x}`**".replace("_", " ") for x in ctx.guild.features), inline=False)
    guildembed.set_footer(icon_url=ctx.author.avatar.url, text=f"Requested by {ctx.author.name}")
    await ctx.send(embed=guildembed)

@testbot.command(aliases=["el", "emoji", "emote", "emotelist"])
async def emojilist(ctx):
    guild = ctx.guild
    await ctx.send(f"{''.join(str(emote) for emote in guild.emojis)}")

@testbot.command()
@commands.has_permissions(manage_emojis_and_stickers=True)
async def addemoji(ctx, url:str, *, name):
    guild = ctx.guild
    async with aiohttp.ClientSession() as ses:
        async with ses.get(url) as r:
            try:
                imgorgif = BytesIO(await r.read())
                bvalue = imgorgif.getvalue()
                if r.status in range(200, 299):
                    emoji = await guild.create_custom_emoji(image=bvalue, name=name)
                    await ctx.send("Successfully added the given emoji!\n" + f"{emoji}")
                    await ses.close()
                else:
                    await ctx.send(f"An error occured: {r.status}")
            except discord.HTTPException:
                await ctx.send("Error: The file is too large(must be under 256 kb in size)")

@testbot.command()
@commands.has_permissions(manage_emojis_and_stickers=True)
async def delemoji(ctx, emoji: discord.Emoji):
    await ctx.send("Successfully removed the given emoji!\n" + f"{emoji}")
    await emoji.delete()

@testbot.command(aliases=["pfp", "profilepic", "profile"])
async def avatar(ctx, target : Optional[Member]):
    if not target:
        target = ctx.message.author
    avatar = target.avatar.url
    embed = discord.Embed(title=target.name, description=target.mention, colour=target.colour)
    embed.set_image(url=avatar)
    embed.set_footer(icon_url=ctx.author.avatar.url, text=f"Requested by {ctx.author.name}")
    await ctx.send(embed=embed)

@testbot.command(aliases=['8ball'])
async def eightball(ctx, *, question):
    await ctx.send(f':8ball: {random.choice(outputs)}')

@testbot.command(pass_context=True)
@commands.has_permissions(manage_roles=True)
async def giverole(ctx, emoji, role : discord.Role, *, rolemessage):
    emb = discord.Embed(title='Reaction role!', description=rolemessage, colour = role.colour)
    emb.set_footer(text="This reaction embed will expire after 30 days! ")
    rolemsg = await ctx.channel.send(embed=emb)
    await rolemsg.add_reaction(emoji)

    with open('giverole.json') as json_file:
        data = json.load(json_file)

        new_react_role = {'role_name' : role.name,
            'role_id' : role.id,
            'emoji' : emoji,
            'message_id' : rolemsg.id}

        data.append(new_react_role)

    with open('giverole.json','w') as f:
        json.dump(data,f,indent=4)
    await asyncio.sleep(2592000)
    embvone = discord.Embed(title='Reactions role!', description=rolemessage, colour = discord.Colour.magenta())
    embvone.set_footer(text="This reaction embed has expired, ask the admin to make a new one!")
    await rolemsg.edit(embed=embvone)
    with open('giverole.json', 'w') as f:
        data.remove(new_react_role)
        json.dump(data,f,indent=4)

@testbot.command()
async def meme(ctx):
    memeApi = urllib.request.urlopen('https://meme-api.herokuapp.com/gimme')
    memeData = json.load(memeApi)
    memeUrl = memeData['url']
    memeName = memeData['title']
    memeOP = memeData['author']
    memeSub = memeData['subreddit']
    memeLink = memeData['postLink']

    em = discord.Embed(title=memeName, url=memeLink, description=f"u/{memeOP}", colour=discord.Colour.random())
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

    em = discord.Embed(title=name, url=f"https://www.reddit.com{posturl}")
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

@testbot.command(aliases=["ttt"])
async def tictactoe(ctx, p1 : discord.Member, p2 : discord.Member):
    global player1
    global player2
    global turn
    global gameOver
    global count

    if gameOver:
        global board
        await ctx.send(embed = discord.Embed(title="To see what each square's number is type &board"))
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

@testbot.command(aliases=["tictactoeplace"])
async def tttplace(ctx, pos : int):
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
        await ctx.send('⭕There are no ongoing tictactoe matches going on. Use the "&tictactoe" command to start a new one!❌')

@testbot.command(aliases=["tictactoeend"])
async def tttend(ctx):
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

@testbot.command(aliases=["tictactoeboard"])
async def tttboard(ctx):
    embed = discord.Embed(title="What each square's number is", description = ":one::two::three:\n:four::five::six:\n:seven::eight::nine:")
    await ctx.send(embed = embed)

@tictactoe.error
async def tictactoe_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention two players for this command")
    if isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to mention/ping players (e.g <@839532962600714280>).")

@tttplace.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please enter the position you'd like to mark")
    if isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to enter an integer.")


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
    await ctx.send(f"New category {category.name} has been created!")

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
    await ctx.send(f"New channel {channel.name} has been created!")

@testbot.command(aliases=['connectfour', "c4"])
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

@testbot.command(aliases=['connect4place', 'c4p', 'connectfourplace'])
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
        await ctx.send("Please start with &connect4 command.")

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

@testbot.command(aliases=["connect4stop", 'c4s', 'connectfourstop'])
async def c4stop(ctx):
    global gameOver
    if not gameOver:
        gameOver = True
        await ctx.send("The game has been stopped.")
    else:
        await ctx.send("The Game has ended.")

@testbot.command(aliases=["connect4mode", "c4m", "connectfourmode"])
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

for folder in os.listdir("Cogsforbot"):
    if os.path.exists(os.path.join("Cogsforbot", folder, "cog.py")):
        testbot.load_extension(f"Cogsforbot.{folder}.cog")

DISCORD_TOKEN = os.getenv("TOKEN")
testbot.run(DISCORD_TOKEN)
