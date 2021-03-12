'''Reroll The Winner!'''

from discord.ext import commands
from packages.utils import Embed, ImproperType
from mongoclient import DBClient
from discord.utils import get
import random
class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def reroll(self, ctx, messageID: int):
        dbclient = DBClient()
        collection = dbclient.db.giveaways
        dbdata = await dbclient.get_array(collection, {"$and": [{"messageID": messageID}, {"messageID": messageID}]})
        async for d in dbdata:
            giveaway = d
            break
        try:
            giveaway['ended']
        except:
            embed = Embed('Error!', f'No giveaway found with message ID `{messageID}`', 'warning')
            return await embed.send(ctx)
        if giveaway['ended'] == False:
            embed = Embed('Error!', 'This giveaway hasn\'t ended! Try `n.end` to end the giveaway!', 'warning')
            return await embed.send(ctx)
        channel = get(self.client.get_all_channels(), id=giveaway['channelID'])
        msg = get(await channel.history(limit=1000).flatten(), id=giveaway['messageID'])
        try:
            winner = random.choice(giveaway['joined'])
            if giveaway['joined'] == []:
                await msg.channel.send(f':weary:No one won\n{msg.jump_url}:weary:')
            else:
                await msg.channel.send(f':tada:The new winner is <@{winner}> {msg.jump_url}!:tada:')
                
        except KeyError:
            await msg.channel.send(f'No one won because no one joined!\n{msg.jump_url}')

def setup(client):
    client.add_cog(Command(client))