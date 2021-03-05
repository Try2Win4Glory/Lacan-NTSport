'''Report a bug in the bot'''

from discord.ext import commands
from packages.utils import Embed, ImproperType
from datetime import date
from time import time
from discord.utils import get
import discord

class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    #async def bug(self, ctx, *args):
    async def message(self,ctx, *sendmessage):
        #return await ctx.send('This command is currently under maintenance. The developers will try to get it up again as soon as possible. In the meantime feel free to use `n.help` to get the other commands. Thank you for your understanding!')
        if await ImproperType.check(ctx): return
        author = ctx.author.name + '#' + ctx.author.discriminator
        message = ''
        for word in sendmessage:
            message += f' {word}'

        if len(message[1:]) < 40:
            await Embed('Error!', 'Your Message is too short', 'warning').send(ctx)
        else:
            #client = commands.Bot(command_prefix=commands.when_mentioned_or(*['n.', 'N.']), case_insensitive=True)
            client = self.client
            channel = discord.utils.get(client.get_all_channels(), id=809723132083568681)
                #user = self.client.get_user(user_id)
                #embed = Embed(f'Bug by {author}', message, 'wrench')
            
            embed1 = discord.Embed(title=':newspaper:  Message Log', description=str(ctx.author), color=0xFF6347)
            embed1.add_field(name='Author ID', value=f'`{str(ctx.message.author.id)}`')
            embed1.add_field(name='User mention', value=f'{ctx.author.mention}')
            embed1.add_field(name='Message', value=f'```{message}```')
            #embed1.footer(f"{date.fromtimestamp(round(time())).strftime('%d %B %Y')} UTC")
            await channel.send(embed=embed1)
            embed=Embed('Message sent!', f'Thank you! The developers of this bot have received your message:\n\n```{message}```\n\n*Please note that in case of abusing this feature this will have consequences following (e.g. a ban from the bot).*', 'wrench')
            await embed.send(ctx)
            
            #embed=Embed(f'New message!', f'Reported by {author}.\n\nMessage: {message}')
            #await Embed('Message sent!', 'Thank you!', 'wrench').send(ctx)

def setup(client):
    client.add_cog(Command(client))