'''Link your NT account to your discord!'''
from discord.ext import commands
from packages.utils import Embed, ImproperType
from packages.nitrotype import Racer
import requests
import os
import json
from mongoclient import DBClient
class Command(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def register(self, ctx, user=None):
        #return await ctx.send('This command is currently under maintenance. The developers will try to get it up again as soon as possible. In the meantime feel free to use `n.help` to get the other commands. Thank you for your understanding!')
        if user == None:
            embed = Embed('Error!', 'How are you supposed to register without a nitrotype account? Make sure to add your username by sending `n.register <username>` without the `<>`.', 'warning')
            #if (ctx.author.id) not in [505338178287173642, 637638904513691658, 396075607420567552]:

              #embed.footer('Make sure to use n.register <username>!\nBecome a premium 💠 member today! Run n.premium for more info.', 'https://media.discordapp.net/attachments/719414661686099993/765110312482766919/NT_Server_Halloween_Logo_2020_GIF.gif')
            #else: 
              #embed.footer('Discord user '+str(ctx.author.name + '#' + ctx.author.discriminator)+' is a developer of this bot.', 'https://media.discordapp.net/attachments/719414661686099993/765490220858081280/output-onlinepngtools_32.png')
            return await embed.send(ctx)
        if ''.join(list(user)[0:32]) == 'https://www.nitrotype.com/racer/':
            racer = await Racer(''.join(list(user)[32:]))
        else:
            racer = await Racer(user)
        if not racer.success:
            embed = Embed('Error!', 'Couldn\'t find that user. Make sure to use `n.register <username>`.', 'warning')
            await embed.send(ctx)
            return
        #dbdata = json.loads(requests.get('https://test-db.nitrotypers.repl.co', data={"key": dbkey}).text)
        dbclient = DBClient()
        collection = dbclient.db.NT_to_discord
        dbdata = await dbclient.get_big_array(collection, 'registered')
        for x in dbdata['registered']:
            if str(ctx.author.id) == x['userID']:
                embed = Embed('Error!', 'You\'ve already registered!\nIn case this is a premium :diamond_shape_with_a_dot_inside: server, run `n.update` to update your roles.', 'warning')
                await embed.send(ctx)
                return
            if user == x['NTuser']:
                embed = Embed('Error!', 'Someone is already registered to this account!', 'warning')
                await embed.send(ctx)
                return
        else:
            dbdata['registered'].append({"userID": str(ctx.author.id), "NTuser": racer.username.lower(), "verified": "false"})
            #if json.loads(requests.post('https://test-db.nitrotypers.repl.co', data={"key": dbkey, "data": json.dumps(dbdata)}).text)['success'] == 'true':
        dbclient = DBClient()
        collection = dbclient.db.NT_to_discord
        await dbclient.update_big_array(collection, 'registered', dbdata)
        embed = Embed('Success!', 'You are now registered to `' + racer.username.lower() + '`. Type `n.verify` to verify your ownership!', 'white_check_mark')
        await embed.send(ctx)
def setup(client):
    client.add_cog(Command(client))