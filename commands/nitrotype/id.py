'''User Id and stuff'''

from discord.ext import commands
from packages.utils import Embed, ImproperType
from packages.nitrotype import Racer
import requests, json, os
from mongoclient import DBClient
from nitrotype import get_username
class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def id(self, ctx, user=None):
        #data = json.loads(requests.get('https://test-db.nitrotypers.repl.co', data={'key': os.getenv('DB_KEY')}).text)
        if user == None:
            success, result = await get_username(str(ctx.author.id))
            if success:
                racer = result
            else:
                embed = result
                await embed.send(ctx)
                return
            if racer.success:
                success, result = await get_username(str(ctx.author.id), get_id=True)
                userid = result
        if user != None:
            racer = await Racer(user)
            success, result = await get_username(racer.username.lower(), get_id=True)
            if racer.success:            
                userid = result
        if not racer.success:
            userid = str(''.join(list(user)[3:-1]))
            success, result = await get_username(str(userid))
            if success:
                racer = result
            else:
                userid = str(''.join(list(user)[2:-1]))
                success, result = await get_username(str(userid))
                if success:
                    racer = result
                else:
                    success, result = await get_username(str(userid))
                    if success:
                        racer = result
                    else:
                        userid = str(user)
                        success, result = await get_username(str(userid))
                        if success:
                            racer = result
                        else:
                            embed = result
                            await embed.send(ctx)
                            return
        try:
            embed = Embed('Identification', f'<@'+userid+'>\'s NT Profile [:link:](https://www.nitrotype.com/racer/'+racer.username+')')
        except:
            embed = Embed('Identification', f'{racer.username}\'s NT Profile [:link:](https://www.nitrotype.com/racer/'+racer.username+')')
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
