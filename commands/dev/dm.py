'''Simple tool to assist users by dming them.'''
from discord.ext import commands
import discord
from packages.utils import Embed, ImproperType

class Command(commands.Cog):

    def __init__(self, client):
        self.client= client
    
    @commands.command()
    async def dm(self, ctx, user: discord.Member = None, *, message = None):
        #return await ctx.send('This command is currently under maintenance. The developers will try to get it up again as soon as possible. In the meantime feel free to use `n.help` to get the other commands. Thank you for your understanding!')
        developers = [505338178287173642]
        if ctx.author.id in developers:
          if user == None:
            return await ctx.send('Please specify a user you\'re sending your message to.')
          else:
            pass
          if message == None:
            return await ctx.send('Please specify a message you want to send.')
          else:
            embed=Embed('New Direct Message', 'speech_left')
            embed.field('Author:', f'Message sent by {ctx.author}')
            embed.field('Message:', f'Following message was sent: {message}')
            return await user.send(embed=Embed)
        else:
            return await ctx.send('You do not have perms, dude.')
    
def setup(client):
    client.add_cog(Command(client))
