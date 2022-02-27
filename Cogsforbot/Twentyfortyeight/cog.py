import os
import nextcord
from Cogsforbot.Twentyfortyeight.Gamegrid import *
from nextcord.ext import commands
from Cogsforbot.Twentyfortyeight.Events import *


class TwentyFortyEight(commands.Cog):
    """Play a 2048 game on Discord!"""
    COG_EMOJI = nextcord.PartialEmoji(name="2048", id=947417027839156274, animated=False)

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="2048")
    @commands.cooldown(1, 3.0, type=commands.BucketType.user)
    async def _2048(self, ctx, args=None):
        if args is None:
            embed = nextcord.Embed(title="2048 Help", colour=nextcord.Color.gold())
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

            embed = nextcord.Embed(title='2048', color=nextcord.Color.dark_theme())
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
                embed = nextcord.Embed(title='Game Stopped', description='Your game session stopped successfully',
                                    color=nextcord.Color.orange())
                embed.set_image(url=str(img['link']))
                await ctx.send(embed=embed)
                return

            embed = nextcord.Embed(title='Error', description='You haven\'t started a game yet.',
                                color=nextcord.Color.red())
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(TwentyFortyEight(bot))


#All credits go to AbhigyaKrishna