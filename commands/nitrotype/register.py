'''Link your NT account to your discord!'''
from discord.ext import commands
from packages.utils import Embed, ImproperType
from packages.nitrotype import Racer
import requests
import os
import json
import discord
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
          try:
            racer = await Racer(user)
          except AttributeError:
            embed = Embed('Error!', 'Couldn\'t find that user. Make sure to use `n.register <username>`.', 'warning')
            await embed.send(ctx)
            return
        if not racer.success:
            embed = Embed('Error!', 'Couldn\'t find that user. Make sure to use `n.register <username>`.', 'warning')
            await embed.send(ctx)
            return
        #dbdata = json.loads(requests.get('https://test-db.nitrotypers.repl.co', data={"key": dbkey}).text)
        dbclient = DBClient()
        collection = dbclient.db.NT_to_discord
        dbdata = await dbclient.get_array(collection, {})
        async for x in dbdata:
            if str(ctx.author.id) == x['userID']:
                embed = Embed('Error!', 'You\'ve already registered!\nRun `n.verify` to check if you already verified your identity and in case this is a premium :diamond_shape_with_a_dot_inside: server and you are already verified, run `n.update` to update your roles.', 'warning')
                await embed.send(ctx)
                return
            if user == x['NTuser']:
                        embed = Embed('Error!', 'Someone is already registered to this account!\nFor more information on who is registered to **'+x['NTuser']+'**, run `n.id '+x['NTuser']+'`.', 'warning')
                        await embed.send(ctx)
                        return
        else:
            await dbclient.create_doc(collection, {"userID": str(ctx.author.id), "NTuser": racer.username.lower(), "verified": "false"})
            #if json.loads(requests.post('https://test-db.nitrotypers.repl.co', data={"key": dbkey, "data": json.dumps(dbdata)}).text)['success'] == 'true':
        dbclient = DBClient()
        collection = dbclient.db.NT_to_discord
        #await dbclient.update_big_array(collection, 'registered', dbdata)
        embed = Embed('<a:Check:797009550003666955>  Success!', 'You are now registered to `' + racer.username.lower() + '`. Type `n.verify` to verify your ownership!')
        await embed.send(ctx)
        try:
            channel1 = discord.utils.get(self.client.get_all_channels(), id=803938544175284244)
            embed = Embed(':regional_indicator_r:  Register', f'<@{str(ctx.author.id)}> registered.', color=0x00ff00)
            embed.field('ID', f'`{str(ctx.author.id)}`')
            embed.field('Linked Account', f'`{user}`')
            embed.field('Link', f'[:link:](https://nitrotype.com/racer/{user})')
            embed.field('Author', f'{str(ctx.author.name)}#{str(ctx.author.discriminator)}')
            embed.field('Guild', f'`{str(ctx.guild.name)}`')
            msg1 = await channel1.send(embed=embed.default_embed())
        except:
            print('Couldn\'t log register.')
def setup(client):
    client.add_cog(Command(client))
