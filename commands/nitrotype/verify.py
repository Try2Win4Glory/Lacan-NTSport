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
    async def verify(self, ctx, type="None"):
        #return await ctx.send('This command is currently under maintenance. The developers will try to get it up again as soon as possible. In the meantime feel free to use `n.help` to get the other commands. Thank you for your understanding!')
        if type == 'car':
            return await verify(ctx)
        if type == 'race':
            return await verify_race(ctx)
        if type == 'friend':
            return await verify_friend(ctx)
        if type == 'link':
            return await verify_link(ctx)
        else:
            

            # Get Collection            
            dbclient = DBClient()
            collection = dbclient.db.NT_to_discord
            dbdata = await collection.find_one({"userID":str(ctx.author.id)})

            # User is not registered yet
            if dbdata == None:
              embed = Embed('Error!', 'You have not registered yet. Make sure to run `n.register <username>`', 'warning')
              return await embed.send(ctx)
            # Recognized the User
            async for elem in dbdata:
              old = copy.deepcopy(elem)
              # Check whether the User is verified
              if elem['verified'] == 'false':
                # Get the User's Nitrotype Username
                racer = await Racer(elem['NTuser'])
                # Check current Title
                if racer.title != 'Raw Racing Recruit':
                  changeto_type = 'title'
                  changeto = 'Raw Racing Recruit'
                # Gold members are able to use Solid Gold instead
                elif racer.title == 'Raw Racing Recruit' and racer.membership == 'gold':
                  changeto_type = 'title'
                  changeto = 'Solid Gold'
                # Non Gold Members have to change their trail ranodmely
                else:
                  changeto_type = 'trail'
                  basic_traillist = ['Bits', 'Puff', 'Shock', 'Lovely', 'Dust']
                  if racer.trailname in basic_traillist:
                    basic_traillist.remove(racer.trailname)
                  changeto = random.choice(basic_traillist)
                # Verification Instructions
                embed = Embed(':clipboard:  Verify your Identity!', f'In order to verify, your ownership of **{elem["NTuser"]}**, login to [Nitrotype](https://www.nitrotype.com/login) and change your __{changeto_type}__ to **{changeto}**. \nAfter that, run `n.verify` again.\n\n**Attention:** Please be friendly enough to give me some time to recognize your changes (max. ~5 minutes) after you changed your {changeto_type}.')
                # Set Database Elements
                elem['verifyCar'] = None
                elem['verified'] = 'in progress'
                elem['ChangeToType'] = changeto_type
                elem['ChangeTo'] = changeto
                # Update Database
                await dbclient.update_array(collection, old, elem)
                # Send the Embed
                await embed.send(ctx)
                # Break the for loop
                break
              # The User already run the command before
              elif elem['verified'] == 'in progress':
                racer = await Racer(elem['NTuser'])
                # Check if the User followed the instructions
                if elem['ChangeToType'] == 'title':
                  if elem['ChangeTo'] == racer.title:
                    # User is verified
                    elem['verified'] = 'true'
                    embed=Embed('<a:Check:797009550003666955>  Success', 'You\'ve been verified! In case this is a premium 💠 server run `n.update` to update your roles.')
                    # Update Database
                    await dbclient.update_array(collection, old, elem)
                    # Send the Embed
                    await embed.send(ctx)
                    # Break the for loop
                    break
                  # User did not follow the instructions
                  else:
                    # Failed to recognize the title change
                    embed=Embed('Error!', f'Nitrotype User **{elem["NTuser"]}** did not change their {elem["ChangeToType"]}__ to **{elem["ChangeTo"]}** yet.\n\n**Attention:**Please be friendly enough to give me some time to recognize your changes (max. ~5 minutes) after you changed your {elem["ChangeToType"]}.')
                    await embed.send(ctx)
                    # Break the for loop
                    break
                # User has to change their trail
                elif elem['ChangeToType'] == 'trail':
                  # Check if the User followed the instructions
                  if elem['ChangeTo'] == racer.trailname:
                    # User is verified
                    elem['verified'] = 'true'
                    embed=Embed('<a:Check:797009550003666955>  Success', 'You\'ve been verified! In case this is a premium 💠 server run `n.update` to update your roles.')
                    # Update Database
                    await dbclient.update_array(collection, old, elem)
                    # Send the Embed
                    await embed.send(ctx)
                    # Break the for loop
                    break
                  else:
                    # Failed to recognize the trail change
                    embed=Embed('Error!', f'Nitrotype User **{elem["NTuser"]}** did not change their __{elem["ChangeToType"]}__ to **{elem["ChangeTo"]}** yet.\n\n**Attention:**Please be friendly enough to give me some time to recognize your changes (max. ~5 minutes) after you changed your {elem["ChangeToType"]}.')
                    await embed.send(ctx)
                    # Break the for loop
                    break
              # The User is already verified
              else:
                embed=Embed('Error!', 'You are already verified. In case this is a Premium 💠 server, please run `n.update`.', 'joy')
                await embed.send(ctx)
                # Break the for loop
                break
            # If the for loop doesn't break, the User is not registered yet
            else:
              embed = Embed('<a:error:800338727645216779>  Error!', 'You have not registered yet. Make sure to run `n.register <username>`', 'warning')
              await embed.send(ctx)
              return
def setup(client):
    client.add_cog(Command(client))
