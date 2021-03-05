'''Equip A Car'''

from discord.ext import commands
from packages.utils import Embed, ImproperType
from mongoclient import DBClient
class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def equip(self, ctx, index):
        if index == None:
            embed = Embed('Error!', 'Please choose which car you want to equip by index! Your first car will have the index 1.')
            return await embed.send(ctx)
        dbclient = DBClient()
        collection = dbclient.db.pointsdb
        dbdata = await dbclient.get_array(collection, {'$and': [{'userid': str(ctx.author.id)}, {'userid': str(ctx.author.id)}]})
        async for d in dbdata:
            user = d
            break
        old = user.copy()
        try:
            user['equipped'] = user['cars'][int(index)-1]
        except:
            embed = Embed('Error!', f"Can't equip the car with index {index}!")
            return await embed.send(ctx)
        await dbclient.update_array(collection, old, user)
        embed = Embed('Success!', f"You have equipped {user['cars'][int(index)-1]['car']}")
        return await embed.send(ctx)


def setup(client):
    client.add_cog(Command(client))