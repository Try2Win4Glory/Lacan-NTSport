'''Reroll The Winner!'''

from discord.ext import commands
from packages.utils import Embed, ImproperType
from mongoclient import DBClient
class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def reroll(self, ctx):
        dbclient = DBClient()
    
def setup(client):
    client.add_cog(Command(client))