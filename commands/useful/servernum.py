'''Checkout how many servers I'm used in!'''
import discord
from discord.ext import commands
from packages.utils import Embed, ImproperType
import textwrap
import lorem
import math

client = discord.Client

class Command(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Dev only servers command ready!")

    @commands.command()
    async def servernum(self, ctx):
        #activeservers = list (self.client.guilds)
        #return await ctx.send('This command is currently under maintenance. The developers will try to get it up again as soon as possible. In the meantime feel free to use `n.help` to get the other commands. Thank you for your understanding!')
        #if (ctx.author.id) in [505338178287173642, 637638904513691658, 396075607420567552]:
      
        totalusers = 0
        for guild in self.client.guilds:
          totalusers += guild.member_count
        comma_users = "{:,}".format(totalusers)

        guilds = len(self.client.guilds)
        divided_users = totalusers/guilds
       
        embed=Embed('Server Number', f'Lacan NTSport is currently used in `{len(self.client.guilds)}` servers by `{comma_users}` users. \nThis is an average of `{round(divided_users, 2)}` users per server.\nIn order to invite me to your server, use `n.invite.`', '1234')
        embed.thumbnail('https://media.discordapp.net/attachments/719414661686099993/799587106673655838/Official_Lacan_NTSport_Logo.png?width=495&height=493')
        return await embed.send(ctx)
        #else:
            #await ctx.send(f'Lol. That\'s private! We\'re not gonna tell you the servers the bot is in.')

def setup(client):
    client.add_cog(Command(client))