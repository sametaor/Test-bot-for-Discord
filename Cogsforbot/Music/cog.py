import wavelink
import nextcord
import datetime
import os
from nextcord.ext import commands
from wavelink.ext import spotify
from dotenv.main import load_dotenv

load_dotenv()

spotifyclientid = os.getenv('SPOTIFYCLIENTID')
spotifyclientsecret = os.getenv('SPOTIFYCLIENTSECRET')

async def node_connect(self):
    await self.bot.wait_until_ready()
    await wavelink.NodePool.create_node(bot = self.bot, host='lavalinkinc.ml', port=443, password='incognito', https=True, spotify_client=spotify.SpotifyClient(client_id=spotifyclientid, client_secret=spotifyclientsecret))

class ControlPanel(nextcord.ui.View):
    def __init__(self, vc, ctx):
        super().__init__()
        self.vc = vc
        self.ctx = ctx
    
    @nextcord.ui.button(label="Play/Pause", style=nextcord.ButtonStyle.blurple)
    async def playnpause(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if not interaction.user == self.ctx.author:
            return await interaction.response.send_message("This is not your embed, you'll need to run your own distinct command to perform the intended action", ephemeral=True)
        for child in self.children:
            child.disabled = False
        if self.vc.is_paused:
            await self.vc.resume()
            await interaction.message.edit(content="Resuming...", view=self)
        else:
            await self.vc.pause()
            await interaction.message.edit(content="Pausing...", view=self)
    
    @nextcord.ui.button(label="Queue", style=nextcord.ButtonStyle.blurple)
    async def queue(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if not interaction.user == self.ctx.author:
            return await interaction.response.send_message("This is not your embed, you'll need to run your own distinct command to perform the intended action", ephemeral=True)
        for child in self.children:
            child.disabled = False
        button.disabled = True
        if self.vc.queue.is_empty:
            return await interaction.response.send_message("Queue is empty!", ephemeral=True)
        
        em = nextcord.Embed(title="Queue")
        queue = self.vc.queue.copy()
        song_count = 0
        for song in queue:
            song_count += 1
            em.add_field(name=f"Song Num {song_count}", value=f"`{song.title}`")
        await interaction.message.edit(embed=em, view=self)
    
    @nextcord.ui.button(label="Skip", style=nextcord.ButtonStyle.blurple)
    async def skip(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if not interaction.user == self.ctx.author:
            return await interaction.response.send_message("This is not your embed, you'll need to run your own distinct command to perform the intended action", ephemeral=True)
        for child in self.children:
            child.disabled = False
        button.disabled = True
        if self.vc.queue.is_empty:
            return await interaction.response.send_message("Queue is empty!", ephemeral=True)
        
        try:
            next_song = self.vc.queue.get()
            await self.vc.play(next_song)
            await interaction.message.edit(content=f"Now Playing `{next_song}`", view=self)
        except Exception:
            await interaction.response.send_message("The queue is empty", ephemeral=True)
    
    @nextcord.ui.button(label="Disconnect", style=nextcord.ButtonStyle.blurple)
    async def disconnect(self, button: nextcord.ui.Button, interaction: nextcord.Interaction):
        if not interaction.user == self.ctx.author:
            return await interaction.response.send_message("This is not your embed, you'll need to run your own distinct command to perform the intended action", ephemeral=True)
        for child in self.children:
            child.disabled = True
        await self.vc.disconnect()
        await interaction.message.edit(content="Disconnecting...", view=self)
        

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
    
    @commands.Cog.listener()
    async def on_wavelink_track_end(self, player: wavelink.Player, track: wavelink.Track, reason):
        try:
            ctx = player.ctx
            vc: player = ctx.voice_client
        except nextcord.HTTPException:
            interaction = player.interaction
            vc: player = interaction.guild.voice_client
            

        if vc.loop:
            return await vc.play(track)

        if not player.queue.is_empty:
            next_song = vc.queue.get()
            await vc.play(next_song)
            try:
                await ctx.send(f"now playing {next_song.title}")
            except nextcord.HTTPException:
                await interaction.send(f"now playing {next_song.title}")
        elif player.queue.is_empty:
            await ctx.send("Queue is empty, use &play <query> to play another song")
            await vc.disconnect()
        
    @commands.command()
    async def musicpanel(self, ctx: commands.Context):
        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("you have to be in a Voice Channel!")
        else:
            vc: wavelink.Player = ctx.voice_client
        if not vc.is_playing():
            return await ctx.send("Please play some music first")
        
        musicpanelembed = nextcord.Embed(title="Tachyon's Music Panel", description="Enjoy your songs and music by clicking on the buttons below!")
        musicview = ControlPanel(vc, ctx)
        await ctx.send(embed=musicpanelembed, view=musicview)
    
    @commands.command()
    async def play(self, ctx: commands.Context, *, search: wavelink.YouTubeTrack):
        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("you have to be in a Voice Channel!")
        else:
            vc: wavelink.Player = ctx.voice_client
        
        if vc.queue.is_empty and not vc.is_playing():
            await vc.play(search)
            conversion = datetime.timedelta(seconds=search.duration)
            musicduration = str(conversion)
            musicembed = nextcord.Embed(title="Now Playing", description=f"Song: [{search.title}]({search.uri})\n Artist: `{search.author}`\n Duration: `{musicduration}`")
            musicembed.set_thumbnail(url=search.thumb)
            await ctx.send(embed=musicembed)
        else:
            await vc.queue.put_wait(search)
            await ctx.send(f"Added `{search.title}` to the queue :)")
        vc.ctx = ctx
        setattr(vc, "loop", False)
    
    @commands.command()
    async def pause(self, ctx: commands.Context):
        if not ctx.voice_client:
            return await ctx.send("There is nothing playing right now")
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("you have to be in a Voice Channel!")
        else:
            vc: wavelink.Player = ctx.voice_client
        
        await vc.pause()
        await ctx.send("Pausing currently playing music...")
    
    @commands.command()
    async def resume(self, ctx: commands.Context):
        if not ctx.voice_client:
            return await ctx.send("There is nothing playing right now")
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("you have to be in a Voice Channel!")
        else:
            vc: wavelink.Player = ctx.voice_client
        
        await vc.resume()
        await ctx.send("Resuming selected music...")
    
    @commands.command()
    async def stop(self, ctx: commands.Context):
        if not ctx.voice_client:
            return await ctx.send("There is nothing playing right now")
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("you have to be in a Voice Channel!")
        else:
            vc: wavelink.Player = ctx.voice_client
        
        await vc.stop()
        await ctx.send("Stopping current song...")
    
    @commands.command()
    async def disconnect(self, ctx: commands.Context):
        if not ctx.voice_client:
            return await ctx.send("There is nothing playing right now")
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("you have to be in a Voice Channel!")
        else:
            vc: wavelink.Player = ctx.voice_client
        
        await vc.disconnect()
        await ctx.send("Disconnecting from Voice Channel...")
    
    @commands.command()
    async def volume(self, ctx: commands.Context, volumevalue = None):
        if not ctx.voice_client:
            return await ctx.send("There is nothing playing right now")
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("you have to be in a Voice Channel!")
        else:
            vc: wavelink.Player = ctx.voice_client
        
        await vc.set_volume(int(volumevalue))
        await ctx.send(f"Changing Volume to `{volumevalue}`...")
    
    @commands.command()
    async def loop(self, ctx:commands.Context):
        if not ctx.voice_client:
            return await ctx.send('There is nothing playing right now')
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send('you have to be in a Voice Channel!')
        else:
            vc: wavelink.Player = ctx.voice_client
        
        try:
            vc.loop ^= True
        except Exception:
            setattr(vc, "loop", False)
        if vc.loop:
            return await ctx.send("Looping is enabled")
        else:
            return await ctx.send("Looping is disabled")
            vc.loop = False
    
    @commands.command()
    async def queue(self, ctx: commands.Context):
        if not ctx.voice_client:
            return await ctx.send("There is nothing playing right now")
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("you have to be in a Voice Channel!")
        else:
            vc: wavelink.Player = ctx.voice_client
        
        if vc.queue.is_empty:
            return await ctx.send("Queue is empty!")
        
        em = nextcord.Embed(title="Queue")
        queue = vc.queue.copy()
        song_count = 0
        for song in queue:
            song_count += 1
            em.add_field(name=f"Song Num {song_count}", value=f"`{song.title}`")
        return await ctx.send(embed=em)
    
    @commands.command()
    async def nowplaying(self, ctx: commands.Context):
        if not ctx.voice_client:
            return await ctx.send("There is nothing playing right now")
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("you have to be in a Voice Channel!")
        else:
            vc: wavelink.Player = ctx.voice_client
        
        if not vc.is_playing():
            return await ctx.send("Nothing is playing right now.")
        
        nowplayingembed  = nextcord.Embed(title=f"Now Playing {vc.track.title}", description=f"Artist {vc.track.author}", url=f"{vc.track.uri}")
        nowplayingembed.add_field(name="Duration", value=f"`{str(datetime.timedelta(seconds=vc.track.length))}`")
        await ctx.send(embed=nowplayingembed)
    
    @commands.command()
    async def spotiplay(self, ctx:commands.Context, *, search: str):
        if not ctx.voice_client:
            vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        elif not getattr(ctx.author.voice, "channel", None):
            return await ctx.send("you have to be in a Voice Channel!")
        else:
            vc: wavelink.Player = ctx.voice_client
        
        if vc.queue.is_empty and not vc.is_playing():
            try:
                track = await spotify.SpotifyTrack.search(query=search, return_first=True)
                await vc.play(track)
                conversion = datetime.timedelta(seconds=track.duration)
                musicduration = str(conversion)
                musicembed = nextcord.Embed(title="Now Playing", description=f"Song: [{track.title}]({track.uri})\n Artist: `{track.author}`\n Duration: `{musicduration}`")
                musicembed.set_thumbnail(url=track.thumb)
                await ctx.send(embed=musicembed)
            except Exception as e:
                await ctx.send("Please enter a Spotify song url")
                return print(e)
        else:
            await vc.queue.put_wait(search)
            await ctx.send(f"Added `{search.title}` to the queue :)")
        vc.ctx = ctx
        if vc.loop:
            return
        setattr(vc, "loop", False)
    
def setup(bot):
    bot.add_cog(Music(bot))