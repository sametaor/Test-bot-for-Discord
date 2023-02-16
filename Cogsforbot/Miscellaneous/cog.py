import nextcord
from nextcord.ext import commands
from prsaw import RandomStuffV4
import requests
import os
from dotenv import load_dotenv

class AIresponse(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, msg):
        testbot = self.bot
        if testbot.user == msg.author:
            return
        if msg.channel.name == 'ai-chat':
            text = msg.content
            rs = RandomStuffV4()
            response = rs.get_ai_response(text)
            print(response)
            await msg.reply(str(response))
            rs.close()
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