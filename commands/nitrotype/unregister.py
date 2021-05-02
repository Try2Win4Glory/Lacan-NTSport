
'''Unlink your NT account from your discord.'''
from discord.ext import commands
from packages.utils import Embed, ImproperType
from packages.nitrotype import Racer
import requests
import os
import json
from discord.utils import get
from mongoclient import DBClient
class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def unregister(self, ctx):
        #return await ctx.send('This command is currently under maintenance. The developers will try to get it up again as soon as possible. In the meantime feel free to use `n.help` to get the other commands. Thank you for your understanding!')
        thelistofroles = ["Registered", "Gold Member", ">99% Accuracy", "99% Accuracy", "98% Accuracy", "97% Accuracy", "96% Accuracy", "94-95% Accuracy", "90-93% Accuracy", "87-89% Accuracy", "84-86% Accuracy", "80-83% Accuracy", "75-79% Accuracy", "<75% Accuracy", "220+ WPM", "210-219 WPM", "200-209 WPM", "190-199 WPM", "180-189 WPM", "170-179 WPM", "160-169 WPM", "150-159 WPM", "140-149 WPM", "130-139 WPM", "120-129 WPM", "110-119 WPM", "100-109 WPM", "90-99 WPM", "80-89 WPM", "70-79 WPM", "60-69 WPM", "50-59 WPM", "40-49 WPM", "30-39 WPM", "20-29 WPM", "10-19 WPM", "1-9 WPM", "500000+ Races", "250000-499999 Races", "200000-249999 Races", "150000-199999 Races", "100000-149999 Races", "75000-99999 Races", "50000-74999 Races", "40000-49999 Races", "30000-39999 Races", "20000-29999 Races", "10000-19999 Races", "5000-9999 Races", "3000-4999 Races", "1000-2999 Races","500-999 Races", "100-499 Races", "50-99 Races", "1-49 Races"]
        teamswithroles = [
          # Insert Global Team Tags Here
        ]

        #Team N8TE | Server Owner: 630761745140547625
        if ctx.guild.id in [
          636582509429260289
        ]:
          teamswithroles.append('[N8TE]')
        #Team DRPT | Server Owner: 723224207651111003
        if ctx.guild.id in [
          742854336618561608
        ]:
          teamswithroles.append('[DRPT]')
        #Team RRN | Server Owner: 653772108815532053
        if ctx.guild.id in [
          696055942055198760
        ]:
          teamswithroles.append('[RRN]')
        #Team NEWS | Server Owner: 272370019894165505
        if ctx.guild.id in [
          835305919679692850
        ]:
          teamswithroles.append('[NEWS]')
        #Team TEST | Server Owner: 505338178287173642
        if ctx.guild.id in [
          833317505888026644
        ]:
          teamswithroles.append('[TEST]')
        premiumserver = False
        #dbdata = json.loads(requests.get('https://test-db.nitrotypers.repl.co', data={"key": dbkey}).text)
        dbclient = DBClient()
        collection = dbclient.db.NT_to_discord
        dbdata = await dbclient.get_big_array(collection, 'registered')
        pcollection = dbclient.db.premium
        pdata = await dbclient.get_big_array(pcollection, 'premium')
        for x in pdata['premium']:
            if x['serverID'] == str(ctx.author.guild.id):
                premiumserver = True
                break
        for x in dbdata['registered']:
            if str(ctx.author.id) == x['userID']:
                if premiumserver:
                    for role in (ctx.author.roles):
                        name = role.name
                        if name in thelistofroles or name in teamswithroles:
                            role = get(ctx.message.guild.roles, id=role.id)
                            await ctx.author.remove_roles(role)
                        try:
                          role = get(ctx.message.guild.roles, name='Unregistered')
                          await ctx.author.add_roles(role)
                        except:
                          pass  
                dbdata['registered'].pop(dbdata['registered'].index(x))
                embed = Embed('<a:Check:797009550003666955>  Success!', f'Unregistered {ctx.author.mention}!')
               
                await embed.send(ctx)
                #requests.post('https://test-db.nitrotypers.repl.co', data={"key": os.getenv('DB_KEY'), "data": json.dumps(dbdata)})
                dbclient = DBClient()
                collection = dbclient.db.NT_to_discord
                await dbclient.update_big_array(collection, 'registered', dbdata)
                return
def setup(client):
    client.add_cog(Command(client))
