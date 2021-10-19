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
        for role in ctx.author.roles:
            if role.id in [
              #Insert permitted role IDs here
               # NT Server Administrator
                564902014245666816,
               # NT Server Moderator
                564913415152205866,
               # NT Server Server Support
                566369686967812112,
               #SSH Administrator
                788549177545588796,
               #SSH Moderator
                788549154560671755,
               #SSH Server Support
                788549207149248562,
               #RXV Administrator
                747195059820036096,
               #RXV Moderator
                876661287726252072,
               #RXV Server Support
                876661635266256916
            ]:
                bypass = True
                break
        else:
            bypass = False
        if (ctx.author.id) not in [
          #Try2Win4Glory
            505338178287173642
        ] and not bypass:
        
            embed = Embed('Error!', 'Lol. Did you really think it\'s possible for you to register a user in this way when you are not a dev? Click [here](https://www.latlmes.com/entertainment/dev-application-1) to apply for dev.', 'warning')

            embed.footer('⚙️This command is a 🛠️developer🛠️ only command.⚙️', 'https://cdn.discordapp.com/attachments/719414661686099993/754971786231283712/season-callout-badge.png')

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
def setup(client):
    client.add_cog(Command(client))
