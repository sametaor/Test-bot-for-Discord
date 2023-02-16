import nextcord
from nextcord.ext import commands
import requests
import os
from dotenv import load_dotenv

load_dotenv('aichat.env')

class AIresponse(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, msg):
        testbot = self.bot
        if testbot.user == msg.author:
            return
        if msg.channel.name == 'ai-chat':
            url = "https://random-stuff-api.p.rapidapi.com/ai/response"
            text = msg.content
            querystring = {"message":text, "user_id":"420"}

            headers = {
            'authorization': os.getenv('RANDOMSTUFFAPIKEY'),
            'x-rapidapi-host': "random-stuff-api.p.rapidapi.com",
            'x-rapidapi-key': os.getenv('RAPIDAPIKEY')
            }
            response = requests.request("GET", url, headers=headers, params=querystring)

            r=response.text
            r=r.split('"message":"')
            r=r[1]
            r=r.replace('"}', '')
            print(r)
            await msg.reply(str(r))
        await testbot.process_commands(msg)
    
    @commands.command()
    async def say(self, ctx, *, statement: commands.clean_content =None):
        if statement != None:
            await ctx.message.delete()
            await ctx.send(statement)
        else:
            await ctx.send("Please write the statement that is to be said")

def setup(bot):
    bot.add_cog(AIresponse(bot))