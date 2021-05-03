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
from nitrotype import get_username
class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    @commands.command()
    async def garage(self, ctx, user=None):
        #data = json.loads(requests.get('https://test-db.nitrotypers.repl.co', data={'key': os.getenv('DB_KEY')}).text)
        if user == None:
            success, result = await get_username(str(ctx.author.id), True)
            if success:
                racer = result
            else:
                racer = Racer('nothiswillnotbesuccesffulbecauseitistoolong')
        if user != None:
            racer = await Racer(user)
        if not racer.success:
            userid = str(''.join(list(user)[3:-1]))
            success, result = await get_username(str(userid), True)
            if success:
                racer = result
            else:
                userid = str(''.join(list(user)[2:-1]))
                success, result = await get_username(str(userid), True)
                if success:
                    racer = result
                else:
                    success, result = await get_username(user, True)
                    if success:
                        racer = result
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