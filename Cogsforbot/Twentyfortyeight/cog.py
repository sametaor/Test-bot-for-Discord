import os
import discord
from Cogsforbot.Twentyfortyeight.Gamegrid import *
from discord.ext import commands
from Cogsforbot.Twentyfortyeight.Events import *


class TwentyFortyEight(commands.Cog):
    """2048 game"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="2048")
    @commands.cooldown(1, 3.0, type=commands.BucketType.user)
    async def _2048(self, ctx, args=None):
        if args is None:
            embed = discord.Embed(title="2048 Help", colour=discord.Color.gold())
            embed.add_field(name=">2048 start", value="Start 2048 game", inline=False)
            embed.add_field(name=">2048 stop", value="Stop game", inline=False)
            await ctx.send(embed=embed)

        elif args.lower() == 'start':

            if getGamesByUser(str(ctx.author.id)) is not None:
                gamer = getGamesByUser(str(ctx.author.id))
                gamer.stopGame(str(ctx.author.id))

            game = GameGrid(f'{ctx.author.id}')
            game.start()

            game.saveImage(str(ctx.author.id))
            img = imgur_client.upload_from_path(game.temp + f'{ctx.author.id}.png')
            try:
                os.remove(game.temp + f'{ctx.author.id}.png')
            except Exception:
                pass

            embed = discord.Embed(title='2048', color=discord.Color.dark_theme())
            embed.set_image(url=str(img['link']))
            message = await ctx.send(embed=embed)

            game.setMessageId(message.id)

            await message.add_reaction('⬆')
            await message.add_reaction('⬇')
            await message.add_reaction('➡')
            await message.add_reaction('⬅')

        elif args.lower() == 'stop':

            if getGamesByUser(str(ctx.author.id)) is not None:
                game = getGamesByUser(str(ctx.author.id))
                game.saveImage(str(ctx.author.id))
                img = imgur_client.upload_from_path(game.temp + f'{ctx.author.id}.png')
                try:
                    os.remove(game.temp + f'{ctx.author.id}.png')
                except Exception:
                    pass

                msgID = game.getMessageId()
                message = await ctx.fetch_message(msgID)
                await message.delete()

                game.stop()
                embed = discord.Embed(title='Game Stopped', description='Your game session stopped successfully',
                                    color=discord.Color.orange())
                embed.set_image(url=str(img['link']))
                await ctx.send(embed=embed)
                return

            embed = discord.Embed(title='Error', description='You haven\'t started a game yet.',
                                color=discord.Color.red())
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(TwentyFortyEight(bot))


#All credits go to AbhigyaKrishna