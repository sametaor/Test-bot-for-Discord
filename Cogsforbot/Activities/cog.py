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

def setup(bot):
    bot.add_cog(Activities(bot))