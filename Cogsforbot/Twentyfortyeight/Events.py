import os
import discord
from discord.ext import commands
from dotenv.main import load_dotenv
from Cogsforbot.Twentyfortyeight.Gamegrid import *
from imgurpython import ImgurClient

load_dotenv()

imgur_client_id = os.getenv('IMGUR_CLIENT_ID')
imgur_client_secret = os.getenv('IMGUR_CLIENT_SECRET')

imgur_client = ImgurClient(imgur_client_id, imgur_client_secret)

class Events:

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def on_reaction_add(self, reaction, user):
        if user.id == self.bot.user.id:
            return

        message = reaction.message

        if getGamesByUser(str(user.id)) is not None:
            game = getGamesByUser(str(user.id))
            if str(game.getMessageId()) == str(message.id):
                if str(reaction.emoji) == '⬆':
                    game.slideUp()
                    game.randomNumber()
                    game.drawMatrix()
                elif str(reaction.emoji) == '⬇':
                    game.slideDown()
                    game.randomNumber()
                    game.drawMatrix()
                elif str(reaction.emoji) == '➡':
                    game.slideRight()
                    game.randomNumber()
                    game.drawMatrix()
                elif str(reaction.emoji) == '⬅':
                    game.slideLeft()
                    game.randomNumber()
                    game.drawMatrix()

                game.saveImage(str(user.id))
                img = imgur_client.upload_from_path(game.temp + f'{user.id}.png')
                try:
                    os.remove(game.temp + f'{user.id}.png')
                except Exception:
                    pass

                await message.remove_reaction(reaction, user)

                embed = discord.Embed(title='2048', color=discord.Color.dark_theme())
                embed.set_image(url=str(img['link']))
                message = await message.edit(embed=embed)


#All credits go to AbhigyaKrishna