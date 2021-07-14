'''Display common Errors'''
from discord.ext import commands
import discord
from packages.utils import Embed, ImproperType

class Command(commands.Cog):

    def __init__(self, client):
        self.client= client
    
    @commands.command()
    async def errors(self, ctx):
        #return await ctx.send('This command is currently under maintenance. The developers will try to get it up again as soon as possible. In the meantime feel free to use `n.help` to get the other commands. Thank you for your understanding!')

        embed=Embed('<a:error:800338727645216779>  __**List of common errors:**__', '```Command raised an exception: AttributeError: \'NoneType\' object has no attribute \'group\'```\nThis mean\'s I can\'t find your NitroType user you\'re looking for. Make sure to use the correct username and not the display name.\n\n```\'NoneType\' object has no attribute \'invoke\'```\nIn case you just received this error, you discovered an unregocnized command. Run `n.help` for a full list of commands.\n\n```Command raised an exception: UnboundLocalError: local variable \'user\' referenced before assignment```\nLooks like you aren\'t in our data base yet. In case I display this error to you, try running `n.guess` and answering correct one time.\n\nAny other errors with the commands, please report using `n.message <message>` and specify what you did and what the bot replied and.')
        return await embed.send(ctx)

def setup(client):
    client.add_cog(Command(client))
