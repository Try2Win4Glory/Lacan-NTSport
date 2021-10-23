'''Verify your account ownership after registering!'''
from discord.ext import commands
from packages.utils import Embed, ImproperType
from packages.nitrotype import Racer, cars
import requests
import discord
import os
import json
import random, copy
from mongoclient import DBClient
from nitrotype import verify, verify_race, verify_friend, verify_link
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
    async def verify(self, ctx, type="switch"):
        #return await ctx.send('This command is currently under maintenance. The developers will try to get it up again as soon as possible. In the meantime feel free to use `n.help` to get the other commands. Thank you for your understanding!')
        if type == 'car':
            return await verify(ctx)
        if type == 'race':
            return await verify_race(ctx)
        if type == 'friend':
            return await verify_friend(ctx)
        else:          
            # Get Collection            
            dbclient = DBClient()
            collection = dbclient.db.NT_to_discord
            dbdata = await collection.find_one({"userID":str(ctx.author.id)})
            print(dbdata)
            old = copy.deepcopy(dbdata)

            if dbdata == 'None':
                embed = Embed('Error!', 'You have not registered yet. Make sure to run `n.register <username>`', 'warning')
                return await embed.send(ctx)

            # Check whether the User is verified
            if dbdata['verified'] == 'false':
                # Get the User's Nitrotype Username
                racer = await Racer(dbdata['NTuser'])
                # Check current Title
                if racer.title != 'Raw Racing Recruit':
                    changeto_type = 'title'
                    changeto = 'Raw Racing Recruit'
                # Gold members are able to use Solid Gold instead
                elif racer.title == 'Raw Racing Recruit' and racer.membership == 'gold':
                    changeto_type = 'title'
                    changeto = 'Solid Gold'
                # Non Gold Members have to change their trail randomely
                else:
                    changeto_type = 'trail'
                    basic_traillist = ['Bits', 'Puff', 'Shock', 'Lovely', 'Dust']
                    if racer.trailname in basic_traillist:
                        basic_traillist.remove(racer.trailname)
                    changeto = random.choice(basic_traillist)
                # Verification Instructions
                embed = Embed(':clipboard:  Verify your Identity!', f'In order to verify, your ownership of **{dbdata["NTuser"]}**, login to [Nitrotype](https://www.nitrotype.com/login) and change your __{changeto_type}__ to **{changeto}**. \nAfter that, run `n.verify` again.\n\n**Attention:** Sometimes, Nitrotype might not work right away, so please be friendly enough to give me some time to recognize your changes (max. ~5 minutes) after you changed your {changeto_type}.')
                await embed.send(ctx)
                #try:
                channel1 = discord.utils.get(self.client.get_all_channels(), id=803938544175284244)
                embed = Embed(':x:  Verify', f'Verification process started by {str(ctx.author.mention)}.', color=0x00ff00)
                embed.field('ID', f'`{str(ctx.author.id)}`')
                embed.field('Linked Account', f'`{dbdata["NTuser"]}`')
                embed.field('Link', f'[:link:](https://nitrotype.com/racer/{dbdata["NTuser"]})')
                embed.field('Author', f'{str(ctx.author.name)}#{str(ctx.author.discriminator)}')
                embed.field('Guild', f'`{str(ctx.guild.name)}`')
                embed.field('Verification Type', f'`{changeto_type}`')
                embed.field('Verification Change', f'`{changeto}`')
                msg1 = await channel1.send(embed=embed.default_embed())
                #except:
                    #print('Couldn\'t log verification start.')
                # Set Database Elements
                dbdata['verifyCar'] = None
                dbdata['verified'] = 'in progress'
                dbdata['ChangeToType'] = changeto_type
                dbdata['ChangeTo'] = changeto
                # Update Database
                await dbclient.update_array(collection, old, dbdata)
                # Return
                return

            # The User already run the command before
            elif dbdata['verified'] == 'in progress':
                racer = await Racer(dbdata['NTuser'])
                # Check if the User followed the instructions
                if dbdata['ChangeToType'] == 'title':
                    if dbdata['ChangeTo'] == racer.title:
                        # User is verified
                        dbdata['verified'] = 'true'
                        embed=Embed('<a:Check:797009550003666955>  Success', 'You\'ve been verified! In case this is a premium 💠 server run `n.update` to update your roles.')
                        await embed.send(ctx)
                        try:
                            channel1 = discord.utils.get(self.client.get_all_channels(), id=803938544175284244)
                            embed = Embed(':white_check_mark:  Verify', f'Verification attempt by {str(ctx.author.mention)} suceeded.', color=0x00ff00)
                            embed.field('ID', f'`{str(ctx.author.id)}`')
                            embed.field('Linked Account', f'`{dbdata["NTuser"]}`')
                            embed.field('Link', f'[:link:](https://nitrotype.com/racer/{dbdata["NTuser"]})')
                            embed.field('Author', f'{str(ctx.author.name)}#{str(ctx.author.discriminator)}')
                            embed.field('Guild', f'`{str(ctx.guild.name)}`')
                            embed.field('Verification Type', f'`{dbdata["ChangeToType"]}`')
                            embed.field('Verification Change', f'`{dbdata["ChangeTo"]}`')
                            msg1 = await channel1.send(embed=embed.default_embed())
                        except:
                            print('Couldn\'t log verification success.')
                        # Update Database
                        await dbclient.update_array(collection, old, dbdata)
                        # Return
                        return
                    # User did not follow the instructions
                    else:
                        # Failed to recognize the title change
                        embed=Embed('Error!', f'Nitrotype User **{dbdata["NTuser"]}** did not change their __{dbdata["ChangeToType"]}__ to \n\n*"{dbdata["ChangeTo"]}"*\n\n yet.\n\n**Attention:** Sometimes, Nitrotype might not work right away, so please be friendly enough to give me some time to recognize your changes (max. ~5 minutes) after you changed your {dbdata["ChangeToType"]}.', 'warning')
                        await embed.send(ctx)
                        try:
                            channel1 = discord.utils.get(self.client.get_all_channels(), id=803938544175284244)
                            embed = Embed(':x:  Verify', f'Verification attempt by {str(ctx.author.mention)} failed.', color=0xffaa00)
                            embed.field('ID', f'`{str(ctx.author.id)}`')
                            embed.field('Linked Account', f'`{dbdata["NTuser"]}`')
                            embed.field('Link', f'[:link:](https://nitrotype.com/racer/{dbdata["NTuser"]})')
                            embed.field('Author', f'{str(ctx.author.name)}#{str(ctx.author.discriminator)}')
                            embed.field('Guild', f'`{str(ctx.guild.name)}`')
                            embed.field('Verification Type', f'`{dbdata["ChangeToType"]}`')
                            embed.field('Verification Change', f'`{dbdata["ChangeTo"]}`')
                            msg1 = await channel1.send(embed=embed.default_embed())
                        except:
                            print('Couldn\'t log verification fail.')
                        return
                # User has to change their trail
                elif dbdata['ChangeToType'] == 'trail':
                    # Check if the User followed the instructions
                    if dbdata['ChangeTo'] == racer.trailname:
                        # User is verified
                        dbdata['verified'] = 'true'
                        embed=Embed('<a:Check:797009550003666955>  Success', 'You\'ve been verified! In case this is a premium 💠 server run `n.update` to update your roles.')
                        await embed.send(ctx)
                        try:
                            channel1 = discord.utils.get(self.client.get_all_channels(), id=803938544175284244)
                            embed = Embed(':white_check_mark:  Verify', f'Verification attempt by {str(ctx.author.mention)} suceeded.', color=0x00ff00)
                            embed.field('ID', f'`{str(ctx.author.id)}`')
                            embed.field('Linked Account', f'`{dbdata["NTuser"]}`')
                            embed.field('Link', f'[:link:](https://nitrotype.com/racer/{dbdata["NTuser"]})')
                            embed.field('Author', f'{str(ctx.author.name)}#{str(ctx.author.discriminator)}')
                            embed.field('Guild', f'`{str(ctx.guild.name)}`')
                            embed.field('Verification Type', f'`{dbdata["ChangeToType"]}`')
                            embed.field('Verification Change', f'`{dbdata["ChangeTo"]}`')
                            msg1 = await channel1.send(embed=embed.default_embed())
                        except:
                            print('Couldn\'t log verification success.')
                        # Update Database
                        await dbclient.update_array(collection, old, dbdata)
                        # Return
                        return
                    else:
                        # Failed to recognize the trail change
                        embed=Embed('Error!', f'Nitrotype User **{dbdata["NTuser"]}** did not change their __{dbdata["ChangeToType"]}__ to \n\n*"{dbdata["ChangeTo"]}"*\n\n yet.\n\n**Attention:** Sometimes, Nitrotype might not work right away, so please be friendly enough to give me some time to recognize your changes (max. ~5 minutes) after you changed your {dbdata["ChangeToType"]}.', 'warning')
                        await embed.send(ctx)
                        try:
                            channel1 = discord.utils.get(self.client.get_all_channels(), id=803938544175284244)
                            embed = Embed(':x:  Verify', f'Verification attempt by {str(ctx.author.mention)} failed.', color=0xffaa00)
                            embed.field('ID', f'`{str(ctx.author.id)}`')
                            embed.field('Linked Account', f'`{dbdata["NTuser"]}`')
                            embed.field('Link', f'[:link:](https://nitrotype.com/racer/{dbdata["NTuser"]})')
                            embed.field('Author', f'{str(ctx.author.name)}#{str(ctx.author.discriminator)}')
                            embed.field('Guild', f'`{str(ctx.guild.name)}`')
                            embed.field('Verification Type', f'`{dbdata["ChangeToType"]}`')
                            embed.field('Verification Change', f'`{dbdata["ChangeTo"]}`')
                            msg1 = await channel1.send(embed=embed.default_embed())
                        except:
                            print('Couldn\'t log verification fail.')
                        return
            # The User is already verified
            else:
                embed=Embed('Error!', f'You are already verified to **{dbdata["NTuser"]}**. In case this is a Premium 💠 server, please run `n.update`.', 'joy')
                return await embed.send(ctx)

def setup(client):
            client.add_cog(Command(client))
