import discord, datetime, time
from discord.ext import commands
import sys
from packages.server import start_time
from packages.utils import Embed, ImproperType

class Command(commands.Cog):

    def __init__(self, client):
        self.client= client

    @commands.command()
    async def uptime(self, ctx):
        current_time = time.time()
        difference = int(round(current_time - start_time))
        uptime = str(datetime.timedelta(seconds=difference))
        embed = Embed(':green_circle:  Lacan NTSport\'s Uptime','Check my uptime stats!', color=0xc8dc6c)
        embed.field(name="__Uptime__", value='`'+uptime+'`')
        embed.field(name=':birthday: __Birthday__', value="**Fri, May 22, 2020 7:29 AM**")
        try:
            await embed.send(ctx)
        except discord.HTTPException:
            await ctx.send("Current uptime: " + uptime)
def setup(client):
    client.add_cog(Command(client))