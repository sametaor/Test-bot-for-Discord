import nextcord
import asyncio
import aiohttp
import json
from nextcord import Member
from typing import Optional
from io import BytesIO
from nextcord.ext import commands

class Moderation(commands.Cog):
    """Manage your server with these helpful tools!"""
    COG_EMOJI = "🛠"
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, msg):
        for file in msg.attachments:
            if file.filename.endswith((".exe", ".dll", ".xlsx")):
                await msg.delete()
                await msg.channel.send("No .exe, .dll or .xlsx files allowed!")

    @commands.command(description="Toggles commands to be enabled or disabled")
    @commands.has_guild_permissions(ban_members=True)
    async def toggle(self, ctx, *, command):
        command = self.bot.get_command(command)
        if command == None:
            await ctx.send("Command not found")
        elif ctx.command == command:
            await ctx.send("You cannot disable this command")
        else:
            command.enabled = not command.enabled
            togglecommand = "enabled" if command.enabled else "disabled"
            await ctx.send(f"{command.qualified_name} command has been {togglecommand}.")

    @commands.command(aliases=["clear", "delete"])
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount=2):
        await ctx.channel.purge(limit=amount)

    @commands.command(aliases=["remove"])
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, target : Optional[Member],*, reason="No reason provided"):
        target = target or ctx.author
        if target == ctx.author:
            await ctx.send("You cannot kick yourself")
        else:
            try:
                await target.send(f"You have been kicked from{ctx.guild.name} for the following reason: " + reason)
            except:
                await ctx.send("The member has their DMs closed.")
            await target.kick(reason=reason)

    @commands.command(brief="Bans members from the server")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, target : Optional[Member], reason="No reason provided"):
        target = target or ctx.author
        if target == ctx.author:
            await ctx.send("You cannot ban yourself")
        else:
            await target.send(f"You have been banned from {ctx.guild.name} for the following reason: " + reason)
            await ctx.send(target.name + f" has been banned from {ctx.guild.name} for the following reason: " + reason)
            await target.ban(reason=reason)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx,*,member):
        banned_users = await ctx.guild.bans()
        for banned_entry in banned_users:
            user = banned_entry.user

            if user==member:
                await ctx.guild.unban(user)
                await ctx.send(member + f" has been unbanned from {ctx.guild.name}")
                return

        await ctx.send(member + " was not found.")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, target : Optional[Member], *, reason=None):
        target = target or ctx.author
        if target is None:
            await ctx.send('Please provide a member.')
        elif target == self.bot.user:
            await ctx.send('You cannot warn a bot member.')
        elif target == ctx.author:
            await ctx.send('You cannot warn yourself.')
        else:
            await ctx.message.delete()
            try:
                await target.send(f'You have been warned in {ctx.guild.name} for the following reason: {reason}')
            except:
                await ctx.send("Couldn't send warn message because member has their DMs closed")

            embed = nextcord.Embed(title="Warn", description=f'{target.mention}', colour = nextcord.Colour.red())
            embed.add_field(name="Reason:", value=f'{reason}')
            embed.add_field(name="Warned by:", value=f'{ctx.author.mention}', inline=False)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx,target : Optional[Member], *, reason=None):
        guild = ctx.guild
        target = target or ctx.author
        muted_role = nextcord.utils.get(guild.roles, name="Muted")

        if not muted_role:
            muted_role = await guild.create_role(name="Muted")

            for channel in guild.channels:
                await channel.set_permissions(muted_role, speak=False, send_messages=False, stream=False, attach_files=False, mention_everyone=False, external_emojis=False, connect=False, read_messages=False)
        if target == ctx.author:
            await ctx.send("You cannot mute yourself")
        else:
            await target.add_roles(muted_role, reason=reason)
            await ctx.send(f"{target.mention} has been muted for the following reason: {reason}.")
            await target.send(f"You were muted in {guild.name} for the following reason: {reason}.")

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx,target : Optional[Member]):
        guild = ctx.guild
        target = target or ctx.author
        mutedRole = nextcord.utils.get(ctx.guild.roles, name="Muted")

        await target.remove_roles(mutedRole)
        await ctx.send(f"{target.mention} has been unmuted.")
        await target.send(f"You were unmuted in {guild.name}.")

    @commands.command()
    async def tempmute(self, ctx, target : Optional[Member]=None, time=None, *, reason=None):
        if target == None:
            await ctx.send("You must mention a member to mute!")
        elif target == ctx.author:
            await ctx.send("You cannot tempmute yourself!")
        elif not time:
            await ctx.send("You must mention a time!")
        else:
            if not reason:
                reason="No reason"
            #Now timed mute manipulation
        try:
            time_interval = time[:-1] #Gets the numbers from the time argument, start to -1
            duration = time[-1] #Gets the timed manipulation, s, m, h, d
            if duration == "s":
                time_interval = time_interval * 1
            elif duration == "m":
                time_interval = time_interval * 60
            elif duration == "h":
                time_interval = time_interval * 60 * 60
            elif duration == "d":
                time_interval = time_interval * 86400
            else:
                await ctx.send("Invalid duration input")
                return
        except Exception as e:
            print(e)
            await ctx.send("Invalid time input")
            return
        guild = ctx.guild
        Muted = nextcord.utils.get(guild.roles, name="Muted")
        if not Muted:
            Muted = await guild.create_role(name="Muted")
            for channel in guild.channels:
                await channel.set_permissions(Muted, speak=False, send_messages=False, read_message_history=True, read_messages=False)
        else:
            await target.add_roles(Muted, reason=reason)
            muted_embed = nextcord.Embed(title="Tempmuted a user", description=f"{target.mention} Was muted for {reason} for {time}", colour=nextcord.Colour.dark_red())
            await ctx.send(embed=muted_embed)
            await asyncio.sleep(int(time_interval))
            await target.remove_roles(Muted)
            unmute_embed = nextcord.Embed(title='Tempmute over!', description=f'{target.mention} has been unmuted for {reason} after {time}', colour=nextcord.Colour.green())
            await ctx.send(embed=unmute_embed)

    @commands.command(aliases=["lock", "ld"])
    @commands.has_permissions(manage_messages=True)
    async def lockdown(self, ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        await ctx.send(ctx.channel.mention + "is now set to lockdown mode.")

    @commands.command(aliases=["ul"])
    @commands.has_permissions(manage_messages=True)
    async def unlock(self, ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
        await ctx.send("Lockdown mode is now removed for " + ctx.channel.mention)

    @commands.command(aliases=["sm", "slow"])
    @commands.has_permissions(manage_messages=True)
    async def slowmode(self, ctx, seconds : int):
        await ctx.channel.edit(slowmode_delay=seconds)
        await ctx.send(f"The slowmode is now set to {seconds} seconds.")

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_nicknames=True)
    async def nickset(self, ctx, target : Optional[Member], nick):
            await target.edit(nick=nick)
            await ctx.send(f"Nickname changed for {target.mention}.")
    
    @commands.command()
    @commands.has_permissions(read_message_history=True)
    async def firstmsg(self, ctx):
        async for message in ctx.channel.history(limit=1, oldest_first=True):
            await ctx.send(f"{message.content} - {message.author}")
    
    @commands.command()
    @commands.has_permissions(read_message_history=True)
    async def search(self, ctx, *, keyword: str):
        async for message in ctx.channel.history(limit=10, oldest_first=True):
            if keyword in message.content:
                embed = nextcord.Embed()
                embed.description = f"[{message.content}]({message.jump_url})"
                await ctx.send(embed=embed)
    
    @commands.command()
    @commands.has_permissions(manage_emojis_and_stickers=True)
    async def addemoji(self, ctx, url:str, *, name):
        guild = ctx.guild
        async with aiohttp.ClientSession() as ses:
            async with ses.get(url) as r:
                try:
                    imgorgif = BytesIO(await r.read())
                    bvalue = imgorgif.getvalue()
                    if r.status in range(200, 299):
                        emoji = await guild.create_custom_emoji(image=bvalue, name=name)
                        await ctx.send("Successfully added the given emoji!\n" + f"{emoji}")
                        await ses.close()
                    else:
                        await ctx.send(f"An error occured: {r.status}")
                except nextcord.HTTPException:
                    await ctx.send("Error: The file is too large(must be under 256 kb in size)")
    
    @commands.command()
    @commands.has_permissions(manage_emojis_and_stickers=True)
    async def delemoji(self, ctx, emoji: nextcord.Emoji):
        await ctx.send("Successfully removed the given emoji!\n" + f"{emoji}")
        await emoji.delete()
    
    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def new(self, ctx):
        await ctx.send("Invalid sub-command passed.")

    @new.command()
    @commands.guild_only()
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def category(self, ctx, role: nextcord.Role, *, name):
        overwrites = {
        ctx.guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
        ctx.guild.me: nextcord.PermissionOverwrite(read_messages=True),
        role: nextcord.PermissionOverwrite(read_messages=True)
        }
        category = await ctx.guild.create_category(name=name, overwrites=overwrites)
        await ctx.send(f"New category {category.name} has been created!")

    @new.command()
    @commands.guild_only()
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    async def channel(self, ctx, role: nextcord.Role, *, name):
        overwrites = {
        ctx.guild.default_role: nextcord.PermissionOverwrite(read_messages=False),
        ctx.guild.me: nextcord.PermissionOverwrite(read_messages=True),
        role: nextcord.PermissionOverwrite(read_messages=True)
        }
        channel = await ctx.guild.create_text_channel(name=name, overwrites=overwrites)
        await ctx.send(f"New channel {channel.name} has been created!")

def setup(bot):
    bot.add_cog(Moderation(bot))