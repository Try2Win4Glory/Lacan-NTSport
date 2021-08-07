'''Check Your Lacans!'''

from discord.ext import commands
from packages.utils import Embed, ImproperType
import json, requests, os
from mongoclient import DBClient
import random, discord
from discord.utils import get
class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def bal(self, ctx, userid=None):
        #return await ctx.send('This command is currently under maintenance. The developers will try to get it up again as soon as possible. In the meantime feel free to use `n.help` to get the other commands. Thank you for your understanding!')
        #data = json.loads(requests.get('https://pointsdb.nitrotypers.repl.co', data={'key': os.getenv('DB_KEY')}).text)['data']
        list_of_lacans = ['<:lacan_economy_1:801006407536607262>','<:lacan_economy_2:801004873612132382>','<:lacan_economy_3:801004873214722079>','<:lacan_economy_4:801004868126113822>','<:lacan_economy_5:801004868348936203>','<:lacan_economy_6:801004863433605160>','<:lacan_economy_7:801004870643220481>','<:lacan_economy_8:801004872820457483>','<:lacan_economy_9:801004872417804298>','<:lacan_economy_10:801004872811413514>']
        random_lacan = random.choice(list_of_lacans)
        channels = self.client.get_all_channels()
        channel = get(channels, id=803938544175284244)
        green =0x40AC7B
        red = 0xE84444
        orange = 0xF09F19

        dbclient = DBClient()
        collection = dbclient.db.pointsdb
        if userid == None:
            data = await dbclient.get_array(collection, {'$and': [{'userid': str(ctx.author.id)}, {'userid': str(ctx.author.id)}]})
        else:
            data = await dbclient.get_array(collection, {'$and': [{'userid': userid}, {'userid': userid}]})
        async for d in data:
            data = d
            break
        try:
            if userid == ctx.author.id:
                embed = Embed('Balance', f'You have **{data["points"]}** {random_lacan}.', 'moneybag')
            else:
                embed = Embed('Balance', f'<@{userid}> has **{data["points"]}** {random_lacan}.', 'moneybag')
        except:
            userid = ''.join(list(userid)[2:-1])
            data = await dbclient.get_array(collection, {'$and': [{'userid': userid}, {'userid': userid}]})
            async for d in data:
                data = d
                break
            try:
                if userid == ctx.author.id
                    embed = Embed('Balance', f'You have **{data["points"]}** {random_lacan}.', 'moneybag')
                else:
                    embed = Embed('Balance', f'<@{userid}> has **{data["points"]}** {random_lacan}.', 'moneybag')
            except:
                userid = ''.join(list(userid)[1:])
                data = await dbclient.get_array(collection, {'$and': [{'userid': userid}, {'userid': userid}]})
                async for d in data:
                    data = d
                    break
                try:
                    if userid == ctx.author.id:
                        embed = Embed('Balance', f'You have **{data["points"]}** {random_lacan}.', 'moneybag')
                    else:
                        embed = Embed('Balance', f'<@{userid}> has **{data["points"]}** {random_lacan}.', 'moneybag')
                except:
                    if userid == ctx.author.id:
                        embed = Embed('Error!', f'You don\'t have any {random_lacan}!', 'warning')
                    else:
                        embed = Embed('Error!', f'<@{userid}> doesn\'t have any {random_lacan}!', 'warning')
        return await embed.send(ctx)
def setup(client):
    client.add_cog(Command(client))
