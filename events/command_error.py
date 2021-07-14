from discord.ext import commands
from packages.utils import Embed
class Events(commands.Cog):
    def __init__(self, client):
        self.client = client
    @commands.Cog.listener('on_command_error')
    async def event(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            embed = Embed(
                'Error!',
                '**Unrecognized command!**\nFor a full list of commands, make sure to use `n.help`.',
                'warning',
                color=0xff0000)
            await embed.send(ctx)
        #await ctx.send('Error!')
        #pass
        else:
            if error!=None:
              try:
                raise (error)
              except:
                pass
def setup(client):
    client.add_cog(Events(client))
