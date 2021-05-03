'''description'''

from discord.ext import commands
from packages.utils import Embed, ImproperType
from mongoclient import DBClient
class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def db_update(self, ctx):
        return
        if ctx.author.id != 396075607420567552:
            return
        await ctx.send('Updating database!')
        dbclient = DBClient()
        collection = dbclient.db.NT_to_discord
        data = await dbclient.get_big_array(collection, 'registered')
        users = []
        for user in data['registered']:
            users.append(user)
        await collection.delete_one({})
        for user in users:
            await dbclient.create_doc(collection, user)
        await ctx.send('done!')
def setup(client):
    client.add_cog(Command(client))