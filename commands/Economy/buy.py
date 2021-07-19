'''Buy A Car'''

from discord.ext import commands
from packages.utils import Embed, ImproperType
from mongoclient import DBClient
import json, requests
from copy import deepcopy
class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def buy(self, ctx, item=None):
        if item == None:
            embed = Embed('Error!', 'Please choose to either buy the daily or weekly car! Ex: `n.buy daily`')
            return await embed.send(ctx)
        dbclient = DBClient()
        collection = dbclient.db.pointsdb
        dbdata = await dbclient.get_array(collection, {'$and': [{'userid': str(ctx.author.id)}, {'userid': str(ctx.author.id)}]})
        async for d in dbdata:
            user = d
            break
        old = deepcopy(user)
        scollection = dbclient.db.shop
        data = {"data": "", "weekly": ""}
        async for x in scollection.find({}):
            if x['type'] == 'weekly':
                data['weekly'] = x
            if x['type'] == 'daily':
                data['daily'] = x
        if item == 'daily':
            data = data['daily']
            if user['points'] < int(data['price']):
                embed = Embed('Error!', 'You don\'t have enough lacans!')
                return await embed.send(ctx)
            try:
                if data in user['cars']:
                    embed = Embed('Error!', "You've already bought the daily car!")
                    return await embed.send(ctx)
                user['cars'].append(data)
            except KeyError:
                user['cars'] = [data]
                user['equipped'] = data
            user['points'] -= int(data['price'])
            await dbclient.update_array(collection, old, user)
            embed = Embed('Success!', f"You've bought the {data['car']}")
            return await embed.send(ctx)
        elif item == 'weekly':
            data = data['weekly']
            if user['points'] < int(data['price']):
                embed = Embed('Error!', 'You don\'t have enough lacans!')
                return await embed.send(ctx)
            try:
                if data in user['cars']:
                    embed = Embed('Error!', "You've already bought the weekly car!")
                    return await embed.send(ctx)
                user['cars'].append(data)
            except KeyError:
                user['cars'] = [data]
                user['equipped'] = data
            user['points'] -= int(data['price'])
            await dbclient.update_array(collection, old, user)
            embed = Embed('Success!', f"You've bought the {data['car']}")
            return await embed.send(ctx)

def setup(client):
    client.add_cog(Command(client))
