'''Report a bug in the bot'''

from discord.ext import commands
from packages.utils import Embed, ImproperType
from discord import Message
from datetime import date
from time import time
from discord.utils import get
from cooldowns.message import rateLimit, cooldown_add
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

        bannedmsgecontent = [
        #Blacklisted content:

        #General Blacklisted content / Swearting, etc...:
        "bitch", 
        "fuck",
        "shit", 
        "idiot", 
        "ass", 

        #Blacklisted NT Content / no instructions read:
        "verify", 
        "verification", 
        "poop", 
        "trade", 
        "sell",
        "garage",
        "Minnie the Cooper"
        ]

        for word in bannedmsgecontent:
          if message.count(word) > 0:
            embed = Embed('Ooops!', f'Keep the language clean! Your message\n\n```{message}```\n\ncontains the blacklisted word\n\n```{word}```\n\nIn order to get your message submitted, please remove this word.\n\n*Not an offensive word? Then you probably didn\'t read the instructions carefully. Please read the instructions carefully first, before you submit your support request.*')
            return await embed.send(ctx)
        else:
          pass
        

        if len(message[1:]) < 10:
            await Embed('Error!', 'Your Message is too short. Your message must at least `10` characters.', 'warning').send(ctx)
        else:
              #if await ImproperType.check(ctx): return
              if str(ctx.author) in rateLimit:
                embed = Embed('Cooldown!','You are on cooldown. Wait `1` hour before running this command again.','alarm clock')
                return await embed.send(ctx)
              else:
                #client = commands.Bot(command_prefix=commands.when_mentioned_or(*['n.', 'N.']), case_insensitive=True)
                client = self.client
                channel = discord.utils.get(client.get_all_channels(), id=809723132083568681)
                    #user = self.client.get_user(user_id)
                    #embed = Embed(f'Bug by {author}', message, 'wrench')
                
                embed1 = discord.Embed(title=':newspaper:  Message Log', description=str(ctx.author), color=0xFF6347)
                embed1.add_field(name='Author ID', value=f'`{str(ctx.message.author.id)}`')
                embed1.add_field(name='User mention', value=f'{ctx.author.mention}')

                try:
                    invitelink = await ctx.channel.create_invite(reason='Better support features - instant developer notification, easier to help people. Don\'t want this? Remove my permission to create invites, but then don\'t expect immediate support.')
                    embed1.add_field(name='__Invite__', value=f'{invitelink}')
                except:
                      pass

                embed1.add_field(name='Message', value=f'```{message}```')
                #embed1.footer(f"{date.fromtimestamp(round(time())).strftime('%d %B %Y')} UTC")
                await channel.send(embed=embed1)
                embed=Embed('Message sent!', f'Thank you! The developers of this bot have received your message:\n\n```{message}```\n\n*Please note that in case of abusing this feature this will have consequences following (e.g. a ban from the bot).*', 'wrench')
                await embed.send(ctx)
                if ctx.author.id not in [
          #Try2Win4Glory
            505338178287173642, 
          #Typerious
            637638904513691658, 
          #adl212
            396075607420567552]:
                  cooldown_add(str(ctx.author))
                  print('Cooldown added!')
                
                #embed=Embed(f'New message!', f'Reported by {author}.\n\nMessage: {message}')
                #await Embed('Message sent!', 'Thank you!', 'wrench').send(ctx)

def setup(client):
    client.add_cog(Command(client))