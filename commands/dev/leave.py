'''Leave a server'''

from discord.ext import commands
from packages.utils import Embed, ImproperType
from discord.utils import get

class Command(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def leave(self, ctx, guildid):
        #return await ctx.send('This command is currently under maintenance. The developers will try to get it up again as soon as possible. In the meantime feel free to use `n.help` to get the other commands. Thank you for your understanding!')
        if ctx.author.id not in [505338178287173642, 637638904513691658, 396075607420567552]:
            return await ctx.send('bru, not dev guy')
        guild = get(self.client.guilds, id=int(guildid))
        if guild is None:
            await ctx.send("I don't recognize that guild.")
            return
        await guild.leave()
        embed=Embed('Success!', f'I successfully left guild `{guildid}`.')
        await embed.send(ctx)
def setup(client):
    client.add_cog(Command(client))