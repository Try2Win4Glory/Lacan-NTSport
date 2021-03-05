'''Get info about this bot.'''

from discord.ext import commands
from packages.utils import Embed, ImproperType

class Command(commands.Cog):

    def __init__(self, client):
        self.client= client
    
    @commands.command()
    async def vote(self, ctx):
        #return await ctx.send('This command is currently under maintenance. The developers will try to get it up again as soon as possible. In the meantime feel free to use `n.help` to get the other commands. Thank you for your understanding!')
        if await ImproperType.check(ctx): return
        await Embed('Vote', f'Vote for Lacan NTSport on top.gg [here](https://top.gg/bot/713352863153258556/vote)').send(ctx)

def setup(client):
    client.add_cog(Command(client))