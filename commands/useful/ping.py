'''Gives the latency between the client and the websocket'''

from discord.ext import commands
from packages.utils import Embed, ImproperType

class Command(commands.Cog):

    def __init__(self, client):
        self.client= client
    
    @commands.command()
    async def ping(self, ctx):
        #return await ctx.send('This command is currently under maintenance. The developers will try to get it up again as soon as possible. In the meantime feel free to use `n.help` to get the other commands. Thank you for your understanding!')
        if await ImproperType.check(ctx): return
        await Embed('Pong!', f'{ctx.author.mention}\'s latency is **{round(self.client.latency*1000, 5)}** ms!', 'wrench').send(ctx)
    
def setup(client):
    client.add_cog(Command(client))