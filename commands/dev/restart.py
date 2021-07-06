'''description'''

from discord.ext import commands
from packages.utils import Embed, ImproperType
import sys, os
class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def restart(self, ctx):
        if ctx.author.id not in [505338178287173642, 396075607420567552]:
            return
        else:
            embed = Embed('Success', 'Refreshed Cache And Restarted Bot!')
            await embed.send(ctx)
            await self.client.logout()
            python = sys.executable
            os.execl(python, python, * sys.argv)
    
def setup(client):
    client.add_cog(Command(client))
