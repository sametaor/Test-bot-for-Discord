import nextcord
from nextcord.ext import commands, activities

class MakeLinkBtn(nextcord.ui.View):
    def __init__(self, link:str):
        super().__init__()
        self.add_item(nextcord.ui.Button(label="Join Game!", url=f"{link}"))

class Activities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group(invoke_without_command=True)
    async def activityplay(self, ctx):
        return await ctx.send("Missing subcommand, please specify the activity/game you'd like to play and mention the subcommand accordingly")
    
    @activityplay.command()
    async def sketch(self, ctx, channel: nextcord.VoiceChannel = None):
        if channel == None:
            return await ctx.send("Please specify a channel to join/create a game")
        try:
            invite_link =  await channel.create_activity_invite(activities.Activity.sketch)
        except nextcord.HTTPException:
            return await ctx.send("Please mention a voice channel to join/create a game")
        sketchembed = nextcord.Embed(title="Sketch game", description=f"{ctx.author.mention} has created a game in {channel.mention}")
        sketchembed.add_field(name="How to Play?", value="If you have played games like skribble.io and gartic phone, this is basically it, where one draws something, and the rest try to guess what it's supposed to be!")
        sketchembed.set_thumbnail(url="https://i.imgur.com/KAg60qh.png")
        await ctx.send(embed=sketchembed, view=MakeLinkBtn(invite_link))
    
    @activityplay.command()
    async def chess(self, ctx, channel: nextcord.VoiceChannel = None):
        if channel == None:
            return await ctx.send("Please specify a channel to join/create a game")
        try:
            invite_link =  await channel.create_activity_invite(activities.Activity.chess)
        except nextcord.HTTPException:
            return await ctx.send("Please mention a voice channel to join/create a game")
        sketchembed = nextcord.Embed(title="Chess game", description=f"{ctx.author.mention} has created a game in {channel.mention}")
        sketchembed.add_field(name="How to Play?", value="This is the same old chess that you play on a physical board but in a voice channel!")
        sketchembed.set_thumbnail(url="https://i.imgur.com/KAg60qh.png")
        await ctx.send(embed=sketchembed, view=MakeLinkBtn(invite_link))
    
    @activityplay.command()
    async def checkers(self, ctx, channel: nextcord.VoiceChannel = None):
        if channel == None:
            return await ctx.send("Please specify a channel to join/create a game")
        try:
            invite_link =  await channel.create_activity_invite(activities.Activity.checker)
        except nextcord.HTTPException:
            return await ctx.send("Please mention a voice channel to join/create a game")
        sketchembed = nextcord.Embed(title="Checkers game", description=f"{ctx.author.mention} has created a game in {channel.mention}")
        sketchembed.add_field(name="How to Play?", value="This is the same old checkers(not Chinese checkers, the original one) that you play on a physical board but in a voice channel!")
        sketchembed.set_thumbnail(url="https://i.imgur.com/KAg60qh.png")
        await ctx.send(embed=sketchembed, view=MakeLinkBtn(invite_link))
    
    @activityplay.command()
    async def youtube(self, ctx, channel: nextcord.VoiceChannel = None):
        if channel == None:
            return await ctx.send("Please specify a channel to join/create a game")
        try:
            invite_link =  await channel.create_activity_invite(activities.Activity.youtube)
        except nextcord.HTTPException:
            return await ctx.send("Please mention a voice channel to join/create a game")
        sketchembed = nextcord.Embed(title="Youtube", description=f"{ctx.author.mention} has created a game in {channel.mention}")
        sketchembed.add_field(name="How to Play?", value="Watch youtube along with your friends conveniently in a Voice Channel!")
        sketchembed.set_thumbnail(url="https://i.imgur.com/KAg60qh.png")
        await ctx.send(embed=sketchembed, view=MakeLinkBtn(invite_link))
    
    @activityplay.command()
    async def ocho(self, ctx, channel: nextcord.VoiceChannel = None):
        if channel == None:
            return await ctx.send("Please specify a channel to join/create a game")
        try:
            invite_link =  await channel.create_activity_invite(activities.Activity.ocho)
        except nextcord.HTTPException:
            return await ctx.send("Please mention a voice channel to join/create a game")
        sketchembed = nextcord.Embed(title="Ocho game", description=f"{ctx.author.mention} has created a game in {channel.mention}")
        sketchembed.add_field(name="How to Play?", value="If you have played Uno before, this is basically the same game with a different name!")
        sketchembed.set_thumbnail(url="https://i.imgur.com/KAg60qh.png")
        await ctx.send(embed=sketchembed, view=MakeLinkBtn(invite_link))
    
    @activityplay.command()
    async def wordsnacks(self, ctx, channel: nextcord.VoiceChannel = None):
        if channel == None:
            return await ctx.send("Please specify a channel to join/create a game")
        try:
            invite_link =  await channel.create_activity_invite(activities.Activity.word_snacks)
        except nextcord.HTTPException:
            return await ctx.send("Please mention a voice channel to join/create a game")
        sketchembed = nextcord.Embed(title="Word Snacks game", description=f"{ctx.author.mention} has created a game in {channel.mention}")
        sketchembed.add_field(name="How to Play?", value="This is the same old chess that you play on a physical board but in a voice channel!")
        sketchembed.set_thumbnail(url="https://i.imgur.com/KAg60qh.png")
        await ctx.send(embed=sketchembed, view=MakeLinkBtn(invite_link))
    
    @activityplay.command()
    async def betrayal(self, ctx, channel: nextcord.VoiceChannel = None):
        if channel == None:
            return await ctx.send("Please specify a channel to join/create a game")
        try:
            invite_link =  await channel.create_activity_invite(activities.Activity.betrayal)
        except nextcord.HTTPException:
            return await ctx.send("Please mention a voice channel to join/create a game")
        sketchembed = nextcord.Embed(title="Betrayal game", description=f"{ctx.author.mention} has created a game in {channel.mention}")
        sketchembed.add_field(name="How to Play?", value="Play a game of Betrayal along with your friends in a Voice Channel!")
        sketchembed.set_thumbnail(url="https://i.imgur.com/KAg60qh.png")
        await ctx.send(embed=sketchembed, view=MakeLinkBtn(invite_link))
    
    @activityplay.command()
    async def fishington(self, ctx, channel: nextcord.VoiceChannel = None):
        if channel == None:
            return await ctx.send("Please specify a channel to join/create a game")
        try:
            invite_link =  await channel.create_activity_invite(activities.Activity.fishington)
        except nextcord.HTTPException:
            return await ctx.send("Please mention a voice channel to join/create a game")
        sketchembed = nextcord.Embed(title="Fishington game", description=f"{ctx.author.mention} has created a game in {channel.mention}")
        sketchembed.add_field(name="How to Play?", value="Try to catch more fish than your friends to win the game!")
        sketchembed.set_thumbnail(url="https://i.imgur.com/KAg60qh.png")
        await ctx.send(embed=sketchembed, view=MakeLinkBtn(invite_link))

    @activityplay.command()
    async def spellcast(self, ctx, channel: nextcord.VoiceChannel = None):
        if channel == None:
            return await ctx.send("Please specify a channel to join/create a game")
        try:
            invite_link =  await channel.create_activity_invite(activities.Activity.spellcast)
        except nextcord.HTTPException:
            return await ctx.send("Please mention a voice channel to join/create a game")
        sketchembed = nextcord.Embed(title="Spellcast game", description=f"{ctx.author.mention} has created a game in {channel.mention}")
        sketchembed.add_field(name="How to Play?", value="Play a game of Spellcast with your friends in a Voice Channel!")
        sketchembed.set_thumbnail(url="https://i.imgur.com/KAg60qh.png")
        await ctx.send(embed=sketchembed, view=MakeLinkBtn(invite_link))

    @activityplay.command()
    async def awkword(self, ctx, channel: nextcord.VoiceChannel = None):
        if channel == None:
            return await ctx.send("Please specify a channel to join/create a game")
        try:
            invite_link =  await channel.create_activity_invite(activities.Activity.awkword)
        except nextcord.HTTPException:
            return await ctx.send("Please mention a voice channel to join/create a game")
        sketchembed = nextcord.Embed(title="Awkword game", description=f"{ctx.author.mention} has created a game in {channel.mention}")
        sketchembed.add_field(name="How to Play?", value="Play a game of Awkword with your friends in a Voice Channel!")
        sketchembed.set_thumbnail(url="https://i.imgur.com/KAg60qh.png")
        await ctx.send(embed=sketchembed, view=MakeLinkBtn(invite_link))

    @activityplay.command()
    async def lettertile(self, ctx, channel: nextcord.VoiceChannel = None):
        if channel == None:
            return await ctx.send("Please specify a channel to join/create a game")
        try:
            invite_link =  await channel.create_activity_invite(activities.Activity.letter_tile)
        except nextcord.HTTPException:
            return await ctx.send("Please mention a voice channel to join/create a game")
        sketchembed = nextcord.Embed(title="Letter Tile game", description=f"{ctx.author.mention} has created a game in {channel.mention}")
        sketchembed.add_field(name="How to Play?", value="Play a game of Letter Tile with your friends in a Voice Channel!")
        sketchembed.set_thumbnail(url="https://i.imgur.com/KAg60qh.png")
        await ctx.send(embed=sketchembed, view=MakeLinkBtn(invite_link))

    @activityplay.command()
    async def letterleague(self, ctx, channel: nextcord.VoiceChannel = None):
        if channel == None:
            return await ctx.send("Please specify a channel to join/create a game")
        try:
            invite_link =  await channel.create_activity_invite(activities.Activity.letter_league)
        except nextcord.HTTPException:
            return await ctx.send("Please mention a voice channel to join/create a game")
        sketchembed = nextcord.Embed(title="Letter League game", description=f"{ctx.author.mention} has created a game in {channel.mention}")
        sketchembed.add_field(name="How to Play?", value="Play a game of Letter League with your friends in a Voice Channel!")
        sketchembed.set_thumbnail(url="https://i.imgur.com/KAg60qh.png")
        await ctx.send(embed=sketchembed, view=MakeLinkBtn(invite_link))

    @activityplay.command()
    async def doodle(self, ctx, channel: nextcord.VoiceChannel = None):
        if channel == None:
            return await ctx.send("Please specify a channel to join/create a game")
        try:
            invite_link =  await channel.create_activity_invite(activities.Activity.doodle)
        except nextcord.HTTPException:
            return await ctx.send("Please mention a voice channel to join/create a game")
        sketchembed = nextcord.Embed(title="Doodle game", description=f"{ctx.author.mention} has created a game in {channel.mention}")
        sketchembed.add_field(name="How to Play?", value="Play a game of Doodle with your friends in a Voice Channel!")
        sketchembed.set_thumbnail(url="https://i.imgur.com/KAg60qh.png")
        await ctx.send(embed=sketchembed, view=MakeLinkBtn(invite_link))

def setup(bot):
    bot.add_cog(Activities(bot))