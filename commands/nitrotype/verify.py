'''Verify your account ownership after registering!'''
from discord.ext import commands
from packages.utils import Embed, ImproperType
from packages.nitrotype import Racer, cars
import requests
import os
import json
import random
from mongoclient import DBClient
from nitrotype import verify
import aiohttp
class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    async def fetch(self, session, url, method='POST', data=None):
        if method == 'POST':
            async with session.post(url) as response:
                return await response.text()
        if method == 'GET':
            async with session.get(url) as response:
                return await response.text()
    @commands.command()
    async def verify(self, ctx, type="car"):
        #return await ctx.send('This command is currently under maintenance. The developers will try to get it up again as soon as possible. In the meantime feel free to use `n.help` to get the other commands. Thank you for your understanding!')
        if type == 'car':
            return await verify(ctx)
        if type == 'race':
            dbclient = DBClient()
            collection = dbclient.db.NT_to_discord
            dbdata = await dbclient.get_big_array(collection, 'registered')
            for elem in dbdata['registered']:
                if elem['userID'] == str(ctx.author.id):
                    if elem['verified'] == 'false':
                        embed = Embed('Please Join This Race!', 'Join This Race To Verify This Account Is Yours')
                        embed.field('Instructions', 'Once you join this race, the race leader will leave and you just have to type `n.verify` again to verify. If this does not work, please try doing the verification again.')
                        embed.field('Link', '[:link:](https://www.nitrotype.com/race/lacanverification)')
                        await embed.send(ctx)
                        elem['verifyCar'] = None
                        elem['verified'] = 'in progress'
                        dbclient = DBClient()
                        collection = dbclient.db.NT_to_discord
                        await dbclient.update_big_array(collection, 'registered', dbdata)
                        async with aiohttp.ClientSession() as s:
                            await self.fetch(s,'https://nebuliteforgold-2.adl212.repl.co')
                        break
                    if elem['verified'] == 'in progress':
                        async with aiohttp.ClientSession() as s:
                            response = await self.fetch(s,'https://nebuliteforgold-2.adl212.repl.co', method='GET')

                        data = json.loads(response)
                        if elem['NTuser'] in data['verified']:
                            elem['verified'] = 'true'
                            dbclient = DBClient()
                            await dbclient.update_big_array(collection, 'registered', dbdata)
                            embed = Embed('<a:Check:797009550003666955>  Success', 'You\'ve been verified! In case this is a premium 💠 server do `n.update` to update your roles.')
                            await embed.send(ctx)
                            break
                        else:
                            embed = Embed('Error!', 'Oops it does not seem like you are verified!')
                            embed.field('Instructions', 'Please try to do `n.verify` again and join the race!')
                            await embed.send(ctx)
                            async with aiohttp.ClientSession() as s:
                                await self.fetch(s,'https://nebuliteforgold-2.adl212.repl.co')
                            break
                    if elem['verified'] == 'true':
                        embed = Embed('bru', 'You are already verified :rofl:')
                        return await embed.send(ctx)
            else:
                embed = Embed('bru', 'You have not registered yet. Do `n.register <username>`')
                await embed.send(ctx)
def setup(client):
    client.add_cog(Command(client))
