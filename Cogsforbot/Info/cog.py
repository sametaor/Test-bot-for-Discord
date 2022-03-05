import nextcord
import time
import datetime
from typing import Optional
from nextcord import Spotify, Member
from nextcord.ext import commands

class Information(commands.Cog):
    """Get detailed stats for Discord"""
    COG_EMOJI = 'ℹ'
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True)
    async def ping(ctx):
        """ Pong! """
        before = time.monotonic()
        pingembed = nextcord.Embed(title="Pong!🏓", description="", colour=nextcord.Colour.blue())
        message = await ctx.send(embed=pingembed)
        ping = (time.monotonic() - before) * 1000
        editpingembed = nextcord.Embed(title="Pong!🏓", description=f"`{int(ping)} ms`", colour=nextcord.Colour.blue())
        await message.edit(embed=editpingembed)
    
    @commands.command(pass_context=True)
    async def spotify(self, ctx, user: nextcord.Member = None):
        if user == None:
            user = ctx.author
            pass
        if user.activities:
            for activity in user.activities:
                if isinstance(activity, Spotify):
                    embed = nextcord.Embed(title = f"{user.name}'s Spotify", description = "Listening to{}".format(activity.title), color = 0xC902FF)
                    embed.set_thumbnail(url=activity.album_cover_url)
                    embed.add_field(name="Artist", value=activity.artist)
                    embed.add_field(name="Album", value=activity.album)
                    m1, s1 = divmod(int(activity.duration.seconds), 60)
                    song_length = f'{m1}:{s1}'
                    embed.add_field(name="**Song Length:**", value=song_length)
                    embed.set_footer(text="Song started at {}".format(activity.created_at.strftime("%H:%M")))
                    await ctx.send(embed=embed)
    
    @commands.command(pass_context=True, aliases=["whois", "ui", "memberinfo", "user", "member"])
    async def userinfo(self, ctx, target : Optional[Member]):
        target = target or ctx.author or nextcord.User
        target1 = target.mention.replace("<", "")
        target1 = target1.replace(">", "")
        target1 = target1.replace("@", "")
        target1 = target1.replace("!", "")
        target2 = await self.bot.fetch_user(target1)
        if target == self.bot.user:
            await ctx.send(nextcord.Embed(title="Bot Info", description = 'Please use "&botinfo" to know more about me 🙂!', colour=self.bot.user.colour))
        else:
            userembed = nextcord.Embed(title=target, description=f"{target.mention} | **__{nextcord.PartialEmoji(name='IDcard', id=868046662306770985, animated=False)} ID: __** {target.id}", colour = target.colour, timestamp=ctx.message.created_at)
            userembed.add_field(name=f"__{nextcord.PartialEmoji(name='Top_Role', id=869212283941834764, animated=False)} Top role: __", value=target.top_role.mention, inline=True)
            userembed.add_field(name=f"__{nextcord.PartialEmoji(name='Humanbot', id=869219560488829008, animated=False)} Bot: __", value = bool(target.bot), inline=True)
            userembed.add_field(name=f"__{nextcord.PartialEmoji(name='Booster', id=869228744462708856, animated=False)} Booster: __", value=bool(target.premium_since), inline=True)
            userembed.add_field(name=f"__{nextcord.PartialEmoji(name='UserJoin', id=869220716468387910, animated=False)} Joined on: __", value=datetime.date.strftime(target.joined_at, '%a, %d/%m/%Y %H:%M:%S'), inline=True)
            userembed.add_field(name=f"__{nextcord.PartialEmoji(name='UserRegister', id=869222509902442528, animated=False)} Registered on: __", value=datetime.date.strftime(target.created_at, '%a, %d/%m/%Y %H:%M:%S'), inline=True)
            userembed.add_field(name=f"__{nextcord.PartialEmoji(name='Activity', id=869225549917220874, animated=False)} Activity: __", value=f"{str(target.activity.type).split('.')[-1].title() if target.activity else 'N/A'} | {target.activity.name if target.activity else 'N/A'}", inline=False)
            userembed.add_field(name=f"__{nextcord.PartialEmoji(name='Status', id=869226936197591070, animated=False)} Status: __", value=str(target.status).upper(), inline=True)
            userembed.add_field(name=f"__{nextcord.PartialEmoji(name='Nickname', id=869227972496871466, animated=False)} Nickname: __", value=target.nick, inline=True)
            userembed.add_field(name=f"__{nextcord.PartialEmoji(name='Roles', id=869214008077602856, animated=False)} Roles({len(target.roles)}): __",value='|'.join(role.mention for role in target.roles), inline=False)
            userembed.add_field(name=f"__{nextcord.PartialEmoji(name='UserPerms', id=871662256709062676, animated=False)} Permissions: __", value=', '.join(f"{(perm[0])}".title() for perm in target.guild_permissions if perm[1]).replace("_", " "), inline=True)
            userembed.add_field(name=f"__{nextcord.PartialEmoji(name='Badge', id=875656242855559199, animated=False)} Badges: __", value='\n'.join(((((((((((((((((((((((((((((f'{x}'.replace("'", "")).replace(", ", ": ")).replace("(", "")).replace(")", "")).title()).replace("True", "✅")).replace("False", "❌")).replace("Staff", f"{nextcord.PartialEmoji(name='StaffDiscord', id=875627848482832464, animated=False)} Staff")).replace("Partner", f"{nextcord.PartialEmoji(name='PartnerDiscord', id=875628049595527208, animated=False)} Partner")).replace("Hypesquad", f"{nextcord.PartialEmoji(name='HypesquadDiscord', id=875638722526347305, animated=False)} Hypesquad")).replace("Bug_Hunter", f"{nextcord.PartialEmoji(name='BughunterDiscord', id=875638745360138262, animated=False)} Bug_Hunter")).replace("Hypesquad_Bravery", f"{nextcord.PartialEmoji(name='BraveryLogo', id=875638856517570601, animated=False)} Hypesquad_Bravery")).replace("Hypesquad_Brilliance", f"{nextcord.PartialEmoji(name='BrillianceLogo', id=875638884443226133,)} Hypesquad_Brilliance")).replace("Hypesquad_Balance", f"{nextcord.PartialEmoji(name='BalanceLogo', id=875638903456034826, animated=False)} Hypesquad_Balance")).replace("Early_Supporter", f"{nextcord.PartialEmoji(name='EarlySupporter', id=875639057697353728, animated=False)} Early_Supporter")).replace("Team_User", f"{nextcord.PartialEmoji(name='TeamUser', id=875639157622460416, animated=False)} Team_User")).replace("System", f"{nextcord.PartialEmoji(name='SystemDiscord', id=875639240006959105, animated=False)} System")).replace("Bug_Hunter_Level_2", f"{nextcord.PartialEmoji(name='BugHunterlv2', id=875639279810912266, animated=False)} Bug_Hunter_Level_2")).replace("Verified_Bot", f"{nextcord.PartialEmoji(name='BotUser', id=875639837032583209, animated=False)} Verified_Bot")).replace("Verified_Bot_Developer", f"{nextcord.PartialEmoji(name='VerifiedBotdev', id=875656092120674346, animated=False)} Verified_Bot_Developer")).replace(f"{nextcord.PartialEmoji(name='HypesquadDiscord', id=875638722526347305, animated=False)} {nextcord.PartialEmoji(name='BraveryLogo', id=875638856517570601, animated=False)} Hypesquad_Bravery", f"{nextcord.PartialEmoji(name='BraveryLogo', id=875638856517570601, animated=False)} Hypesquad_Bravery")).replace(f"{nextcord.PartialEmoji(name='HypesquadDiscord', id=875638722526347305, animated=False)} {nextcord.PartialEmoji(name='BrillianceLogo', id=875638884443226133,)} Hypesquad_Brilliance", f"{nextcord.PartialEmoji(name='BrillianceLogo', id=875638884443226133,)} Hypesquad_Brilliance")).replace(f"{nextcord.PartialEmoji(name='HypesquadDiscord', id=875638722526347305, animated=False)} {nextcord.PartialEmoji(name='BalanceLogo', id=875638903456034826, animated=False)} Hypesquad_Balance", f"{nextcord.PartialEmoji(name='BalanceLogo', id=875638903456034826, animated=False)} Hypesquad_Balance")).replace(f"{nextcord.PartialEmoji(name='BughunterDiscord', id=875638745360138262, animated=False)} {nextcord.PartialEmoji(name='BugHunterlv2', id=875639279810912266, animated=False)} Bug_Hunter_Level_2", f"{nextcord.PartialEmoji(name='BugHunterlv2', id=875639279810912266, animated=False)} Bug_Hunter_Level_2")).replace(f"{nextcord.PartialEmoji(name='BotUser', id=875639837032583209, animated=False)} {nextcord.PartialEmoji(name='VerifiedBotdev', id=875656092120674346, animated=False)} Verified_Bot_Developer", f"{nextcord.PartialEmoji(name='VerifiedBotdev', id=875656092120674346, animated=False)} Verified_Bot_Developer")).replace("_", " ")).replace(f"{nextcord.PartialEmoji(name='HypesquadDiscord', id=875638722526347305, animated=False)} Hypesquad", f"{nextcord.PartialEmoji(name='HypesquadDiscord', id=875638722526347305, animated=False)} Hypesquad Events")).replace("Discord Certified Moderator", f"{nextcord.PartialEmoji(name='CertifiedModerator', id=942802702092599316, animated=False)} Discord Certified Moderator")).replace("Known Spammer", f"{nextcord.PartialEmoji(name='KnownSpammer', id=942807033781055588, animated=False)} Known Spammer") for x in target.public_flags), inline=False)
            userembed.set_thumbnail(url=target.avatar.url)
            userembed.set_footer(icon_url=ctx.author.avatar.url, text=f"Requested by {ctx.author.name}")
            for activity in target.activities:
                if isinstance(activity, Spotify):
                    userembed.add_field(name=f"{nextcord.PartialEmoji(name='Spotify', id=942800717440254072, animated=False)}__Spotify Activity: __", value= f"Song Name: [{activity.title}]({activity.track_url})\n Artist: {activity.artist}\n Album: {activity.album}\n Duration: {activity.duration}", inline = False)
            await ctx.send(embed=userembed)
    
    @commands.command(aliases=["bot"])
    async def botinfo(self, ctx):
        target = ctx.guild.me
        botappinfo = await self.bot.application_info()
        botembed = nextcord.Embed(title=target, description=f"{target.mention} | **__{nextcord.PartialEmoji(name='IDcard', id=868046662306770985, animated=False)} ID: __** {target.id}", colour = target.colour, timestamp=ctx.message.created_at)
        botembed.add_field(name=f"__{nextcord.PartialEmoji(name='Top_Role', id=869212283941834764, animated=False)} Top role: __", value=target.top_role.mention, inline=True)
        botembed.add_field(name=f"__{nextcord.PartialEmoji(name='Humanbot', id=869219560488829008, animated=False)} Bot: __", value = bool(target.bot), inline=True)
        botembed.add_field(name=f"__{nextcord.PartialEmoji(name='Booster', id=869228744462708856, animated=False)} Booster: __", value=bool(target.premium_since), inline=True)
        botembed.add_field(name=f"__{nextcord.PartialEmoji(name='UserJoin', id=869220716468387910, animated=False)} Joined: __", value=datetime.date.strftime(target.joined_at, '%a, %d/%m/%Y %H:%M:%S'), inline=True)
        botembed.add_field(name=f"__{nextcord.PartialEmoji(name='UserRegister', id=869222509902442528, animated=False)} Registered: __", value=datetime.date.strftime(target.created_at, '%a, %d/%m/%Y %H:%M:%S'), inline=True)
        botembed.add_field(name=f"__{nextcord.PartialEmoji(name='Activity', id=869225549917220874, animated=False)} Activity: __", value=f"{str(target.activity.type).split('.')[-1].title() if target.activity else 'N/A'} | {target.activity.name if target.activity else 'N/A'}", inline=False)
        botembed.add_field(name=f"__{nextcord.PartialEmoji(name='Status', id=869226936197591070, animated=False)}  Status: __", value=str(target.status).upper(), inline=True)
        botembed.add_field(name=f"__{nextcord.PartialEmoji(name='Nickname', id=869227972496871466, animated=False)} Nickname: __", value=target.nick, inline=True)
        botembed.add_field(name=f"__{nextcord.PartialEmoji(name='Roles', id=869214008077602856, animated=False)} Roles({len(target.roles)}): __",value='|'.join(role.mention for role in target.roles), inline=False)
        botembed.add_field(name=f"__{nextcord.PartialEmoji(name='DiscordPython', id=876495517960527912, animated=False)} Discord.py version: __", value=((f"{nextcord.__version__}| {nextcord.version_info[3]} release").title()).replace("Final", "Stable"), inline=True)
        botembed.add_field(name=f"__{nextcord.PartialEmoji(name='Server', id=876495661179211816, animated=False)} Servers: __", value=len(self.bot.guilds), inline=True)
        botembed.add_field(name=f"__{nextcord.PartialEmoji(name='UserPerms', id=871662256709062676, animated=False)} Permissions: __", value=', '.join(f"{(perm[0])}".title() for perm in target.guild_permissions if perm[1]).replace("_", " "), inline=False)
        botembed.add_field(name=f"__{nextcord.PartialEmoji(name='Badge', id=875656242855559199, animated=False)} Badges: __", value='\n'.join((((((((((((((((((((((((((((f'{x}'.replace("'", "")).replace(", ", ": ")).replace("(", "")).replace(")", "")).title()).replace("True", "✅")).replace("False", "❌")).replace("Staff", f"{nextcord.PartialEmoji(name='StaffDiscord', id=875627848482832464, animated=False)} Staff")).replace("Partner", f"{nextcord.PartialEmoji(name='PartnerDiscord', id=875628049595527208, animated=False)} Partner")).replace("Hypesquad", f"{nextcord.PartialEmoji(name='HypesquadDiscord', id=875638722526347305, animated=False)} Hypesquad")).replace("Bug_Hunter", f"{nextcord.PartialEmoji(name='BughunterDiscord', id=875638745360138262, animated=False)} Bug_Hunter")).replace("Hypesquad_Bravery", f"{nextcord.PartialEmoji(name='BraveryLogo', id=875638856517570601, animated=False)} Hypesquad_Bravery")).replace("Hypesquad_Brilliance", f"{nextcord.PartialEmoji(name='BrillianceLogo', id=875638884443226133,)} Hypesquad_Brilliance")).replace("Hypesquad_Balance", f"{nextcord.PartialEmoji(name='BalanceLogo', id=875638903456034826, animated=False)} Hypesquad_Balance")).replace("Early_Supporter", f"{nextcord.PartialEmoji(name='EarlySupporter', id=875639057697353728, animated=False)} Early_Supporter")).replace("Team_User", f"{nextcord.PartialEmoji(name='TeamUser', id=875639157622460416, animated=False)} Team_User")).replace("System", f"{nextcord.PartialEmoji(name='SystemDiscord', id=875639240006959105, animated=False)} System")).replace("Bug_Hunter_Level_2", f"{nextcord.PartialEmoji(name='BugHunterlv2', id=875639279810912266, animated=False)} Bug_Hunter_Level_2")).replace("Verified_Bot", f"{nextcord.PartialEmoji(name='BotUser', id=875639837032583209, animated=False)} Verified_Bot")).replace("Verified_Bot_Developer", f"{nextcord.PartialEmoji(name='VerifiedBotdev', id=875656092120674346, animated=False)} Verified_Bot_Developer")).replace(f"{nextcord.PartialEmoji(name='HypesquadDiscord', id=875638722526347305, animated=False)} {nextcord.PartialEmoji(name='BraveryLogo', id=875638856517570601, animated=False)} Hypesquad_Bravery", f"{nextcord.PartialEmoji(name='BraveryLogo', id=875638856517570601, animated=False)} Hypesquad_Bravery")).replace(f"{nextcord.PartialEmoji(name='HypesquadDiscord', id=875638722526347305, animated=False)} {nextcord.PartialEmoji(name='BrillianceLogo', id=875638884443226133,)} Hypesquad_Brilliance", f"{nextcord.PartialEmoji(name='BrillianceLogo', id=875638884443226133,)} Hypesquad_Brilliance")).replace(f"{nextcord.PartialEmoji(name='HypesquadDiscord', id=875638722526347305, animated=False)} {nextcord.PartialEmoji(name='BalanceLogo', id=875638903456034826, animated=False)} Hypesquad_Balance", f"{nextcord.PartialEmoji(name='BalanceLogo', id=875638903456034826, animated=False)} Hypesquad_Balance")).replace(f"{nextcord.PartialEmoji(name='BughunterDiscord', id=875638745360138262, animated=False)} {nextcord.PartialEmoji(name='BugHunterlv2', id=875639279810912266, animated=False)} Bug_Hunter_Level_2", f"{nextcord.PartialEmoji(name='BugHunterlv2', id=875639279810912266, animated=False)} Bug_Hunter_Level_2")).replace(f"{nextcord.PartialEmoji(name='BotUser', id=875639837032583209, animated=False)} {nextcord.PartialEmoji(name='VerifiedBotdev', id=875656092120674346, animated=False)} Verified_Bot_Developer", f"{nextcord.PartialEmoji(name='VerifiedBotdev', id=875656092120674346, animated=False)} Verified_Bot_Developer")).replace("_", " ")).replace(f"{nextcord.PartialEmoji(name='HypesquadDiscord', id=875638722526347305, animated=False)} Hypesquad", f"{nextcord.PartialEmoji(name='HypesquadDiscord', id=875638722526347305, animated=False)} Hypesquad Events").replace("Discord Certified Moderator", f"{nextcord.PartialEmoji(name='CertifiedModerator', id=942802702092599316, animated=False)} Discord Certified Moderator")).replace("Known Spammer", f"{nextcord.PartialEmoji(name='KnownSpammer', id=942807033781055588, animated=False)} Known Spammer") for x in target.public_flags), inline=False)
        botembed.add_field(name=f"__{nextcord.PartialEmoji(name='Botcreator', id=876496012393476116, animated=False)} Creator: __", value=botappinfo.owner, inline=True)
        botembed.add_field(name="__Codename: __", value=botappinfo.name, inline=True)
        botembed.set_thumbnail(url=botappinfo.icon.url)
        botembed.set_footer(icon_url=ctx.author.avatar.url, text=f"Requested by {ctx.author.name}")
        await ctx.send(embed=botembed)
    
    @commands.command(aliases=["si","guildinfo", "guild", "server"])
    @commands.has_permissions(embed_links=True)
    async def serverinfo(self, ctx):
        guild = ctx.guild
        statuses = [len(list(filter(lambda m: str(m.status) == "online", ctx.guild.members))),
                        len(list(filter(lambda m: str(m.status) == "idle", ctx.guild.members))),
                        len(list(filter(lambda m: str(m.status) == "dnd", ctx.guild.members))),
                        len(list(filter(lambda m: str(m.status) == "offline", ctx.guild.members)))]
        guildembed = nextcord.Embed(title=guild.name, description=f"**{nextcord.PartialEmoji(name='Serverdesc', id=871586961188610079, animated=False)} Description: ** {guild.description}", colour = ctx.guild.owner.colour, timestamp=ctx.message.created_at)
        guildembed.add_field(name=f"{nextcord.PartialEmoji(name='ServerID', id=871583345363021854, animated=False)} ID: ", value=guild.id, inline=True)
        guildembed.add_field(name=f"{nextcord.PartialEmoji(name='Servercreation', id=871591082260058123, animated=False)} Created on: ", value = datetime.date.strftime(guild.created_at, '%a, %d/%m/%Y %H:%M:%S'), inline=True)
        guildembed.add_field(name=f"{nextcord.PartialEmoji(name='Serverroles', id=871615599091007519, animated=False)} Roles({len(guild.roles)}): ", value='|'.join(role.mention for role in guild.roles), inline=False)
        guildembed.set_thumbnail(url=guild.icon.url if guild.icon else "https://i.imgur.com/poBdtmA.png")
        guildembed.add_field(name=f"{nextcord.PartialEmoji(name='Emojiblob', id=871715724693999677, animated=False)} Emojis({int(len(guild.emojis))}): ", value=f"{''.join(str(emote) for emote in guild.emojis[0:32])} and more", inline=False)
        guildembed.add_field(name=f"{nextcord.PartialEmoji(name='Membercount', id=871616325108248586, animated=False)} Membercount: ", value=f"`{guild.member_count}` Members", inline=True)
        guildembed.add_field(name=f"{nextcord.PartialEmoji(name='Human', id=871617153495859230, animated=False)} Humans: ", value =f"`{len(list(filter(lambda m: not m.bot, guild.members)))}` Human(s)", inline=True)
        guildembed.add_field(name=f"{nextcord.PartialEmoji(name='Bot', id=871620978462048317, animated=False)} Bots: ", value=f"`{len(list(filter(lambda m: m.bot, guild.members)))}` Bot(s)", inline=True)
        guildembed.add_field(name=f"{nextcord.PartialEmoji(name='Banhammer', id=871624353681399898, animated=False)} Member bans: ", value=len(await guild.bans()), inline=True)
        guildembed.add_field(name=f"{nextcord.PartialEmoji(name='Nitroboost', id=871624854288351242, animated=False)} Nitro boost level: ", value=f"Level {guild.premium_tier}", inline=True)
        guildembed.add_field(name=f"{nextcord.PartialEmoji(name='Booster', id=869228744462708856, animated=False)} Boosts: ", value=guild.premium_subscription_count, inline=True)
        guildembed.add_field(name=f"{nextcord.PartialEmoji(name='Statuses', id=872498901842788453, animated=False)} Statuses: ", value=f"{nextcord.PartialEmoji(name='Useronline', id=871985942741782539, animated=False)} {statuses[0]} {nextcord.PartialEmoji(name='Useridle', id=871985959737102367, animated=False)} {statuses[1]} {nextcord.PartialEmoji(name='Userdnd', id=871986111843532852, animated=False)} {statuses[2]} {nextcord.PartialEmoji(name='Useroffline', id=871986172346376252, animated=False)} {statuses[3]}", inline=True)
        guildembed.add_field(name=f"{nextcord.PartialEmoji(name='Serververify', id=871978151058751528, animated=False)} Verification level: ", value=str(guild.verification_level).title(), inline=True)
        guildembed.add_field(name=f"{nextcord.PartialEmoji(name='Textchannel', id=871628497414684682, animated=False)} Text channels({len(guild.text_channels)}): ", value='|'.join(channel.mention for channel in guild.text_channels), inline=False)
        guildembed.add_field(name=f"{nextcord.PartialEmoji(name='Voicechannel', id=871632753186177055, animated=False)} Voice channels({len(guild.voice_channels)}): ", value='|'.join(channel.mention for channel in guild.voice_channels), inline=False)
        guildembed.add_field(name=f"{nextcord.PartialEmoji(name='Category', id=871636437609639977, animated=False)} Channel categories({len(guild.categories)}): ", value=' | '.join(category.mention for category in guild.categories), inline=False)
        guildembed.add_field(name=f"{nextcord.PartialEmoji(name='Serverregion', id=871638602843553792, animated=False)} Region: ", value=str(guild.region).title(), inline=True)
        guildembed.add_field(name=f"{nextcord.PartialEmoji(name='Serverowner', id=871641007400300574, animated=False)} Owner: ", value=guild.owner.mention, inline=True)
        guildembed.add_field(name=f"{nextcord.PartialEmoji(name='Serverfeature', id=875656634280579082, animated=False)} Features: ", value=('\n'.join(f"{nextcord.PartialEmoji(name='MemberEnter', id=875359683517509633, animated=False)} **`{x}`**".replace("_", " ") for x in ctx.guild.features)) if ctx.guild.features else 'N/A', inline=False)
        guildembed.set_footer(icon_url=ctx.author.avatar.url, text=f"Requested by {ctx.author.name}")
        await ctx.send(embed=guildembed)

    @commands.command(aliases=["el", "emoji", "emote", "emotelist"])
    async def emojilist(self, ctx):
        guild = ctx.guild
        await ctx.send(f"{''.join(str(emote) for emote in guild.emojis)}")
    
    @commands.command(aliases=["pfp", "profilepic", "profile"])
    async def avatar(self, ctx, target : Optional[Member]):
        if not target:
            target = ctx.message.author
        avatar = target.avatar.url
        embed = nextcord.Embed(title=target.name, description=target.mention, colour=target.colour)
        embed.set_image(url=avatar)
        embed.set_footer(icon_url=ctx.author.avatar.url, text=f"Requested by {ctx.author.name}")
        await ctx.send(embed=embed)
    
    
def setup(bot):
    bot.add_cog(Information(bot))