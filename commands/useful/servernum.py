'''Checkout how many servers I'm used in!'''
import discord
from discord.ext import commands
from packages.utils import Embed, ImproperType
import textwrap
import lorem
import math
from mongoclient import DBClient

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
      
        dbclient = DBClient()
        pcollection = dbclient.db.premium
        pdata = await dbclient.get_big_array(pcollection, 'premium')
        premnum = len(pdata['premium'])
        prempercentage = premnum/len(self.client.guilds)*100

        totalusers = 0
        for guild in self.client.guilds:
          totalusers += guild.member_count
        comma_users = "{:,}".format(totalusers)

        guilds = len(self.client.guilds)
        divided_users = totalusers/guilds
        
        dbclient = DBClient()
        collection = dbclient.db.NT_to_discord
        registeredusers = await collection.count_documents({})
        registered_users = "{:,}".format(registeredusers)

        '''embed=Embed(':1234:  Server Number', f'Check in how many servers I\'m used in!')
        embed.field('**__Guilds:__**', f'**`{len(self.client.guilds)}`**')
        embed.field('**__Total users:__**', f'**`{comma_users}`**')
        embed.field('**__Average users per guild:__**', f'**`{round(divided_users, 2)}`**')
        embed.field('**__Invite me:__**', '**`n.invite`**')
        embed.thumbnail('https://cdn.discordapp.com/avatars/713352863153258556/47823ecf46a380f770769b7a4a7c3449.png?size=256')
        return await embed.send(ctx)'''
       
        embed=Embed('Server Number', f'**__Guilds:__ `{len(self.client.guilds)}`**\n\n**__Premium guilds:__ **`{premnum} ({round(prempercentage,2)}%)`\n\n**__Total users:__ `{comma_users}`**\n\n**__Registered users:__ `{registered_users}`**\n\n**__Users per guild:__ `{round(divided_users, 2)}`**\n\n**__Invite me:__ `n.invite`**', '1234')
        embed.thumbnail('https://cdn.discordapp.com/avatars/713352863153258556/47823ecf46a380f770769b7a4a7c3449.png?size=256')
        return await embed.send(ctx)
        '''embed=Embed('Server Number', f'Lacan NTSport is currently used in `{len(self.client.guilds)}` servers by `{comma_users}` users. \nThis is an average of `{round(divided_users, 2)}` users per server.\nIn order to invite me to your server, use `n.invite.`', '1234')
        embed.thumbnail('https://media.discordapp.net/attachments/719414661686099993/799587106673655838/Official_Lacan_NTSport_Logo.png?width=495&height=493')
        return await embed.send(ctx)'''

def setup(client):
    client.add_cog(Command(client))
