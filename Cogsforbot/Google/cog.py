import os
import nextcord
from nextcord.ext import commands
import random
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv("token.env")

class Google(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def gimgsearch(self, ctx, *,query):
        rand = random.randint(0, 9)
        result = build("customsearch", "v1", developerKey=os.getenv("GOOGLE_API_KEY")).cse()
        queryresult = result.list(q=f"{query}", cx=os.getenv("GOOGLE_CX_ID"), searchType="image").execute()
        url = queryresult["items"][rand]["link"]
        googlembed = nextcord.Embed(title=f"Here are the results for {query.title()}", colour=nextcord.Color.og_blurple())
        googlembed.set_image(url=url)
        await ctx.send(embed=googlembed)
    
    @commands.command()
    async def gsearch(self, ctx, *, query):
        rand = random.randint(0, 9)
        result = build("customsearch", "v1", developerKey=os.getenv("GOOGLE_API_KEY")).cse()
        queryresult = result.list(q=f"{query}", cx=os.getenv("GOOGLE_CX_ID")).execute()
        url = queryresult["items"][rand]["link"]
        googlembed = nextcord.Embed(title=f"Here are the results for {query.title()}", description=f"[Click here!]({url})", colour=nextcord.Color.og_blurple())
        await ctx.send(embed=googlembed)
    
def setup(bot):
    bot.add_cog(Google(bot))