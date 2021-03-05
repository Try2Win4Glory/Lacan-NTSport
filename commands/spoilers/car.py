'''description'''

from discord.ext import commands
from packages.utils import Embed, ImproperType
import requests, re, json
class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def car(self, ctx, id):
        text = requests.get('https://www.nitrotype.com/index/d8dad03537419610ef21782a075dde2d94c465c61266-1266/bootstrap.js').text
        result = re.search(r'\[\{\"id\"\:\d+,\"carID\":\d+,\"name\":\".{10,35}\",\"options\":\{.{20,80}\}.{1,100}\}.*\]', text).group()
        data = json.loads('{"list": '+''.join(list(result)[:-1])+'}')
        for elem in data['list']:
            for v in elem.values():
                try:
                    if re.search(str(id).lower(), str(v)).group().lower():
                        cardata = elem
                        break
                except:
                    continue
            else:
                continue
            break
        else:
            embed = Embed('Car Image', 'Search Query: '+str(id))
            embed.field('Results', 'None')
            return await embed.send(ctx)
        embed = Embed('Car Image', 'Search Query: '+str(id))
        embed.image('https://www.nitrotype.com/cars/'+cardata['options']['largeSrc'])
        return await embed.send(ctx)
    
def setup(client):
    client.add_cog(Command(client))