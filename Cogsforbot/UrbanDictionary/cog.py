import asyncio
import json

import aiohttp
import nextcord
from nextcord.ext import commands

# Constants
BASEURL = 'https://api.urbandictionary.com/v0/'
NEXT_DEFINITION = '➡️'
MAX_EMBED_VALUE_LENGTH = 1024


def add_field_to_embed(embed: nextcord.Embed,
                       *, name: str, value: str):
    """
    Adds a field to a given embed, taking note of whether the value is empty
    and also that the value is less than the embed's maximum
    :param embed: nextcord.Embed to add to
    :param name: Title of the field
    :param value: Content of the field.
    """
    if not value:
        value = "..."

    value = (value[:MAX_EMBED_VALUE_LENGTH - 3] + "..."
            if len(value) > MAX_EMBED_VALUE_LENGTH
            else value)
    embed.add_field(name=name, value=value)


async def fetch(session, url):
    """
    Fetch content from a URL
    :param session: aiohttp session to use
    :param url: URL to query
    :return: Response text
    """
    async with session.get(url) as response:
        return await response.text()


async def search_query(querystring):
    """
    Query the Urban dictionary API for a specific word
    :param querystring: word to query the API for
    :return: response from the API
    """
    async with aiohttp.ClientSession() as session:
        data = await fetch(
            session, BASEURL + f'define?term={querystring}')
        return data


async def search_random_word():
    """
    Query the Urban Dictionary API for a random word
    :return: response from the API
    """
    async with aiohttp.ClientSession() as session:
        data = await fetch(session, BASEURL + 'random')
        return data


class Urbandict(commands.Cog):
    """Get definitions of words straight from Urban Dictionary."""
    COG_EMOJI = "📔"

    def __init__(self, bot):
        self.bot = bot

    async def create_embed(self, definitions, ctx):
        """
        Create an embed based on a given list of definitions
        :param definitions: List of definitions for a word.
        :param ctx: Context the command was used in
        """
        def check_reaction(message_reaction, message_user):
            return (str(message_reaction.emoji) == NEXT_DEFINITION
                    and message_reaction.message.id == message.id
                    and message_user.id != self.bot.user.id)

        counter = 0
        message = None

        if len(definitions) == 0:
            embed = nextcord.Embed(color=nextcord.Color.gold())
            embed.add_field(
                name="Error",
                value="There was no definition found for that word."
            )
            await ctx.send(embed=embed)

        while counter < len(definitions):

            definition = definitions[counter]['definition']
            example = definitions[counter]['example']
            word = definitions[counter]['word']

            embed = nextcord.Embed(title="Defining...", color=nextcord.Color.gold())

            for name, value in [("Word", word),
                                ("Definition", definition),
                                ("Example", example)]:

                add_field_to_embed(embed, name=name, value=value)

            if message is None:
                message = await ctx.send(embed=embed)
                # add emoji to message
                await message.add_reaction(NEXT_DEFINITION)
            else:
                await message.edit(embed=embed)
            try:
                reaction, user = await self.bot.wait_for(
                    'reaction_add', check=check_reaction, timeout=120.0)
                counter = (counter + 1) % len(definitions)
            except asyncio.TimeoutError:
                pass
            await reaction.remove(user)

    # Parse the searched word and display here
    @commands.command(name='urban',
                    help='use &urban <term> to search for a word.'
                    + 'You can also use &urban to search for a random word')
    async def search_dictionary(self, ctx, *, query=None):
        if query is None:
            definition_list = json.loads(
                await search_random_word())['list']

        else:
            # Gets the typed in query and parses it
            definition_list = json.loads(
                await search_query(query))['list']

        await self.create_embed(definition_list, ctx)


def setup(bot):
    bot.add_cog(Urbandict(bot))