import datetime
import discord
import inspect
import urbandictionary as ud
import re
from discord.ext import commands
import functools
import urllib.request
import urllib.parse
import wikipediaapi


class Wikipedia(commands.Cog):
    """Get detailed info on any topic via Wikipedia!"""
    def __init__(self, bot):
        self.bot = bot
    

    @commands.command(name='wiki', help='use &wiki <term> to easily get detailed information about any topic you like.')
    async def wiki_search(self, ctx, *args):
        wiki_wiki = wikipediaapi.Wikipedia('en')

        page_py = wiki_wiki.page(args)
        page_py = wiki_wiki.page(args)
        print("Page - Exists: %s" % page_py.exists())
        # Page - Exists: True

        page_missing = wiki_wiki.page('NonExistingPageWithStrangeName')
        print("Page - Exists: %s" %     page_missing.exists())
        # Page - Exists: False

        wiki_wiki = wikipediaapi.Wikipedia('en')

        print("Page - Title: %s" % page_py.title)
            # Page - Title: Python (programming language)

        print("Page - Summary: %s" % page_py.summary[0:60])
            # Page - Summary: Python is a widely used high-level programming language for
        wikiembed = discord.Embed(title =page_py.title, description = page_py.summary[0:2000], colour = discord.Colour.lighter_grey())
        await ctx.send(embed=wikiembed)

def setup(bot):
    bot.add_cog(Wikipedia(bot))