import wavelink
import nextcord
import datetime
from nextcord.ext import commands

async def node_connect(self):
    await self.bot.wait_until_ready()
    await wavelink.NodePool.create_node(bot = self.bot, host='lavalinkinc.ml', port=443, password='incognito', https=True)

class Music(commands.Cog):
    """Play music right on Discord!"""
    COG_EMOJI = '🎶'
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.loop.create_task(node_connect(self))
    
    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        print(f"Node {node.identifier} is ready!")
    
    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    async  def play(self, ctx):
        await ctx.send("Invalid sub-command passed.")
    
    @play.command()
    async def track(self, ctx: commands.Context, *, search: wavelink.YouTubeTrack):
        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("Please join a Voice Channel first, and then type '&play track <query>'")
        else:
            vc: wavelink.Player = ctx.voice_client
        
        await vc.play(search)
        conversion = datetime.timedelta(seconds=search.duration)
        musicduration = str(conversion)
        musicembed = nextcord.Embed(title="Now Playing", description=f"Song: [{search.title}]({search.uri})\n Artist: `{search.author}`\n Duration: `{musicduration}`")
        musicembed.set_thumbnail(url=search.thumb)
        await ctx.send(embed=musicembed)

    @commands.command()
    async def pause(self, ctx: commands.Context):
        if not ctx.voice_client:
            return await ctx.send("There is nothing playing right now")
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("Please join a Voice Channel first, and then type '&pause'")
        else:
            vc: wavelink.Player = ctx.voice_client
        
        await vc.pause()
        await ctx.send("Pausing currently playing music...")
    
    @commands.command()
    async def resume(self, ctx: commands.Context):
        if not ctx.voice_client:
            return await ctx.send("No song is present to be resumed right now")
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("Please join a Voice Channel first, and then type '&resume'")
        else:
            vc: wavelink.Player = ctx.voice_client
        
        await vc.resume()
        await ctx.send("Resuming selected music...")
    
    @commands.command()
    async def stop(self, ctx: commands.Context):
        if not ctx.voice_client:
            return await ctx.send("No song is present to be stopped right now")
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("Please join a Voice Channel first, and then type '&stop'")
        else:
            vc: wavelink.Player = ctx.voice_client
        
        await vc.stop()
        await ctx.send("Stopping current song...")
    
    @commands.command()
    async def disconnect(self, ctx: commands.Context):
        if not ctx.voice_client:
            return await ctx.send("I am not connected to any voice channel yet")
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("Please join a Voice Channel first, and then type '&disconnect'")
        else:
            vc: wavelink.Player = ctx.voice_client
        
        await vc.disconnect()
        await ctx.send("Disconnecting from Voice Channel...")
    
    @commands.command()
    async def volume(self, ctx: commands.Context, volumevalue = None):
        if not ctx.voice_client:
            return await ctx.send("There is no song for changing the volume of")
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("Please join a Voice Channel first, and then type '&play track <query>'")
        else:
            vc: wavelink.Player = ctx.voice_client
        
        await vc.set_volume(int(volumevalue))
        await ctx.send(f"Changing Volume to `{volumevalue}`...")

def setup(bot):
    bot.add_cog(Music(bot))