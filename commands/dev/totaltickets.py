'''Shows the total tickets'''

from discord.ext import commands
from packages.utils import Embed, ImproperType
import json
import math
class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def totaltickets(self, ctx):
        if ctx.author.id not in [505338178287173642, 724772394748870718]:
            embed = Embed('Error!', 'You are not a dev!', 'warning')
            #if (ctx.author.id) not in [505338178287173642, 637638904513691658, 396075607420567552]:
                #embed.footer('⚙️This command is a 🛠️developer🛠️ only command.⚙️ \nBecome a premium 💠 member today!','https://media.discordapp.net/attachments/719414661686099993/765110312482766919/NT_Server_Halloween_Logo_2020_GIF.gif')
            #else: 
                #embed.footer('⚙️This command is a 🛠️developer🛠️ only command.⚙️\n Discord user '+str(ctx.author.name + '#' + ctx.author.discriminator)+' is a 🛠️developer🛠️ of this bot.', 'https://media.discordapp.net/attachments/719414661686099993/765490220858081280/output-onlinepngtools_32.png')
            return await embed.send(ctx)
        with open('tickets.json') as f:
            data = json.load(f)
        tickets = data['tickets']
        dict = {i:tickets.count(i) for i in tickets}
        payload = ''
        total = 0
        for k, v in dict.items():
            payload += f'<@{k}> has `{str(v)}` tickets.\n'
            total += v*100000
        payload += f'\nTotal :money_with_wings: sent to raffle: `{str(total)}`'
        #await ctx.send(payload)
        embed=Embed('Totaltickets', f'{payload}', 'tickets')
        await embed.send(ctx)

    
def setup(client):
    client.add_cog(Command(client))
