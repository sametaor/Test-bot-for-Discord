import nextcord
from nextcord.ext import commands
from PIL import Image
from io import BytesIO

class MemeGen(commands.Cog, name="Meme Generation"):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def wanted(self, ctx, user: nextcord.Member = None):
        if user == None:
            user = ctx.author
        
        wanted = Image.open("Cogsforbot/ImageManipulation/Wanted.jpg")
        asset = user.avatar.with_size(512)
        
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        
        pfp.resize((283,283))
        wanted.paste(pfp, (96,230))
        wanted.save("profile.jpg")
        await ctx.send(file = nextcord.File("profile.jpg"))
    
def setup(bot):
    bot.add_cog(MemeGen(bot))