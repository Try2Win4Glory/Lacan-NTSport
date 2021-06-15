from discord.ext import commands
from packages.utils import Embed
from mongoclient import DBClient
import copy
class Events(commands.Cog):
    def __init__(self, client):
        self.client = client
    @commands.Cog.listener('on_raw_reaction_remove')
    async def event(self, payload):
        dbclient = DBClient()
        collection = dbclient.db.giveaways
        dbdata = await dbclient.get_array(collection, {'$and': [{'messageID': payload.message_id}, {'messageID': payload.message_id}]})
        async for d in dbdata:
            user = d
            break
        try:
            old = copy.deepcopy(user)
            user['joined'].remove(payload.user_id)
        except:
            return
        await dbclient.update_array(collection, old, user)
def setup(client):
    client.add_cog(Events(client))