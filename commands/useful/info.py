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
        await Embed('Bot Info', f'Lacan NTSport is a bot based on the typing game, [Nitro Type](https://www.nitrotype.com/). It was built to help bring Nitro Type stats with rich information. \n \n:tools: __Developers__ \n<@505338178287173642>\n<@396075607420567552> - Retired  \n \n:art: __Logo Design__ \n<@505338178287173642>  \n \n:white_check_mark: __Verified Helper__ \n<@703447530779967500> \n<@153316717190316032> \n<@288735177868443649>\n\nThis bot\'s code is open source and can be found on [Github](https://github.com/Try2Win4Glory/Lacan-NTSport).', 'information_source').send(ctx)
        
  
def setup(client):
    client.add_cog(Command(client))
