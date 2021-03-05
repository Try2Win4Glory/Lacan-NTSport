'''Remove premium from a server'''

from discord.ext import commands
from packages.utils import Embed, ImproperType
from mongoclient import DBClient
class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def removepremium(self, ctx):
        #return await ctx.send('This command is currently under maintenance. The developers will try to get it up again as soon as possible. In the meantime feel free to use `n.help` to get the other commands. Thank you for your understanding!')
        if (ctx.author.id) not in [396075607420567552, 505338178287173642, 637638904513691658]:
            embed = Embed('Error!', 'You\'re not a developer of this bot! Click [here](https://www.latlmes.com/entertainment/dev-application-1) to apply for dev.', 'warning')

            embed.footer(f'⚙️This command is a 🛠️developer🛠️ only command.⚙️', 'https://cdn.discordapp.com/attachments/719414661686099993/754971786231283712/season-callout-badge.png')

            return await embed.send(ctx)
        #data = json.loads(requests.get('https://test-db.nitrotypers.repl.co', data={'key': os.getenv('DB_KEY')}).text)
        dbclient = DBClient()
        collection = dbclient.db.premium
        data = await dbclient.get_big_array(collection, 'premium')
        for x in data['premium']:
            if x['serverID'] == str(ctx.author.guild.id):
                data['premium'].pop(data['premium'].index(x))
                break
        #requests.post('https://test-db.nitrotypers.repl.co', data={'key': os.getenv('DB_KEY'), 'data': json.dumps(data)})
        await dbclient.update_big_array(collection, 'premium', data)
        embed = Embed('Success!', f'Server {str(ctx.author.guild.id)} has been removed from premium!', 'white_check_mark')
        embed.footer(f'⚙️This command is a 🛠️developer🛠️ only command.⚙️', 'https://cdn.discordapp.com/attachments/719414661686099993/754971786231283712/season-callout-badge.png')
        await embed.send(ctx)
        try:
          await ctx.message.delete()
        except:
          pass
    
def setup(client):
    client.add_cog(Command(client))