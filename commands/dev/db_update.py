'''description'''

from discord.ext import commands
from packages.utils import Embed, ImproperType

class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def db_update(self, ctx):
        if ctx.author.id != 396075607420567552:
            return
        
def setup(client):
    client.add_cog(Command(client))