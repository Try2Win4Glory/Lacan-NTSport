from discord import Embed as DefaultEmbed
from discord import ChannelType
import random
import time
from datetime import datetime
class Embed:
    def __init__ (self, title, content, emoji=None, color=0xff6347, timestamp=None):
        self.content = content
        self.footer_exist = False
        if not emoji:
            self.emoji = ''
        else:
            self.emoji = f':{emoji.replace(" ", "_")}:  '

        self.embed = DefaultEmbed(
        color = color,
        title = self.emoji + title,
        description = content,
        timestamp = timestamp or datetime.now()
        )

    async def send(self, ctx, dm=False):
        if self.footer_exist == False:
          if ctx.author.id:
            pfp = ctx.author.avatar_url
            self.footer(self.content, pfp)

            list_of_footers = [
              'Become a premium 💠 member today!', 'Created by adl212, Joshua, Try2Win4Glory', 'https://discord.gg/Wj96Ehg for support', 'Officially the biggest Nitrotype Bot']
            random_footer = random.choice(list_of_footers)
            self.embed.set_footer(icon_url=pfp, text=str(ctx.author)+' • '+random_footer)
          else:
            pfp='https://images-ext-1.discordapp.net/external/kTCQEW4t9lrrrjOSzuvR57sawc-ErICSo3wpT37klVE/https/media.discordapp.net/attachments/719414661686099993/765490220858081280/output-onlinepngtools_32.png'
            self.embed.set_footer(icon_url=pfp, text='Discord user '+str(ctx.author.name + '#' + ctx.author.discriminator)+' is a developer of this bot.')
        if dm == True:
            return await ctx.author.send(embed=self.embed, content=None)
        self.sent = await ctx.send(embed=self.embed, content=None)
    async def edit(self, title, content, emoji = None):
      if not emoji:
          emoji = self.emoji
      else:
          self.emoji = f':{emoji.replace(" ", "_")}:  '
          
      new_embed = DefaultEmbed(
        color = 0xFF6347,
        title = self.emoji + title,
        description = content
        )
      await self.sent.edit(embed=new_embed, content=None)
    
    def footer(self, content, pic=None):
        if pic in ["https://media.discordapp.net/attachments/719414661686099993/765110312482766919/NT_Server_Halloween_Logo_2020_GIF.gif", "https://cdn.discordapp.com/attachments/719414661686099993/754971786231283712/season-callout-badge.png"]:
            return
        if pic == 'https://media.discordapp.net/attachments/719414661686099993/765490220858081280/output-onlinepngtools_32.png':
            self.embed.set_footer(icon_url=pic, text='It is a very dumb developer')
        if not pic:
            self.embed.set_footer(text=content)
        else:
            self.embed.set_footer(icon_url=pic, text=content)
        self.footer_exist = True
    
    def image(self, url):
        self.embed.set_image(url=url)
    
    def default_embed(self):
        return self.embed
    
    def thumbnail(self, url):
        self.embed.set_thumbnail(url=url)
    
    def field(self, name, value, inline=True):
        self.embed.add_field(name=name, value=value, inline=inline)

class ImproperType:
    async def check(ctx):

          #if ctx.channel.type is ChannelType.private:
            #embed= Embed('Error!', 'You can\'t use commands in DMs! You can invite the bot to a server through this [invite link](https://discord.com/api/oauth2/authorize?client_id=713352863153258556&permissions=8&redirect_uri=https%3A%2F%2Fnitrotype.com&scope=bot)', 'warning')
            #await embed.send(ctx)
            #return True
            #embed=Embed('Error!', 'Please invite me to your server in order to use my full version!')
            #await embed.send(ctx)
            #pass
            #return True
        return
def get_role(roles, name=None):
    for role in roles:
        if name == role.name:
            return role
    else:
        return
