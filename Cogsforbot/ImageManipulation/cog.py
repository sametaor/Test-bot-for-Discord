import nextcord
from nextcord.ext import commands
from PIL import Image, ImageFont, ImageDraw
from io import BytesIO

class MemeGen(commands.Cog, name="Meme Generation"):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def wanted(self, ctx, user: nextcord.Member = None):
        if user == None:
            user = ctx.author
        
        wanted = Image.open("Cogsforbot/ImageManipulation/Wanted.jpg")
        asset = user.avatar.with_size(256)
        
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        
        pfp.resize((283,283))
        wanted.paste(pfp, (107,240))
        wanted.save("profile.jpg")
        await ctx.send(file = nextcord.File("profile.jpg"))
    
    @commands.command()
    async def society(self, ctx, *, text=None):
        if text == None:
            text = "Put a statement here to add to the meme by typing '&society <statement>'"
        
        img = Image.open("Cogsforbot/ImageManipulation/Society.jpg")
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype("Cogsforbot/ImageManipulation/Myriad Pro Regular.ttf", 24)
        draw.text((7,11), text, (0, 0, 0), font=font)
        img.save("societyif.png")
        await ctx.send(file = nextcord.File("societyif.jpg"))
    
def setup(bot):
    bot.add_cog(MemeGen(bot))