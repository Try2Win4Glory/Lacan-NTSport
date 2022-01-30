'''Devs manual register'''

from discord.ext import commands
from packages.utils import Embed, ImproperType
import discord
import requests
import json
import os
from mongoclient import DBClient
from packages.nitrotype import Racer

class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def devregister(self, ctx, discordid, ntuser):
        #return await ctx.send('This command is currently under maintenance. The developers will try to get it up again as soon as possible. In the meantime feel free to use `n.help` to get the other commands. Thank you for your understanding!')
        racer = await Racer(ntuser)
        if not racer.success:
            embed = Embed('Error!', 'Nitrotype user not found! Make sure to use `n.devregister <Mention / ID> <username>.', 'warning')
            return await embed.send(ctx)

        dbclient = DBClient()
        permcollection = dbclient.client.dev.devregister
        serversearch = ctx.guild.id
        x = await permcollection.find_one({"serverID":str(serversearch)})
        dev = await permcollection.find_one({"bypass":"dev"})
        bypass = False
        if dev != None:
          if str(ctx.author.id) in str(dev["dev"]):
            permittedserver = True
            devbypass = True
          else:
            permittedserver = False
            devbypass = False
        else:
          permittedserver = False
          devbypass = False

      # Server Devregister  Not Supported
        if x == None and devbypass == False:
          permittedserver = False
          embed = Embed('Error!', 'This server does not have permission to use this command. Click [here](https://www.latlmes.com/entertainment/permission-application-1) to apply for permission.', 'warning')
          return await embed.send(ctx)
      # Server Devregister Supported
        elif x != None or devbypass == True:
          permittedserver = True

      # Author Permitted Check
        if permittedserver == True and devbypass != True:
            for role in ctx.author.roles:
              if str(role.id) in str(x['permitted']):
                bypass = True
                break
              else:
                bypass = False

        if bypass == False and devbypass == True:
          bypass = True

        if bypass == False:
          embed = Embed('Error!', 'Lol. Did you really think it\'s possible for you to register another user when you are not a dev? Click [here](https://www.latlmes.com/entertainment/dev-application-1) to apply for dev.', 'warning')
          return await embed.send(ctx)
        else:
            discordid = discordid.replace("!", "")
            discordid0 = discordid.replace("<@", "")
            discordid1 = discordid0.replace(">", "")
            print(discordid1)
            #data = json.loads(requests.get('https://test-db.nitrotypers.repl.co', data={"key": os.getenv('DB_KEY')}).text)
            dbclient = DBClient()
            collection = dbclient.db.NT_to_discord
            await dbclient.create_doc(collection, {
                "NTuser": ntuser,
                "userID": str(discordid1),
                "verified": "true"
            })
            #requests.post('https://test-db.nitrotypers.repl.co', data={"key": os.getenv('DB_KEY'), "data": json.dumps(data)})
            embed = Embed('Success!', f'<@{str(ctx.author.id)}> just connected discord user <@'+discordid1+'> with NT username `' + ntuser + '`! \nIn case this is a premium :diamond_shape_with_a_dot_inside: server, <@'+discordid1+'> needs to run `n.update` to update their roles.', 'white_check_mark')
            
            if (ctx.author.id) in [396075607420567552, 505338178287173642, 637638904513691658]:
              embed.footer('Discord user '+str(ctx.author.name + '#' + ctx.author.discriminator)+' is a 🛠️developer🛠️ of this bot. \n⚙️This command is a 🛠️developer🛠️ and verified helper only command.⚙️', 'https://media.discordapp.net/attachments/719414661686099993/765490220858081280/output-onlinepngtools_32.png')
            else:
              embed.footer('Discord user '+str(ctx.author.name + '#' + ctx.author.discriminator)+' is a verified helper of this bot. \n⚙️This command is a 🛠️developer🛠️ and ✅ verified helper only command.⚙️', 'https://cdn.discordapp.com/attachments/765547632072196116/781838805044166676/output-onlinepngtools6.png')
            await embed.send(ctx)
            try:
              await ctx.message.delete()
            except:
              pass
            try:
                channel1 = discord.utils.get(self.client.get_all_channels(), id=803938544175284244)
                dontlog = [505338178287173642]
                if ctx.author.id not in dontlog:
                    channel2 = discord.utils.get(self.client.get_all_channels(), id=901503736013262888)
                    channel3 = discord.utils.get(self.client.get_all_channels(), id=924334305570852916)
                embed = Embed('<:dev:901381277477900358>  Devregister', f'<@{str(discordid1)}> was devregistered by {str(ctx.author.mention)}.', color=0x00ff00)
                embed.field('ID', f'`{discordid1}`')
                embed.field('Linked Account', f'`{ntuser}`')
                embed.field('Link', f'[:link:](https://nitrotype.com/racer/{ntuser})')
                embed.field('Registered by', f'{str(ctx.author.name)}#{str(ctx.author.discriminator)}')
                embed.field('Author', f'`{str(ctx.author.id)}`')
                embed.field('Guild', f'`{str(ctx.guild.name)}`')
                msg1 = await channel1.send(embed=embed.default_embed())
                if ctx.author.id not in dontlog:
                    msg2 = await channel2.send(embed=embed.default_embed())
                    msg3 = await channel3.send(embed=embed.default_embed())
            except:
                print('Couldn\'t log devregister.')
def setup(client):
    client.add_cog(Command(client))
