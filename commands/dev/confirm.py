'''Confirms the ownership of a registered User'''

from discord.ext import commands
from packages.utils import Embed, ImproperType
import discord
import requests
import json
import copy
import os
from mongoclient import DBClient
from packages.nitrotype import Racer

class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def confirm(self, ctx, discordid):
        dbclient = DBClient()
        permcollection = dbclient.client.dev.confirm
        serversearch = ctx.guild.id
        x = await permcollection.find_one({"serverID":str(serversearch)})
        dev = await permcollection.find_one({"bypass":"dev"})
        bypass = False
        if dev != None:
          if str(ctx.author.id) in str(dev["dev"]):
            permittedserver = True
            devbypass = True
          else:
            permittedserver = False
            devbypass = False
        else:
          permittedserver = False
          devbypass = False

      # Server Confirm Not Supported
        if x == None and devbypass == False:
          permittedserver = False
          embed = Embed('Error!', 'This server does not have permission to use this command. Click [here](https://www.latlmes.com/entertainment/permission-application-1) to apply for permission.', 'warning')
          return await embed.send(ctx)
      # Server Confirm Supported
        elif x != None or devbypass == True:
          permittedserver = True

      # Author Permitted Check
        if permittedserver == True and devbypass != True:
            for role in ctx.author.roles:
              if str(role.id) in str(x['permitted']):
                bypass = True
                break
              else:
                bypass = False

        if bypass == False and devbypass == True:
          bypass = True

        if bypass == False:
          embed = Embed('Error!', 'Lol. Did you really think it\'s possible for you to confirm another user when you are not a dev? Click [here](https://www.latlmes.com/entertainment/dev-application-1) to apply for dev.', 'warning')
          return await embed.send(ctx)
        else:
            discordid = discordid.replace("!", "")
            discordid = discordid.replace("<@", "")
            discordid = discordid.replace(">", "")
            dbclient = DBClient()
            collection = dbclient.db.NT_to_discord
            #dbdata = await dbclient.get_array(collection, {[{'userID': str(discordid)}]})
            dbdata = await collection.find_one({"userID":discordid})
            print(dbdata)
            ntuser = dbdata['NTuser']
            old = copy.deepcopy(dbdata)
            for elem in dbdata:
              # Delete previous Collection  
              await collection.delete_one(dbdata)

              # Create new Collection
              await dbclient.create_doc(collection, {
                "NTuser": ntuser,
                "userID": str(discordid),
                "verified": "true"
              })
              embed=Embed('<a:Check:797009550003666955>  Success', f'{ctx.author.mention} confirmed <@{discordid}>\'s Ownership of the Nitrotype Account **{ntuser}**.')
              await embed.send(ctx)
              try:
                channel1 = discord.utils.get(self.client.get_all_channels(), id=803938544175284244)
                dontlog = [505338178287173642]
                if ctx.author.id not in dontlog:
                    channel2 = discord.utils.get(self.client.get_all_channels(), id=901503736013262888)
                    channel3 = discord.utils.get(self.client.get_all_channels(), id=924334305570852916)
                embed = Embed('<:dev:901381277477900358>  Confirm', f'<@{str(discordid)}>\'s Ownership was confirmed by {str(ctx.author.mention)}.', color=0x00ff00)
                embed.field('ID', f'`{discordid}`')
                embed.field('Linked Account', f'`{ntuser}`')
                embed.field('Link', f'[:link:](https://nitrotype.com/racer/{ntuser})')
                embed.field('Registered by', f'{str(ctx.author.name)}#{str(ctx.author.discriminator)}')
                embed.field('Author', f'`{str(ctx.author.id)}`')
                embed.field('Guild', f'`{str(ctx.guild.name)}`')
                msg1 = await channel1.send(embed=embed.default_embed())
                if ctx.author.id not in dontlog:
                    msg2 = await channel2.send(embed=embed.default_embed())
                    msg3 = await channel3.send(embed=embed.default_embed())
              except:
                print('Couldn\'t log confirm.')
              break
            else:
              embed = Embed('Error!', 'Doesn\'t seem like `'+userid+'` is registered!', 'warning')
              return await embed.send(ctx)
def setup(client):
    client.add_cog(Command(client))
