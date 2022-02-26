import nextcord
from nextcord.ext import commands
import requests

class AIresponse(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, msg):
        testbot = self.bot
        if testbot.user == msg.author:
            return
        if msg.channel.name == 'ai-chat':
            url = "https://random-stuff-api.p.rapidapi.com/ai"
            text = msg.content
            querystring = {"msg":text,"bot_name":"Tachyon","bot_gender":"Male","bot_master":"sametaor","bot_age":"2","bot_build":"Public ","bot_birth_year":"2020","bot_birth_date":"15th April, 2020","bot_favorite_color":"Blue"}

            headers = {
            'authorization': RANDOMSTUFFAPIKEY,
            'x-rapidapi-host': "random-stuff-api.p.rapidapi.com",
            'x-rapidapi-key': RAPIDAPIKEY
            }
            response = requests.request("GET", url, headers=headers, params=querystring)

            r=response.text
            r=r.split('"AIResponse":"')
            r=r[1]
            r=r.replace('"}', '')
            print(r)
            await msg.reply(str(r))
        await testbot.process_commands(msg)

def setup(bot):
    bot.add_cog(AIresponse(bot))