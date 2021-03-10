'''Compile a nitrotype users garage'''

from discord.ext import commands
from packages.utils import Embed, ImproperType
from packages import garageScript
from math import ceil, floor
from PIL import Image
from io import BytesIO
import numpy
import json
import asyncio
import discord
import requests, os
from mongoclient import DBClient
from packages.nitrotype import Racer
class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    async def compileGarage(self, username):
        profile = await garageScript.compileProfileAsync(username)

        width = 913 + 24
        height = 30 + (ceil(len(profile['garage']) / 30) * 291)
        with Image.new('RGBA', (width, height)) as img:

            # Pasting lots
            with Image.open('packages/parking_spots_all.png') as lots:
                for i in range(ceil(len(profile['garage']) / 30)):
                    img.paste(lots, (12, 15 + (291 * i)), lots)
            garage = numpy.reshape(profile['garage'],
                                (ceil(len(profile['garage']) / 15), 15))
            for y, row in enumerate(garage):
                for x, id in enumerate(row):

                    # Skipping blanks
                    if not id:
                        continue

                        # Looking for garage car in cars
                    id = int(id)
                    car_details = [
                        c for c in profile['cars']
                        if c[0] == id and c[1] == 'owned'
                    ]
                    if not car_details:
                        continue
                    car_details = car_details[0]
                    car = await garageScript.compileCarAsync(
                        id, car_details[2], 'small')
                    with Image.open(car) as c:
                        width = c.size[1]
                        length = c.size[0]
                        with c.rotate(90 if y % 2 == 0 else -90,
                                    expand=True,
                                    resample=Image.NEAREST) as temp:
                            _x = 12 + ((x * 61) + (30 - floor(width / 2)))
                            _y = 20 + (48 -
                                    floor(length / 2)) + (y * 181 -
                                                            (floor(y / 2) * 71))
                            img.paste(temp, (_x, _y))

                    car.close()

            with BytesIO() as b:
                img.save("garage.png", 'PNG')
                b.seek(0)
    @commands.command()
    async def garage(self, ctx, user=None):
        #data = json.loads(requests.get('https://test-db.nitrotypers.repl.co', data={'key': os.getenv('DB_KEY')}).text)
        dbclient = DBClient()
        collection = dbclient.db.NT_to_discord
        data = await dbclient.get_big_array(collection, 'registered')
        if user == None:
            for elem in data['registered']:
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
        username = racer.username
        await self.compileGarage(username)
        await ctx.send(file=discord.File("garage.png"))
        return await ctx.send('Having troubles loading your cars? Do you have too many Minnie the coopers? Please do **NOT** message developers just to say that, this is a common problem, caused by NitroType staff, not this bot\'s developers.')
    
def setup(client):
    client.add_cog(Command(client))