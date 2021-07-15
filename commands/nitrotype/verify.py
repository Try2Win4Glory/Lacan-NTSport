'''Verify your account ownership after registering!'''
from discord.ext import commands
from packages.utils import Embed, ImproperType
from packages.nitrotype import Racer, cars
import requests
import os
import json
import random, copy
from mongoclient import DBClient
from nitrotype import verify, verify_race
import aiohttp
import cloudscraper
import asyncio
import functools
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
    async def verify(self, ctx, type="friend"):
        #return await ctx.send('This command is currently under maintenance. The developers will try to get it up again as soon as possible. In the meantime feel free to use `n.help` to get the other commands. Thank you for your understanding!')
        if type == 'car':
            return await verify(ctx)
        if type == 'race':
            return await verify_race(ctx)
        if type == 'friend':
            dbclient = DBClient()
            collection = dbclient.db.NT_to_discord
            dbdata = await dbclient.get_array(collection, {})
            async for elem in dbdata:
                old = copy.deepcopy(elem)
                if elem['userID'] == str(ctx.author.id):
                    if elem['verified'] == 'false':
                        username = elem['NTuser']
                        embed = Embed(':clipboard:  Verify your Identity!', f'In order to verify, your ownership of **{elem["NTuser"]}**, friend me on nitrotype [here](https://www.nitrotype.com/racer/lacanverification)! \nAfter that run `n.verify` again.')
                        elem['verifyCar'] = None
                        elem['verified'] = 'in progress'
                        dbclient = DBClient()
                        collection = dbclient.db.NT_to_discord
                        await dbclient.update_array(collection, old, elem)
                        return await embed.send(ctx)
                    if elem['verified'] == 'in progress':
                        session = cloudscraper.create_scraper()
                        loop = asyncio.get_event_loop()
                        
                        # Login with Username and Password
                        #fut = await loop.run_in_executor(None, functools.partial(session.post, 'https://www.nitrotype.com/api/login', data={'username': os.getenv('verification_username'), 'password': os.getenv('verification_password')}))
                        
                        # Login with Cookies
                        session.cookies['ntuserrem'] = os.environ('ntuserrem')
                        session.cookies['PHPNTSESSION'] = "applesandbananas"
                        session.cookies['applesandbananas'] = os.getenv('phpntsessiondata')

                        fut = await loop.run_in_executor(None, functools.partial(session.get, 'https://www.nitrotype.com/api/friend-requests'))
                        friends = json.loads(fut.text)
                        
                        for friend in friends['data']['requests']:
                            if friend['username'] == elem['NTuser']:
                                break
                            #elif friends['data']['requests']==None:
                                #break
                        else:
                            embed = Embed(':warning:  Nearly there!', f'Nitro Type user **{elem["NTuser"]}** did not friend request me yet. In order to verify your ownership for **{elem["NTuser"]}**, click [here](https://www.nitrotype.com/racer/lacanverification) and friend request me. \nAfter that make sure to run `n.verify` again.')
                            return await embed.send(ctx)
                        elem['verified'] = 'true'
                        dbclient = DBClient()
                        await dbclient.update_array(collection, old, elem)
                        embed = Embed('<a:Check:797009550003666955>  Success', 'You\'ve been verified! In case this is a premium 💠 server run `n.update` to update your roles.')
                        return await embed.send(ctx)
                    if elem['verified'] == 'true':
                        embed = Embed('Error!', 'You are already verified :rofl:', 'joy')
                        return await embed.send(ctx)
            else:
                embed = Embed('Error!', 'You have not registered yet. Make sure to run `n.register <username>`', 'warning')
                return await embed.send(ctx)
        
def setup(client):
    client.add_cog(Command(client))

