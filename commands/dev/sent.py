'''Your Lacans have been sent'''

from discord.ext import commands
from packages.utils import Embed, ImproperType
from mongoclient import DBClient
import discord
class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def sent(self, ctx, sendto: discord.User, amount):
        if (ctx.author.id) not in [505338178287173642]:
            embed = Embed('Error!', 'Lol, did you really think it\'s possible for you to use this command 5540097> when you are not a dev? Click [here](https://www.latlmes.com/entertainment/dev-application-1) to apply for dev.', 'warning')
            embed.footer('⚙️This command is a 🛠️developer🛠️ only command.⚙️', 'https://cdn.discordapp.com/attachments/719414661686099993/754971786231283712/season-callout-badge.png')
            await embed.send(ctx)
            return
        try:
            await sendto.send(f'Developer {ctx.author} just paid out the **{amount}** <:Lacan:766669740545540097> (worth {str(int(amount)*1000)} NT Cash). Check your NT account in order to get the cash.')
            embed = Embed('Success', f'{ctx.author} just paid out the **{amount}** <:Lacan:766669740545540097> (worth {str(int(amount)*1000)} NT Cash).', 'white check mark')
        except Exception:
            embed=Embed('Error!',''+sendto.mention+' has received '+str(ctx.author)+'\'s **''** <:Lacan:766669740545540097>, but they have their DMs turned off so I couldn\'t Direct message '+sendto.mention+'.', 'warning')
        await embed.send(ctx)
        try:
            await ctx.message.delete()
        except:
            pass
        return
        
def setup(client):
    client.add_cog(Command(client))
