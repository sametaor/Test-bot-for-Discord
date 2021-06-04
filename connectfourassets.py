import discord
from discord.ext import commands,tasks
import random
import asyncio
import time

player1 = ""
player2 = ""
turn = ""
numturn = 0
count_render = 0
board_render = []
board = [
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0]
]
gameOver = True
modes = 1