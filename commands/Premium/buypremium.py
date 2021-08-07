'''Buy Premium For The Server!'''
#810296381779476510 is the channel id
from discord.ext import commands
from packages.utils import Embed, ImproperType
from mongoclient import DBClient
import discord
class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def buypremium(self, ctx):
        dbclient = DBClient()
        collection = dbclient.db.premium
        data = await dbclient.get_big_array(collection, 'premium')
        for x in data['premium']:
            if x['serverID'] == str(ctx.author.guild.id):
                embed = Embed('Error!', 'This server is already premium :diamond_shape_with_a_dot_inside:!', 'warning')
                return await embed.send(ctx)
        else:
            del collection
            del data
        collection = dbclient.db.pointsdb
        data = await dbclient.get_array(collection, {'$and': [{'userid': str(ctx.author.id)}, {'userid': str(ctx.author.id)}]})
        async for d in data:
            data = d
            old = data.copy()
            break
        try:
            points = data['points']
        except:
            embed = Embed('Error!', 'The user doesn\'t have any lacans!')
            return await embed.send(ctx)
        data['points'] = int(points) - 3000
        if data['points'] < 0:
            embed = Embed('Error!', 'You do not have 3000 lacans!', 'rofl')
            return await embed.send(ctx)
        await dbclient.update_array(collection, old, data)
        embed = Embed('Success!', 'You have bought premium :diamond_shape_with_a_dot_inside: for this server, pending dev verification. \n\n*Please wait for a developer to accept your server for premium. If you get rejected, your lacans will be refunded.*', 'white check mark')
        await embed.send(ctx)
        channel = discord.utils.get(self.client.get_all_channels(), id=810296381779476510)
        embed = Embed('Someone Wants Premium!', 'Click :ballot_box_with_check: to accept or :x: to deny.')
        embed.field('Guild ID', f'{str(ctx.guild.id)}')
        embed.field('Guild Name', f'{str(ctx.guild)}')
        embed.field('Buyer ID', f'{str(ctx.author.id)}')
        embed.field('Buyer Name', str(ctx.author))
        msg = await channel.send(embed=embed.default_embed())
        await msg.add_reaction('☑️')
        await msg.add_reaction('❌')

    
def setup(client):
    client.add_cog(Command(client))
