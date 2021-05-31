import discord
from discord.ext import commands
import time
import random



game = {
    "high_score": 0,
    "current_score": 0,
    "games_played": 0,
    "game": False,
    "head": [1, 1],
    "length": 0,
    "direction": 6,
    "body": [],
    "grid": [
        [4, 4, 4, 4, 4, 4, 4, 4],
        [4, 3, 3, 3, 3, 3, 3, 4],
        [4, 3, 3, 3, 3, 3, 3, 4],
        [4, 3, 3, 3, 3, 3, 3, 4],
        [4, 3, 3, 3, 3, 3, 3, 4],
        [4, 3, 3, 3, 3, 3, 3, 4],
        [4, 3, 3, 3, 3, 3, 3, 4],
        [4, 4, 4, 4, 4, 4, 4, 4]
    ],# Just for reference
    "elements": {
        0: ":green_circle:", # Snake Head
        1: ":green_square:", # Snake Body
        2: ":black_large_square:", # Background
        3: ":brown_square:", # Walls
        4: ":apple:" # Food
    },
    "spawn_food": True,
    "food": []
}


class Snakegame(commands.Cog, name = "Snake"):
    """Play a game of snake right on Discord!"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="snek", help="Use $snek to start a quick game of snake while avoiding hitting the walls and reaching for food.")
    async def start(self, ctx):
        if game['game']:
            return await ctx.channel.send('A game is already going on.')
        await ctx.channel.send('Starting a new game.')
        await self.start_game(ctx)

    async def start_game(self, ctx):
        game['game'] = True
        game['games_played'] += 1
        await ctx.channel.send(f'This will be game number {game["games_played"]}')
        await self.update_grid(ctx)

    async def update_grid(self, ctx):
        if game['length'] > 0:
            game['body'].insert(0, game['head'].copy())
            game['body'].pop(-1)

        if game['direction'] == 2:
            game['head'][0] += 1
        elif game['direction'] == 4:
            game['head'][1] -= 1
        elif game['direction'] == 6:
            game['head'][1] += 1
        elif game['direction'] == 8:
            game['head'][0] -= 1

        if game['head'] == game['food'] and not game['spawn_food']:
            game['current_score'] += 1
            game['spawn_food'] = True
            game['length'] += 1
            body_add = game['head'].copy()
            if game['length'] > 1:
                body_add = game['body'][-1].copy()
            if game['direction'] == 2:
                body_add[0] -= 1
            elif game['direction'] == 4:
                body_add[1] += 1
            elif game['direction'] == 6:
                body_add[1] -= 1
            elif game['direction'] == 8:
                body_add[0] -= 1
            game['body'].insert(0, body_add)

        while game['spawn_food']:
            game['food'] = [random.randint(1, 6), random.randint(1, 6)]
            if game['food'] not in game['body'] and game['food'] != game['head']:
                game['spawn_food'] = False

        plot = await self.plot_grid()
        message = await ctx.channel.send(plot)
        clockwise = '\U0001F503'
        counter_clockwise = '\U0001F504'
        await message.add_reaction(counter_clockwise)
        await message.add_reaction(clockwise)

        time.sleep(5)
        message = await message.channel.fetch_message(message.id)
        clockwise_reactions = discord.utils.get(message.reactions, emoji='🔃')
        counter_clockwise_reactions = discord.utils.get(message.reactions, emoji='🔄')
        
        if clockwise_reactions and counter_clockwise_reactions:
            if clockwise_reactions.count > counter_clockwise_reactions.count:
                if game['direction'] == 2:
                    game['direction'] = 4
                elif game['direction'] == 4:
                    game['direction'] = 8
                elif game['direction'] == 6:
                    game['direction'] = 2
                elif game['direction'] == 8:
                    game['direction'] = 6
            elif clockwise_reactions.count < counter_clockwise_reactions.count:
                if game['direction'] == 2:
                    game['direction'] = 6
                elif game['direction'] == 4:
                    game['direction'] = 8
                elif game['direction'] == 6:
                    game['direction'] = 8
                elif game['direction'] == 8:
                    game['direction'] = 4

        if not (await self.game_over_check(message)):
            await self.update_grid(message)
        
    async def plot_grid(self):
        plot = ""
        for x in range(0, 8):
            for y in range(0, 8):
                if [x, y] == game['head']:
                    plot += game['elements'][0]
                elif [x, y] in game['body']:
                    plot += game['elements'][1]
                elif [x, y] == game['food']:
                    plot += game['elements'][4]
                elif x == 0 or y == 0 or x == 7 or y == 7:
                    plot += game['elements'][3]
                else:
                    plot += game['elements'][2]
            plot += '\n'
        return plot
    
    async def game_over_check(self, ctx):
        if game['head'][0] == 0 or game['head'][0] == 7 or game['head'][1] == 0 or game['head'][1] == 7:
            await ctx.channel.send(f'Game Over!\nCurrent Score: {game["current_score"]}\nHigh Score: {game["high_score"]}')
            if game["current_score"] > game["high_score"]:
                game["high_score"] = game["current_score"]
                await ctx.channel.send("New High Score!!")
            game['game'] = False
            game['head'] = [1, 1]
            game['length'] = 0
            game['direction'] = 6
            game['body'] = []
            game['spawn_food'] = True
            game['food'] = []
            return True
        if game['head'] in game['body']:
            await ctx.channel.send(f'Game Over!\nCurrent Score: {game["current_score"]}\nHigh Score: {game["high_score"]}')
            if game["current_score"] > game["high_score"]:
                game["high_score"] = game["current_score"]
                await ctx.channel.send("New High Score!!")
            game['game'] = False
            game['head'] = [1, 1]
            game['length'] = 0
            game['direction'] = 6
            game['body'] = []
            game['spawn_food'] = True
            game['food'] = []
            return True
        return False

def setup(bot):
    bot.add_cog(Snakegame(bot))