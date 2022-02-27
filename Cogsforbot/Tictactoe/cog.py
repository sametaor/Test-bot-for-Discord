import nextcord
from nextcord.ext import commands
import random

player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [
    [0, 1, 2],
    [3, 4 ,5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

class Tictactoe(commands.Cog, name="Tictactoe"):
    """Play a relaxing game of Tictactoe on Discord!"""
    COG_EMOJI = nextcord.PartialEmoji(name="tictactoe", id=947407376070373407, animated=False)
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=["ttt"])
    async def tictactoe(self, ctx, p1 : nextcord.Member, p2 : nextcord.Member):
        global player1
        global player2
        global turn
        global gameOver
        global count

        if gameOver:
            global board
            await ctx.send(embed = nextcord.Embed(title="To see what each square's number is type &tttboard"))
            board = ["⬜", "⬜", "⬜",
                    "⬜", "⬜", "⬜",
                    "⬜", "⬜", "⬜"]

            turn = ""
            gameOver = False
            count = 0


            player1 = p1
            player2 = p2

            line = ""
            for x in range(len(board)):
                if x == 2 or x == 5 or x ==8:
                    line += " " + board[x]
                    await ctx.send(line)
                    line = ""
                else:
                    line += " " + board[x]


            num =random.randint(1, 2)
            if num == 1:
                turn = player1
                await ctx.send(f"It's {player1.mention}'s turn!")
            elif num == 2:
                turn = player2
                await ctx.send(f"It's {player2.mention}'s turn!")
        else:
            await ctx.send("⭕There is still an ongoing match of tictactoe, please wait for it to end❌")

    @commands.command(aliases=["tictactoeplace"])
    async def tttplace(self, ctx, pos : int):
        global turn
        global player1
        global player2
        global board
        global count

        if not gameOver:
            mark = ""
            if turn == ctx.author:
                if turn == player1:
                    mark = ":x:"
                elif turn == player2:
                    mark = ":o:"
                if 0 < pos < 10 and board[pos - 1] == "⬜":
                    board[pos - 1] = mark
                    count += 1

                    line = ""
                    for x in range(len(board)):
                        if x == 2 or x == 5 or x ==8:
                            line += " " + board[x]
                            await ctx.send(line)
                            line = ""
                        else:
                            line += " " + board[x]

                    checkWinner(winningConditions, mark)
                    if gameOver:
                        await ctx.send(mark + " wins!")
                    elif count >= 9:
                        await ctx.send("It's a tie!")
                        tie()

                    #switch turns
                    if turn == player1:
                        turn = player2
                    elif turn ==player2:
                        turn = player1

                else:
                    await ctx.send("Be sure to choose an integer between 1 and 9 and an unmarked tile")
            else:
                await ctx.send("It is not your turn yet. Please wait for your turn.")
        else:
            await ctx.send('⭕There are no ongoing tictactoe matches going on. Use the "&tictactoe" command to start a new one!❌')

    @commands.command(aliases=["tictactoeend"])
    async def tttend(self, ctx):
        global gameOver
        if not gameOver:
            gameOver = True
            await ctx.send("Stopping current game...")
        else:
            await ctx.send("⭕There is currently no game running!❌")

    @commands.command(aliases=["tictactoeboard"])
    async def tttboard(self, ctx):
        embed = nextcord.Embed(title="What each square's number is", description = ":one::two::three:\n:four::five::six:\n:seven::eight::nine:")
        await ctx.send(embed = embed)

    @tictactoe.error
    async def tictactoe_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please mention two players for this command")
        if isinstance(error, commands.BadArgument):
            await ctx.send("Please make sure to mention/ping players (e.g <@123456789123456789>).")

    @tttplace.error
    async def place_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Please enter the position you'd like to mark")
        if isinstance(error, commands.BadArgument):
            await ctx.send("Please make sure to enter an integer.")

def tie():
    global gameOver
    gameOver = True

def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True

def setup(bot):
    bot.add_cog(Tictactoe(bot)) 