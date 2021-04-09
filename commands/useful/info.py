'''Get info about this bot.'''

from discord.ext import commands
from packages.utils import Embed, ImproperType

class Command(commands.Cog):

    def __init__(self, client):
        self.client= client
    
    @commands.command()
    async def info(self, ctx):
        #return await ctx.send('This command is currently under maintenance. The developers will try to get it up again as soon as possible. In the meantime feel free to use `n.help` to get the other commands. Thank you for your understanding!')
        if await ImproperType.check(ctx): return
        await Embed('Bot Info', f'Lacan NTSport is a bot based on the typing game, [Nitro Type](https://www.nitrotype.com/). It was built to help bring Nitro Type stats with rich information. \n \n**Developers** \n<@505338178287173642>  \n <@637638904513691658>   \n<@437984033377484803>  \n<@396075607420567552>  \n \n  **Logo Designer** \n<@505338178287173642>  \n \n ** Verified Helper** \n <@703447530779967500> \n <@666515662931492874>  \n <@153316717190316032> \n <@288735177868443649>\n\n **Garage Compiler**\n<@645415863767531541>\n\nBy using you agree to create a temporary (5 minutes lasting) invite for easier support.', 'information_source').send(ctx)
        
  
def setup(client):
    client.add_cog(Command(client))