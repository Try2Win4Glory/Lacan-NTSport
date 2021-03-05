'''Dev only say command'''
import discord
from discord.ext import commands
from discord.utils import get
class Command(commands.Cog):
  def __init__(self, client):
      self.client = client
    #return await ctx.send('This command is currently under maintenance. The developers will try to get it up again as soon as possible. In the meantime feel free to use `n.help` to get the other commands. Thank you for your understanding!')
  @commands.command(none='say', pass_context=True, aliases=['announce'])
  async def say(self,ctx, channel, *msg):
    if ctx.author.id in [505338178287173642, 396075607420567552, 637638904513691658]:
      if channel == 'no':
        await ctx.send(' '.join(msg))
        await ctx.message.delete()
      else:
          channel = get(self.client.get_all_channels(), id=int(channel))
          await channel.send(' '.join(msg))
    else:
      await ctx.message.delete()
      await ctx.send(f'Lol '+str(ctx.author.name + '#' + ctx.author.discriminator)+'! \nRip! This command is dev only by default as some people might abuse it. :warning:<@'+str(ctx.author.id)+'> was about to say: \n\n`'+(msg)+'` \n\nhttps://media.tenor.com/images/a5d46f7b746bf96c8a70b7f5a788e201/tenor.gif')
  
def setup(client):
    client.add_cog(Command(client))