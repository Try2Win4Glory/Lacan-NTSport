'''Warn users who behave who don\'t behave themselves'''

'''from discord.ext import commands
from packages.utils import Embed, ImproperType
from packages.nitrotype import Racer
import requests, json, os
import discord
from discord.utils import get
from mongoclient import DBClient
class Command(commands.Cog):

    def __init__(self, client):
        self.client = client

    
        @commands.command()
        async def warn(self, ctx, userid, rulenum, *additional_note):
          #return await ctx.send('This command is currently under maintenance. The developers will try to get it up again as soon as possible. In the meantime feel free to use `n.help` to get the other commands. Thank you for your understanding!')
          if ctx.author.id not in [505338178287173642, 637638904513691658, 396075607420567552]:
            embed=Embed('Error!', 'This commmand is developer only!', 'hammer')
            return await embed.send(ctx)
          else:
            if userid == None:
              embed=Embed('Error!', 'Make sure to specify a user to get warned!', 'warning')
              return await embed.send
            if rulenum == None:
              embed=Embed('Error!', 'Make sure to specify a rule you want to make sure it gets enforced!')
              return await embed.send(ctx)
            if additional_note == None:
              pass
            discord.utils.get(client.get_all_users(), id=userid)
            warnuser = await client.get_user_info(userid)
            await client.send_message(warnuser, "Hello!")
            
def setup(client):
    client.add_cog(Command(client))'''
from discord.ext import commands
from packages.utils import Embed, ImproperType
import discord
from discord.utils import get

class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def warn(self, ctx, userid, rulenum, *additional_note):
        #if await ImproperType.check(ctx): return
        if ctx.author.id not in [505338178287173642]:
            embed=Embed('Error!', 'This commmand is developer only!', 'tools')
            return await embed.send(ctx)
        else:
            if userid == None:
              embed=Embed('Error!', 'Make sure to specify a user to get warned!', 'warning')
              return await embed.send
            if rulenum == None:
              embed=Embed('Error!', 'Make sure to specify a rule you want to make sure it gets enforced!')
              return await embed.send(ctx)
            if additional_note == None:
              pass
            client = self.client
            #discord.utils.get(client.get_all_users(), id=userid)
            #await client.get_user_info(userid)
            #await client.send_message(userid, "Hello!")
            await userid.send('TEST')
def setup(client):
    client.add_cog(Command(client))
