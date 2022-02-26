import datetime
import nextcord
import inspect
import urbandictionary as ud
import re
from nextcord.ext import commands
import functools
import urllib.request
import urllib.parse
import wikipediaapi


def count(list1, l, r):
    c = 0
    # traverse in the list1
    for x in list1:
        # condition check
        if x>= l and x<= r:
            c+= 1
    return c

class Wikipedia(commands.Cog):
    """Get detailed info on any topic via Wikipedia!"""
    COG_EMOJI = "📖"
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
        string_length = len(page_py.summary)
        if string_length < 2000:
            wikiembed = nextcord.Embed(title =page_py.title, description = page_py.summary, url =page_py.fullurl, colour = nextcord.Colour.lighter_grey())
            await ctx.send(embed=wikiembed)
        else:
            max_index = 2000
            index = 0
            while index < (string_length - max_index):
                posted_string = page_py.summary[index:max_index]
                wikiembed = nextcord.Embed(title =page_py.title, description = posted_string, url =page_py.fullurl, colour = nextcord.Colour.lighter_grey())
                index = index + max_index
                posted_string = page_py.summary[index-max_index:]
                wikiembed = nextcord.Embed(title =page_py.title, description = page_py.summary, url =page_py.fullurl, colour = nextcord.Colour.lighter_grey())
                await ctx.send(embed=wikiembed)

def setup(bot):
    bot.add_cog(Wikipedia(bot))