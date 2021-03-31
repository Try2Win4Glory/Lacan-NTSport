
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
    async def verify(self, ctx, type="race"):
        #return await ctx.send('This command is currently under maintenance. The developers will try to get it up again as soon as possible. In the meantime feel free to use `n.help` to get the other commands. Thank you for your understanding!')
        if type == 'car':
            return await verify(ctx)
        if type == 'race':
            #return await ctx.send('**Your** security is important for **us**! Because of security reasons, this command has been taken down and will be back soon. Thanks for your understanding.')
            dbclient = DBClient()
            collection = dbclient.db.NT_to_discord
            dbdata = await dbclient.get_big_array(collection, 'registered')
            for elem in dbdata['registered']:
                if elem['userID'] == str(ctx.author.id):
                    if elem['verified'] == 'false':
                        username = elem['NTuser']
                        embed = Embed(':clipboard:  Verify your Identity!', f'Join the race to verify **{username}** is owned by you. You don\'t own **{username}**? Run `n.unregister` to unlink your discord from this account.')
                        embed.field('__Instructions__', 'Once you join the race, the race leader will leave and you just have to type n.verify again to verify. If this does not work, please try unregistering and registering again.')
                        embed.field('__Short instructions__', '**1.** Run `n.verify`\n**2.** Join the race track shown under the link category.\n**3.** Run `n.verify` again.')
                        embed.field('__Common errors__', 'Is the race leader not joining the race? Refresh your page, after maximal **4** refreshs the race leader joins and you can attempt to verify.')
                        embed.field('__Link__', 'Join [this](https://www.nitrotype.com/race/lacanverification) race to verify your identity.')
                        await embed.send(ctx)
                        elem['verifyCar'] = None
                        elem['verified'] = 'in progress'
                        dbclient = DBClient()
                        collection = dbclient.db.NT_to_discord
                        await dbclient.update_big_array(collection, 'registered', dbdata)
                        async with aiohttp.ClientSession() as s:
                            await self.fetch(s,'https://Lacan-Verification.try2win4code.repl.co')
                        break
                    if elem['verified'] == 'in progress':
                        async with aiohttp.ClientSession() as s:
                            response = await self.fetch(s,'https://Lacan-Verification.try2win4code.repl.co', method='GET')

                        data = json.loads(response)
                        if elem['NTuser'] in data['verified']:
                            elem['verified'] = 'true'
                            dbclient = DBClient()
                            await dbclient.update_big_array(collection, 'registered', dbdata)
                            embed = Embed('<a:Check:797009550003666955>  Success', 'You\'ve been verified! In case this is a premium 💠 server do `n.update` to update your roles.')
                            await embed.send(ctx)
                            break
                        else:
                            username = elem['NTuser']
                            embed = Embed('Nearly there!', f'You\'re nearly done - just one more step to go!\nYou are just about to verify your ownership for **{username}**. Not you? Run `n.unregister` to unlink your discord from this account.', 'warning')
                            embed.field('__Instructions__', 'Please join the race and run `n.verify` again.')
                            embed.field('__Common errors__', 'Is the race leader not joining the race? Refresh your page, after maximal **4** refreshs the race leader joins and you can attempt to verify.')
                            embed.field('__Link__', 'Join [this](https://www.nitrotype.com/race/lacanverification) race to verify your identity.')
                            await embed.send(ctx)
                            async with aiohttp.ClientSession() as s:
                                await self.fetch(s,'https://Lacan-Verification.try2win4code.repl.co')
                            break
                    if elem['verified'] == 'true':
                        embed = Embed('Error!', 'You are already verified :rofl:', 'joy')
                        return await embed.send(ctx)
            else:
                embed = Embed('Error!', 'You have not registered yet. Make sure to run `n.register <username>`', 'warning')
                await embed.send(ctx)
def setup(client):
    client.add_cog(Command(client))
