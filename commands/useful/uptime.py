import discord, datetime, time
from discord.ext import commands
import sys
from packages.server import start_time, run_time
from packages.utils import Embed, ImproperType

class Command(commands.Cog):

    def __init__(self, client):
        self.client= client

    @commands.command()
    async def uptime(self, ctx):
      # Uptime
        current_time = time.time()
        difference = int(round(current_time - start_time))
        uptime = str(datetime.timedelta(seconds=difference))
      # Runtime
        current_time2 = time.time()
        difference2 = int(round(current_time2 - run_time))
        uptime2 = str(datetime.timedelta(seconds=difference2))
      # Embed
        embed = Embed(':green_circle:  Lacan NTSport\'s Uptime','Check my uptime stats!', color=0xc8dc6c)
      # Embed Fields
        # Uptime
        embed.field(name="__Uptime__", value='`'+uptime+'`')
        # Runtime
        embed.field(name="__Runtime__", value='`'+uptime2+'`')
        # Birthday
        embed.field(name=':birthday: __Birthday__', value="**Fri, May 22, 2020 7:29 AM**")
        # Explaination
        embed.field(name="Restarting", value="The uptime resets every hour because of the bot being automatically restarted.")
        try:
            await embed.send(ctx)
        except discord.HTTPException:
            await ctx.send("Current uptime: " + uptime)
def setup(client):
    client.add_cog(Command(client))