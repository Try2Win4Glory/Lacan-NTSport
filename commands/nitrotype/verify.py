'''Verify your account ownership after registering!'''
from discord.ext import commands
from packages.utils import Embed, ImproperType
from packages.nitrotype import Racer, cars
import requests
import os
import json
import random
from mongoclient import DBClient
class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def verify(self, ctx):
        #return await ctx.send('This command is currently under maintenance. The developers will try to get it up again as soon as possible. In the meantime feel free to use `n.help` to get the other commands. Thank you for your understanding!')
        dbkey = os.getenv('DB_KEY')
        #dbdata = json.loads(requests.get('https://test-db.nitrotypers.repl.co', data={"key": dbkey}).text)
        dbclient = DBClient()
        collection = dbclient.db.NT_to_discord
        dbdata = await dbclient.get_big_array(collection, 'registered')
        for elem in dbdata['registered']:
            if elem['userID'] == str(ctx.author.id):
                racer = await Racer(elem['NTuser'])
                if elem['verified'] == 'false':
                    if len(racer.carIDs) > 1:
                        while True:
                            verifycar = cars[random.choice(racer.carIDs)]
                            if verifycar == racer.current_car:
                                continue
                            else:
                                break
                        embed = Embed('Instructions', 'Go to your [Garage](https://nitrotype.com/garage), switch your car to **__' + verifycar + '__** and type `n.verify` again. \n\n *(Please note that this could take up to 15 minutes to work.)*', 'clipboard')
                        

                        await embed.send(ctx)
                        elem['verifyCar'] = verifycar
                        elem['verified'] = 'in progress'
                        #requests.post('https://test-db.nitrotypers.repl.co', data={"key": dbkey, "data": json.dumps(dbdata)})
                        dbclient = DBClient()
                        collection = dbclient.db.NT_to_discord
                        await dbclient.update_big_array(collection, 'registered', dbdata)
                        break
                    if len(racer.carIDs) <= 1:
                        embed = Embed('Error', 'Get another car before trying to verifying!', 'warning')
                if elem['verified'] == 'in progress':
                    if elem['verifyCar'] == racer.current_car:
                        elem['verified'] = 'true'
                        #requests.post('https://test-db.nitrotypers.repl.co', data={"key": dbkey, "data": json.dumps(dbdata)})
                        dbclient = DBClient()
                        collection = dbclient.db.NT_to_discord
                        await dbclient.update_big_array(collection, 'registered', dbdata)
                        embed = Embed('<a:Check:797009550003666955>  Success', 'You\'ve been verified! In case this is a premium 💠 server do `n.update` to update your roles.')
                        await embed.send(ctx)
                        break
                    else:
                        embed = Embed('<a:error:800338727645216779>  Oh No!', f'Remember to switch your car to **__{elem["verifyCar"]}__**. \nIf there is a problem, just wait a few minutes before trying again. \n\n***(If you just registered, make sure to wait 15 minutes so that I can recognize your equipped car.)*** \n\nIf any problems occur, please make sure to ping / DM **one** of the following people who are able to register you: \n\n**__Developers:__** \n<@505338178287173642> \n<@637638904513691658> \n<@396075607420567552> \n\n**__Helpers:__**\n<@630761745140547625>\n<@731041476322263050> \n<@527937153817116704>')
                        await embed.send(ctx)
                        break
                if elem['verified'] == 'true':
                    embed = Embed('LOL', 'You already registered and verified silly!\nIn case this is a premium 💠 server do `n.update` to update your roles.', 'rofl')

                    if (ctx.author.id) not in [505338178287173642, 637638904513691658, 396075607420567552]:
                      embed.footer('Make sure to use n.verify after waiting 15 minutes!\n Become a premium 💠 member today! Run n.premium for more info.', 'https://media.discordapp.net/attachments/719414661686099993/765110312482766919/NT_Server_Halloween_Logo_2020_GIF.gif')
                    else: 
                      embed.footer('Discord user '+str(ctx.author.name + '#' + ctx.author.discriminator)+' is a developer of this bot.', 'https://media.discordapp.net/attachments/719414661686099993/765490220858081280/output-onlinepngtools_32.png')

                    await embed.send(ctx)
                    break
        #if the for loop doesn't "break"
        else:
            embed = Embed('<a:error:800338727645216779>  Error!', 'Your account isn\'t registered yet.\nAlready registered? Make sure to run `n.verify` to verify your ownership!')
            await embed.send(ctx)
            return
def setup(client):
    client.add_cog(Command(client))