'''Compile a nitrotype users garage'''

from discord.ext import commands
from packages.utils import Embed, ImproperType
from garageScript.garageScript import compileGarage
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
        await compileGarage(username)
        await ctx.send(file=discord.File("garage.png"))
        return await ctx.send('Having troubles loading your cars? Do you have too many Minnie the coopers? Please do **NOT** message developers just to say that, this is a common problem, caused by NitroType staff, not this bot\'s developers.')
    
def setup(client):
    client.add_cog(Command(client))