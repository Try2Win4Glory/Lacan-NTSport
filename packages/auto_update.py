from discord.ext import commands, tasks
import nitrotype
import os
import json
import time
from discord.utils import get
import discord
import copy, aiohttp
from compsmongo import DBClient
class AutoUpdate(commands.Cog):
    def __init__(self, client):
        self.always_update.start()
        self.client = client
    async def fetch(self, session, url, data=None):
        async with session.post(url, data=data) as response:
            return await response.text()
    @tasks.loop(seconds=30)
    async def always_update(self):
        f = open('dailyupdate.txt')
        if int(time.time()) >= int(f.readlines()[0].strip()):
            async with aiohttp.ClientSession() as session:
                await self.fetch(session, 'https://lacanitemshop.nitrotypers.repl.co/update/daily', data={'key': os.getenv('DB_KEY')})
            f.close()
            with open('dailyupdate.txt', 'w') as f:
                f.write(str(round(time.time())+86400))
        f = open('weeklyupdate.txt')
        if int(time.time()) >= int(f.readlines()[0].strip()):
            async with aiohttp.ClientSession() as session:
                await self.fetch(session, 'https://lacanitemshop.nitrotypers.repl.co/update/weekly', data={'key': os.getenv('DB_KEY')})
            f.close()
            with open('weeklyupdate.txt', 'w') as f:
                f.write(str(round(time.time())+604800))
        
        dbclient = DBClient()
        collection = dbclient.db['test']
        documents = await dbclient.get_array(collection, {})
        async for data in documents:
            old = copy.deepcopy(data)
            compid = data['compid']
            if data['other']['ended'] == True:
                continue
            endcomptime = data['other']['endcomptime']
            if round(time.time()) < endcomptime:
              try:
                  await nitrotype.update_comp(compid)
                  continue
              except:
                pass
            elif round(time.time()) >= endcomptime:
                await nitrotype.update_comp(str(compid))
                lb = await nitrotype.l(str(compid))
                embed = discord.Embed(
                    title='Live Leaderboards',
                    description='This is where you can view everyone\'s progress during the competition!',
                    color=0x15E700
                )
                usernames = []
                races = []
                for stat in lb[1]:
                    if stat[1] == '':
                        usernames.append(f'{stat[0]}\n')
                    else:
                        usernames.append(f'{stat[1]}\n')
                    races.append(str(stat[2]))
                usernames = ''.join(usernames)
                races = '\n'.join(races)
                embed.add_field(
                    name='Team Members',
                    value=usernames
                )
                embed.add_field(
                    name="Races",
                    value=races
                )
                try:
                    user = await self.client.fetch_user(data['other']['author'])
                    await user.send(embed=embed)
                    await user.send('Your conpetition has ended! Comp ID: `'+compid+'`.  Check out the other categories of your competition by doing `n.lb '+compid+'` and adding `speed`, `accuracy`, `races`, or `points`. Ex: `n.lb '+compid+' points`')
                except:
                    pass
                data['other']['ended'] = True
                await dbclient.update_array(dbclient.db["test"], old, data)
        print('Auto Update Done')
def setup(client):
    client.add_cog(AutoUpdate(client))
