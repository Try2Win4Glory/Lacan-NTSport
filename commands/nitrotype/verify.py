'''Verify your account ownership after registering!'''
from discord.ext import commands
from packages.utils import Embed, ImproperType
from packages.nitrotype import Racer, cars
import requests
import os
import json
import random, copy
from mongoclient import DBClient
from nitrotype import verify, verify_race, verify_friend
import aiohttp
import cloudscraper
import asyncio
import functools
import time
try:
    from dotenv import load_dotenv

    load_dotenv()
except:
    pass
class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    async def fetch(self, session, url, method='POST', data=None):
        if method == 'POST':
            async with session.post(url, data=data) as response:
                return await response.text()
        if method == 'GET':
            async with session.get(url) as response:
                return await response.text()
    @commands.command()
    async def verify(self, ctx, type="link"):
        #return await ctx.send('This command is currently under maintenance. The developers will try to get it up again as soon as possible. In the meantime feel free to use `n.help` to get the other commands. Thank you for your understanding!')
        if type == 'car':
            return await verify(ctx)
        if type == 'race':
            return await verify_race(ctx)
        if type == 'friend':
            return await verify_friend(ctx)
        else:
            dbclient = DBClient()
            collection = dbclient.db.NT_to_discord
            dbdata = await collection.find_one({"userID":str(ctx.author.id)})
            if dbdata == None:
                embed = Embed('Error!', 'You have not registered yet. Make sure to run `n.register <username>`', 'warning')
                return await embed.send(ctx)
            old = copy.deepcopy(dbdata)
            if dbdata['verified'] == 'false':
                username = dbdata['NTuser']
                embed = Embed(':clipboard:  Verify your Identity!', f'In order to verify, your ownership of **{dbdata["NTuser"]}**, login to [Nitrotype](https://www.nitrotype.com/login) and go [here](https://lns-verification.herokuapp.com/)! \nAfter that run `n.verify` again.\n\n**Attention:** In case you are currently in Europe :flag_eu:, please either switch to an US :flag_us: VPN or use `n.unregister`, register again and run `n.verify friend` instead.')
                dbdata['verifyCar'] = None
                dbdata['verified'] = 'in progress'
                await dbclient.update_array(collection, old, dbdata)
                return await embed.send(ctx)
            if dbdata['verified'] == 'in progress':
                v_collection = dbclient.db.verified
                data = await v_collection.find_one({'timestamp': {'$gt': time.time()-1000}, 'username': dbdata['NTuser']})
                if data is not None:
                    dbdata['verified'] = 'true'
                    await dbclient.update_array(collection, old, dbdata)
                    embed = Embed('<a:Check:797009550003666955>  Success', 'You\'ve been verified! In case this is a premium 💠 server run `n.update` to update your roles.')
                    return await embed.send(ctx)
                else:
                    embed = Embed(':warning:  Nearly there!', f'Nitro Type user **{dbdata["NTuser"]}** did not visit the link yet. In order to verify your ownership for **{dbdata["NTuser"]}**, login to [Nitrotype](https://www.nitrotype.com/login) and go [here](https://lns-verification.herokuapp.com/). \nAfter that make sure to run `n.verify` again.\n\n**Attention:** In case you are currently in Europe :flag_eu:, please either switch to an US :flag_us: VPN or use `n.unregister`, register again and run `n.verify friend` instead.')
                    return await embed.send(ctx)
            if dbdata['verified'] == 'true':
                embed = Embed('Error!', 'You are already verified :rofl:', 'joy')
                return await embed.send(ctx)
def setup(client):
    client.add_cog(Command(client))
