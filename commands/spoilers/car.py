'''Get car information - use _ as space.'''

from discord.ext import commands
from packages.utils import Embed, ImproperType
import requests, re, json
class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def car(self, ctx, id):
        try:
          id2 = id.replace("_", " ")
          print(id2)
        except:
          print('not replaced')
          pass
        text = requests.get('https://www.nitrotype.com/index/d8dad03537419610ef21782a075dde2d94c465c61266-1266/bootstrap.js').text
        result = re.search(r'\[\{\"id\"\:\d+,\"carID\":\d+.*\]', text).group()
        data = json.loads('{"list": '+''.join(list(result)[:-1])+'}')
        for elem in data['list']:
            for v in elem.values():
                try:
                    if re.search(str(id2).lower(), str(v).lower()).group():
                        cardata = elem
                        break
                except:
                    continue
            else:
                continue
            break
        else:
            embed = Embed(':frame_photo:  Car Image', 'Search Query: `'+str(id2)+'`')
            embed.field('Results', 'None')
            embed.footer('Not the car you\'re looking for? Replace all spaces with _ .')
            return await embed.send(ctx)
        embed = Embed('Car Image', 'Search Query: `'+str(id)+'`')
        embed.image('https://www.nitrotype.com/cars/'+cardata['options']['largeSrc'])
        embed.footer('Not the car you\'re looking for? Replace all spaces with _ .')
        for k, v in cardata.items():
            embed.field(k, v)
        return await embed.send(ctx)
    
def setup(client):
    client.add_cog(Command(client))
