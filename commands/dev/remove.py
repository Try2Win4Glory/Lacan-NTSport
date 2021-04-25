'''Remove lacans'''

from discord.ext import commands
from packages.utils import Embed, ImproperType
import json, requests, os
from mongoclient import DBClient
class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def remove(self, ctx, userid, amount):
        #return await ctx.send('This command is currently under maintenance. The developers will try to get it up again as soon as possible. In the meantime feel free to use `n.help` to get the other commands. Thank you for your understanding!')
        if (ctx.author.id) not in [505338178287173642, 637638904513691658, 396075607420567552]:
            embed = Embed('Error!', 'Lol, did you really think it\'s possible for you to add <:Lacan:766669740545540097> to a user when you are not a dev? Click [here](https://www.latlmes.com/entertainment/dev-application-1) to apply for dev.', 'warning')
            embed.footer('⚙️This command is a 🛠️developer🛠️ only command.⚙️', 'https://cdn.discordapp.com/attachments/719414661686099993/754971786231283712/season-callout-badge.png')
            await embed.send(ctx)
            return
        #data = json.loads(requests.get('https://pointsdb.nitrotypers.repl.co', data={'key': os.getenv('DB_KEY')}).text)['data']
        dbclient = DBClient()
        collection = dbclient.db.pointsdb
        data = await dbclient.get_array(collection, {'$and': [{'userid': str(userid)}, {'userid': str(userid)}]})
        async for d in data:
            user = d
            break
        try:
            old = user.copy()
            if user['userid'] == str(userid):
                user['points'] -= int(amount)
                userpoints = user['points']
                data = await dbclient.update_array(collection, old, user)
        except:
            dbclient.create_doc(collection, {'userid': str(userid), 'points': userpoints})
        embed = Embed('Success!', f'<@{ctx.author.id}> just removed **{amount}** <:Lacan:766669740545540097> from <@{userid}>\'s balance. \n<@{userid}> now has **{userpoints}** <:Lacan:766669740545540097>!', 'white_check_mark')
        embed.footer('Discord user '+str(ctx.author.name + '#' + ctx.author.discriminator)+' is a developer of this bot. \n⚙️This command is a 🛠️developer🛠️ only command.⚙️', 'https://media.discordapp.net/attachments/719414661686099993/765490220858081280/output-onlinepngtools_32.png')
        try:
          await ctx.message.delete()
        except:
          pass
        await embed.send(ctx)
def setup(client):
    client.add_cog(Command(client))