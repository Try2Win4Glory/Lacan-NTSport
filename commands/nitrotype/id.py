'''User Id and stuff'''

from discord.ext import commands
from packages.utils import Embed, ImproperType
from packages.nitrotype import Racer
import requests, json, os
from mongoclient import DBClient
class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def id(self, ctx, user=None):
        #data = json.loads(requests.get('https://test-db.nitrotypers.repl.co', data={'key': os.getenv('DB_KEY')}).text)
        dbclient = DBClient()
        collection = dbclient.db.NT_to_discord
        data = await dbclient.get_big_array(collection, 'registered')
        if user == None:
            for elem in data['registered']:
                userid = str(ctx.author.id)
                if str(ctx.author.id) == elem['userID']:
                    if elem['verified'] == 'true':
                        racer = await Racer(elem['NTuser'])
                        break
                    else:
                        embed = Embed('Error!', 'You\'re not verified yet!', 'warning')
                        await embed.send(ctx)
                        return
            else:
                embed = Embed('Error!', 'Couldn\'t find that user', 'warning')
                await embed.send(ctx)
                return
        if user != None:
            racer = await Racer(user)
        if racer.success:
            for elem in data['registered']:
                if elem['NTuser'] == user:
                    userid = elem['userID']
                    break
        if not racer.success:
            userid = str(''.join(list(user)[3:-1]))
            for elem in data['registered']:
                if userid == elem['userID']:
                    if elem['verified'] == 'true':
                        racer = await Racer(elem['NTuser'])
                        break
                    else:
                        embed = Embed('Error!', 'You\'re not verified yet!', 'warning')
                        await embed.send(ctx)
                        break
                if str(''.join(list(user)[2:-1])) == elem['userID']:
                    if elem['verified'] == 'true':
                        racer = await Racer(elem['NTuser'])
                        break
                    else:
                        embed = Embed('Error!', 'You\'re not verified yet!', 'warning')
                        await embed.send(ctx)
                        break
            else:
                userid = str(user)
                for elem in data['registered']:
                    if str(user) == elem['userID']:
                        if elem['verified'] == 'true':
                            racer = await Racer(elem['NTuser'])
                            break
                        else:
                            embed = Embed('Error!', 'You\'re not verified yet!', 'warning')
                            await embed.send(ctx)
                            break
                else:
                    embed = Embed('Error!', 'Couldn\'t find that user', 'warning')
                    await embed.send(ctx)
                    return
        embed = Embed('Identification', f'<@'+userid+'>\'s NT Profile [:link:](https://www.nitrotype.com/racer/'+racer.username+')')

        embed.field('Nitrotype username ', '`'+racer.username+'`', inline=True)
        embed.field('Nitrotype Display name', '`'+racer.name+'`', inline=True)
        embed.field('Nitrotype ID', '`'+str(racer.userid)+'`', inline=True)
        try:
            embed.field('Discord ID', '`'+userid+'`', inline=True)
            embed.field('Discord Mention', '<@'+userid+'>', inline=True)
        except:
            pass
        await embed.send(ctx)
def setup(client):
    client.add_cog(Command(client))