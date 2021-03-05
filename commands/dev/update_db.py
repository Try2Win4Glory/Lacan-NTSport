'''Update the database'''

from discord.ext import commands
from packages.utils import Embed, ImproperType
from mongoclient import DBClient
import json
class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def update_db(self, ctx):
        return
        f = open('pointsdb.json')
        data = json.loads(f.read())
        dbclient = DBClient()
        collection = dbclient.db.pointsdb
        for user in data['users']:
            await dbclient.create_doc(collection, user)
    
def setup(client):
    client.add_cog(Command(client))