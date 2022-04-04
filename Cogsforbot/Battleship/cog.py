import discord
from discord.ext import commands
import random

class BattleShip(commands.Cog):
	"""Play an intense game of Battleship on Discord!"""
	COG_EMOJI = '⚓'
	
	def __init__(self, bot):
		self.bot = bot
	
	@commands.command(help='Play battleship with a member.')
	async def battleship(self, ctx, member:discord.Member):
		
		game_config_1 = {}
		game_config_2 = {}
		cr_player = member
		player = ctx.author
		counter = 42
		ac = '🟢'
		bs = '🟢'
		mc = '🟢'
		bq = '🟦'
		baq = '🟥'
		gq = '🟫'
		
		isFinished = False
		bothDone = 0
		hidden_config_1 = {}
		hidden_config_2 = {}
		winner = None
		
		baqstr = f'\n{baq*7}\n'
		los = [ac,bs,mc]
		coords = []

		counter2 = 0
		alp = ['a','b','c','d','e','f']
		for item in alp:
			for num in range(1,8):
				coords.append(item+str(num))
		for item in coords:
			hidden_config_1[item] = gq
		for item in coords:
			hidden_config_2[item] = gq
		for item in coords:
			game_config_1[item] = bq 

		for item in range(5):
			choice = random.choice(coords)
			while game_config_1[choice] == ac or game_config_1[choice] == bs or game_config_1[choice] == mc:
				choice = random.choice(coords)
			game_config_1[choice] = random.choice(los)
		for item in coords:
			game_config_2[item] = bq 
		for item in range(5):
			choice = random.choice(coords)
			while game_config_2[choice] == ac or game_config_2[choice] == bs or game_config_2[choice] == mc:
				choice = random.choice(coords)
			game_config_2[choice] = random.choice(los)
		bstr = ''
		rand = False
		for item in coords:
			bstr += game_config_1[item]
			if coords.index(item) % 7 == 0 and item != coords[0] and rand == False:
				bstr += '\n'
			if coords.index(item) == 6 or coords.index(item) == 13 or coords.index(item) == 20 or coords.index(item) == 27 or coords.index(item) == 34 or coords.index(item) == 41:
				bstr += '\n'
				rand = True
			if ((coords.index(item) > 7 and coords.index(item) <= 12) or (coords.index(item) > 14 and coords.index(item) <= 19) or (coords.index(item) > 21 and coords.index(item) <= 26) or (coords.index(item) > 28 and coords.index(item) <= 33) or (coords.index(item) > 36 and coords.index(item) <= 41)) and rand == True:
				rand = False
		bstr += '\n'
		bstr += baq*7
		bstr += '\n'
		rand = False

		for item in coords:
			bstr += game_config_2[item]
			if coords.index(item) % 7 == 0 and item != coords[0] and rand == False:
				bstr += '\n'
			if coords.index(item) == 6 or coords.index(item) == 13 or coords.index(item) == 20 or coords.index(item) == 27 or coords.index(item) == 34 or coords.index(item) == 41:
				bstr += '\n'
				rand = True
			if ((coords.index(item) > 7 and coords.index(item) <= 12) or (coords.index(item) > 14 and coords.index(item) <= 19) or (coords.index(item) > 21 and coords.index(item) <= 26) or (coords.index(item) > 28 and coords.index(item) <= 33) or (coords.index(item) > 36 and coords.index(item) <= 41) or coords.index(item) == 41) and rand == True:
				rand = False
		
		lst = []
		s = bstr.split('\n')
		for num, i in enumerate(s):
			if num == 6:
				lst.append(str(i))
			else:
				lst.append(str(i)+'\n')
		bstr = ''.join(lst)
		lst = []
		s = bstr.split('\n')
		for num, i in enumerate(s):
			if num == 12:
				lst.append(str(i))
			else:
				lst.append(str(i)+'\n')
		
		bstr = ''.join(lst)
		hstr = ''
		hstr2 = ''
		for item in coords:
			hstr += hidden_config_1[item]
			if coords.index(item) % 7 == 0 and item != coords[0] and rand == False:
				hstr += '\n'
			if coords.index(item) == 6 or coords.index(item) == 13 or coords.index(item) == 20 or coords.index(item) == 27 or coords.index(item) == 34 or coords.index(item) == 41:
				hstr += '\n'
				rand = True
			if ((coords.index(item) > 7 and coords.index(item) <= 12) or (coords.index(item) > 14 and coords.index(item) <= 19) or (coords.index(item) > 21 and coords.index(item) <= 26) or (coords.index(item) > 28 and coords.index(item) <= 33) or (coords.index(item) > 36 and coords.index(item) <= 41) or coords.index(item) == 41) and rand == True:
				rand = False
		lst = []
		s = hstr.split('\n')
		for num, i in enumerate(s):
			if num == 6:
				lst.append(str(i))
			else:
				lst.append(str(i)+'\n')
		hstr = ''.join(lst)
		for item in coords:
			hstr2 += hidden_config_2[item]
			if coords.index(item) % 7 == 0 and item != coords[0] and rand == False:
				hstr += '\n'
			if coords.index(item) == 6 or coords.index(item) == 13 or coords.index(item) == 20 or coords.index(item) == 27 or coords.index(item) == 34 or coords.index(item) == 41:
				hstr2 += '\n'
				rand = True
			if ((coords.index(item) > 7 and coords.index(item) <= 12) or (coords.index(item) > 14 and coords.index(item) <= 19) or (coords.index(item) > 21 and coords.index(item) <= 26) or (coords.index(item) > 28 and coords.index(item) <= 33) or (coords.index(item) > 36 and coords.index(item) <= 41) or coords.index(item) == 41) and rand == True:
				rand = False
		for num in range(2):
			lst = []
			s = hstr2.split('\n')
			for num, i in enumerate(s):
				if num == 6:
					lst.append(str(i))
				else:
					lst.append(str(i)+'\n')
			hstr2 = ''.join(lst)
		p1str, p2str = bstr.split(f'\n{baq*7}\n')
		letterdict = {1:'🇧',2:'🇨',3:'🇩',4:'🇪',5:'🇫'}

		while isFinished == False:
			
			
			if bothDone == 0:
				actions = {}
			def check(m):
				return m.author == cr_player and m.channel == ctx.channel
			if cr_player == member:
				em1 = discord.Embed(title=f'BattleShip | {player.name} vs {member.name}',color=discord.Color.gold())
				em1.add_field(name='Your board',value=p1str,inline=True)
				em1.add_field(name='Opponent\'s board',value=hstr,inline=False)
				em3 = discord.Embed(title=f'BattleShip | {player.name} vs {member.name}',color=discord.Color.gold())
				em3.add_field(name='Opponent\'s board',value=hstr,inline=False)
			else:
				em1 = discord.Embed(title=f'BattleShip | {player.name} vs {member.name}',color=discord.Color.gold())
				em1.add_field(name='Your board',value=p2str,inline=True)
				em1.add_field(name='Opponent\'s board',value=hstr2[0:-1],inline=False)
				em3 = discord.Embed(title=f'BattleShip | {player.name} vs {member.name}',color=discord.Color.gold())
				em3.add_field(name='Opponent\'s board',value=hstr2[0:-1],inline=False)
			em1.add_field(name='Reference board', value="⏹1️⃣2️⃣3️⃣4️⃣5️⃣6️⃣7️⃣\n:regional_indicator_a:"+ ("⬛"*7)+"\n:regional_indicator_b:"+ ("⬛"*7)+"\n:regional_indicator_c:"+ ("⬛"*7)+"\n:regional_indicator_d:"+ ("⬛"*7)+"\n:regional_indicator_e:"+ ("⬛"*7)+"\n:regional_indicator_f:"+ ("⬛"*7), inline= False)
			em1.add_field(name='Icons',value='🟢 = Ship\n🟦 = Water\n🟫 = Unknown Territory\n💥 = Hit a Ship\n❌ = Aimed but Missed',inline=True)
			em1.add_field(name='How to play?',value='The game works on a grid system, with \nletters being the rows and numbers \nbeing the colummns.\nFor example: `a1` for the top left and `f7` for the bottom right.')
			
			em3.add_field(name='Reference board', value="⏹1️⃣2️⃣3️⃣4️⃣5️⃣6️⃣7️⃣\n:regional_indicator_a:"+ ("⬛"*7)+"\n:regional_indicator_b:"+ ("⬛"*7)+"\n:regional_indicator_c:"+ ("⬛"*7)+"\n:regional_indicator_d:"+ ("⬛"*7)+"\n:regional_indicator_e:"+ ("⬛"*7)+"\n:regional_indicator_f:"+ ("⬛"*7), inline= False)
			em3.add_field(name='Icons',value='🟢 = Ship\n🟦 = Water\n🟫 = Unknown Territory\n💥 = Hit a Ship\n❌ = Aimed but Missed',inline=True)
			em3.add_field(name='How to play?',value='The game works on a grid system, with \nletters being the rows and numbers \nbeing the colummns.\nFor example: `a1` for the top left and `f7` for the bottom right.')

			await cr_player.send(embed=em1)
			await ctx.send(embed=em3)
			await ctx.send(f'{cr_player.mention}, enter your square below!')
			sq2 = ''
			while sq2 not in coords: 
				sq1 = await self.bot.wait_for('message',check=check)
				if sq1.content == 'cancel':
					canbed = discord.Embed(title='Canceled',description=f'{cr_player.name} canceled the game :(',color=discord.Color.red())
					await ctx.send(embed=canbed)
					await ctx.send(embed=canbed)
					return
				sq2 = sq1.content
				
				if sq2 not in coords:
					em2 = discord.Embed(title='Error',description='Please enter a valid square/coordinate!',color=discord.Color.red())
					await ctx.send(embed=em2)

			if cr_player == member: 
				if game_config_2[sq2] == ac or game_config_2[sq2] == bs or game_config_2[sq2] == mc:
					actions[cr_player] = f'{cr_player.name} hit a ship! BOOM!'
					yq = '💥'
				else:
					actions[cr_player] = f'{cr_player.name} guessed well but unfortunately missed :('
					yq = '❌'
			else: 
				if game_config_1[sq2] == ac or game_config_1[sq2] == bs or game_config_1[sq2] == mc:
					actions[cr_player] = f'{cr_player.name} hit a ship! BOOM!'
					yq = '💥'
				else:
					actions[cr_player] = f'{cr_player.name} guessed well but unfortunately missed :('
					yq = '❌'
			if cr_player == member:
				hidden_config_1[sq2] = yq
				game_config_2[sq2] = yq
				sq3 = sq2
			else:
				hidden_config_2[sq2] = yq
				game_config_1[sq2] = yq
				sq4 = sq2
			bstr = ''
			rand = False
			for item in coords:
				bstr += game_config_1[item]
				if coords.index(item) % 7 == 0 and item != coords[0] and rand == False:
					bstr += '\n'
				if coords.index(item) == 6 or coords.index(item) == 13 or coords.index(item) == 20 or coords.index(item) == 27 or coords.index(item) == 34 or coords.index(item) == 41:
					bstr += '\n'
					rand = True
				if ((coords.index(item) > 7 and coords.index(item) <= 12) or (coords.index(item) > 14 and coords.index(item) <= 19) or (coords.index(item) > 21 and coords.index(item) <= 26) or (coords.index(item) > 28 and coords.index(item) <= 33) or (coords.index(item) > 36 and coords.index(item) <= 41)) and rand == True:
					rand = False
			bstr += '\n'
			bstr += baq*7
			bstr += '\n'
			rand = False

			for item in coords:
				bstr += game_config_2[item]
				if coords.index(item) % 7 == 0 and item != coords[0] and rand == False:
					bstr += '\n'
				if coords.index(item) == 6 or coords.index(item) == 13 or coords.index(item) == 20 or coords.index(item) == 27 or coords.index(item) == 34 or coords.index(item) == 41:
					bstr += '\n'
					rand = True
				if ((coords.index(item) > 7 and coords.index(item) <= 12) or (coords.index(item) > 14 and coords.index(item) <= 19) or (coords.index(item) > 21 and coords.index(item) <= 26) or (coords.index(item) > 28 and coords.index(item) <= 33) or (coords.index(item) > 36 and coords.index(item) <= 41) or coords.index(item) == 41) and rand == True:
					rand = False
		
			lst = []
			s = bstr.split('\n')
			for num, i in enumerate(s):
				if num == 6:
					lst.append(str(i))
				else:
					lst.append(str(i)+'\n')
			bstr = ''.join(lst)
			lst = []
			s = bstr.split('\n')
			for num, i in enumerate(s):
				if num == 12:
					lst.append(str(i))
				else:
					lst.append(str(i)+'\n')
			bstr = ''.join(lst)
			hstr = ''
			hstr2 = ''
			for item in coords:
				hstr += hidden_config_1[item]
				if coords.index(item) % 7 == 0 and item != coords[0] and rand == False:
					hstr += '\n'
				if coords.index(item) == 6 or coords.index(item) == 13 or coords.index(item) == 20 or coords.index(item) == 27 or coords.index(item) == 34 or coords.index(item) == 41:
					hstr += '\n'
					rand = True
				if ((coords.index(item) > 7 and coords.index(item) <= 12) or (coords.index(item) > 14 and coords.index(item) <= 19) or (coords.index(item) > 21 and coords.index(item) <= 26) or (coords.index(item) > 28 and coords.index(item) <= 33) or (coords.index(item) > 36 and coords.index(item) <= 41) or coords.index(item) == 41) and rand == True:
					rand = False
			lst = []
			s = hstr.split('\n')
			for num, i in enumerate(s):
				if num == 6:
					lst.append(str(i))
				else:
					lst.append(str(i)+'\n')
			hstr = ''.join(lst)
			for item in coords:
				hstr2 += hidden_config_2[item]
				if coords.index(item) % 7 == 0 and item != coords[0] and rand == False:
					hstr += '\n'
				if coords.index(item) == 6 or coords.index(item) == 13 or coords.index(item) == 20 or coords.index(item) == 27 or coords.index(item) == 34 or coords.index(item) == 41:
					hstr2 += '\n'
					rand = True
				if ((coords.index(item) > 7 and coords.index(item) <= 12) or (coords.index(item) > 14 and coords.index(item) <= 19) or (coords.index(item) > 21 and coords.index(item) <= 26) or (coords.index(item) > 28 and coords.index(item) <= 33) or (coords.index(item) > 36 and coords.index(item) <= 41) or coords.index(item) == 41) and rand == True:
					rand = False
			for num in range(2):
				lst = []
				s = hstr2.split('\n')
				for num, i in enumerate(s):
					if num == 6:
						lst.append(str(i))
					else:
						lst.append(str(i)+'\n')
				hstr2 = ''.join(lst)
			p1str, p2str = bstr.split(f'\n{baq*7}\n')
			bothDone += 1
			if bothDone == 2:
				embed = discord.Embed(title=f'Game Status | {player.name} vs {member.name}',color=discord.Color.teal())
				embed.add_field(name=player.name,value=actions[player],inline=False)
				embed.add_field(name=member.name,value=actions[member],inline=False)
				await ctx.send(embed=embed)
				bothDone = 0
			if list(game_config_1.values()).count(ac) == 0 and list(game_config_1.values()).count(bs) == 0 and list(game_config_1.values()).count(mc) == 0:
				winner = player
			elif list(game_config_2.values()).count(ac) == 0 and list(game_config_2.values()).count(bs) == 0 and list(game_config_2.values()).count(mc) == 0:
				winner = member
			else:
				pass
			if not winner == None:
				winbed = discord.Embed(title='Winner!',description=f'{winner.name} has won the battleship game! Congrats! :tada:',color=discord.Color.green())

				await ctx.send(embed=winbed)
				return
			if cr_player == member:
				cr_player = player
			else:
				cr_player = member

def setup(bot):
	bot.add_cog(BattleShip(bot))