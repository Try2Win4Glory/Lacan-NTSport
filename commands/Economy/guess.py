'''A game where you guess a silhouetted Nitro Type car'''

from discord.ext import commands
from discord import Message
from packages.utils import Embed, ImproperType
from packages.nitrotype import Guesser
from asyncio import TimeoutError
import json
#from variables.lacanlog import listoflacanlogchannels
#from variables.lacanlog import channel0
#from variables.lacanlog import channel1
from discord.utils import get
import requests
import os, discord
from cooldowns.guess import rateLimit, cooldown_add
from mongoclient import DBClient
import random
import asyncio, json, requests, copy
class Command(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def guess(self, ctx):
        #return await ctx.send('This command is currently under maintenance. The developers will try to get it up again as soon as possible. In the meantime feel free to use `n.help` to get the other commands. Thank you for your understanding!')

        list_of_lacans = ['<:lacan_economy_1:801006407536607262>','<:lacan_economy_2:801004873612132382>','<:lacan_economy_3:801004873214722079>','<:lacan_economy_4:801004868126113822>','<:lacan_economy_5:801004868348936203>','<:lacan_economy_6:801004863433605160>','<:lacan_economy_7:801004870643220481>','<:lacan_economy_8:801004872820457483>','<:lacan_economy_9:801004872417804298>','<:lacan_economy_10:801004872811413514>']
        random_lacan = random.choice(list_of_lacans)
        
        data = json.loads(requests.get('https://lacanitemshop.nitrotypers.repl.co/data.json').text)
        shopcars = [data['daily']['img'], data['weekly']['img']]
        dbclient = DBClient()
        collection = dbclient.db.pointsdb
        data = await dbclient.get_array(collection, {'$and': [{'userid': str(ctx.author.id)}, {'userid': str(ctx.author.id)}]})
        async for d in data:
            user = d
            break
        try:
          old = copy.deepcopy(user)
          for car in user['cars']:
            if user['equipped']['img'] in shopcars:
              carbonus = True
              break
          else:
            print(shopcars)
            carbonus = False
        except:
            carbonus = False
        
        #channels = self.client.get_all_channels()
        #channel1 = get(channels, id=787018607481192479)
        #channel2 = get(channels, id=803879362226946088)

        green =0x40AC7B
        red = 0xE84444
        orange = 0xF09F19
        #dnd = discord.Colour(discord.Status.dnd)
        #idle = discord.Colour(discord.Status.idle)
        #if channels.name in ['logs', 'mod-log']:
          #channel = get(channels, channels)
        #channel = get(channels, if channels.name in ['lacan-log'])
        #channel = get(channels, id=803879362226946088 and 787018607481192479)

        #channel001 = get(channels, id=787018607481192479)
        #channel002 = get(channels, id=803879362226946088)

        if str(ctx.author) in rateLimit:
            embed = Embed('Cooldown!','You are on cooldown. Wait `5` seconds before running this command again.','alarm clock')
            return await embed.send(ctx)
        if await ImproperType.check(ctx): return
        if ctx.author.id not in [
          #Try2Win4Glory
            505338178287173642, 
          #Typerious
            637638904513691658, 
          #adl212
            396075607420567552]:
            cooldown_add(str(ctx.author))
        def check(message: Message):
            return message.author.id == ctx.author.id

        guesser = Guesser(shadow=True)
        embed = Embed('Guess That Car!', guesser.formatted, 'game die')
        embed.image(guesser.pic)
        await embed.send(ctx)

        try:
            response = await self.client.wait_for('message', timeout=20, check=check)
        except TimeoutError:
            embed = Embed('<a:error:800338727645216779>  Error!', 'You ran out of time because you took longer than `20` seconds to respond! The correct answer was :regional_indicator_'+guesser.correct+': (**'+guesser.options[guesser.correct]+'**).')
            return await embed.send(ctx)
        else:
            if response.content.lower() in list('abcd'):
                if response.content.lower() == guesser.correct:
                  if carbonus == True:
                    earned = 4
                    embed = Embed('<a:Check:797009550003666955>  Correct!', 'Your answer was right! You also earned **4** '+random_lacan+' because of equipping a daily / weekly car!')
                    await embed.send(ctx)
                  else:
                    earned = 2
                    embed = Embed('<a:Check:797009550003666955>  Correct!', 'Your answer was right! You also earned **2** '+random_lacan+'!')
                    await embed.send(ctx)
                  dbclient = DBClient()
                  collection = dbclient.db.pointsdb
                  data = await dbclient.get_array(collection, {'$and': [{'userid': str(ctx.author.id)}, {'userid': str(ctx.author.id)}]})
                  async for d in data:
                      user = d
                      break
                  try:
                      old = user.copy()
                      if user['userid'] == str(ctx.author.id):
                        user['points'] += earned
                        await dbclient.update_array(collection, old, user)
                  except UnboundLocalError:
                        await dbclient.create_doc(collection, {'userid': str(ctx.author.id), 'points': earned})
                    #Embed for lacan Log
                    #embed1 = discord.Embed(title=f'{random_lacan}  Lacan Log', description=str(ctx.author), color= green)
                    #embed1.add_field(name='__Won__', value='2')
                    #embed1.add_field(name='__Command__', value='`n.guess`')
                    #embed1.add_field(name='__Type__', value='*Correct response*')
                    #embed1.add_field(name='__Total__', value=f'{total_points}')
                    #embed1.add_field(name='__User ID__', value=f'`{ctx.author.id}`')
                    #await channel0.send(embed=embed1)
                    #await channel1.send(embed=embed1)
                else:
                    embed = Embed('<a:false:800330847865143327>  Wrong!',f'Your answer was wrong! The correct answer was :regional_indicator_'+guesser.correct+': (**'+guesser.options[guesser.correct]+'**). You also lost **2** '+random_lacan+'.')
                    await embed.send(ctx)
                    dbclient = DBClient()
                    collection = dbclient.db.pointsdb
                    data = await dbclient.get_array(collection, {'$and': [{'userid': str(ctx.author.id)}, {'userid': str(ctx.author.id)}]})
                    async for d in data:
                        user = d
                        break
                    try:
                        old = user.copy()
                        if user['userid'] == str(ctx.author.id):
                            user['points'] -= 2
                            await dbclient.update_array(collection, old, user)
                    except UnboundLocalError:
                        await dbclient.create_doc({'userid': str(ctx.author.id), 'points': -2})
                    
                    #Embed for lacan Log
                    #embed1 = discord.Embed(title=f'{random_lacan}  Lacan Log', description=str(ctx.author), color= red)
                    #embed1.add_field(name='__Lost__', value='2')
                    #embed1.add_field(name='__Command__', value='`n.guess`')
                    #embed1.add_field(name='__Type__', value='*Wrong response*')
                    #embed1.add_field(name='__Total__', value=f'{total_points}')
                    #embed1.add_field(name='__User ID__', value=f'`{ctx.author.id}`')
                    #await channel0.send(embed=embed1)
                    #await channel1.send(embed=embed1)

            else:
                embed = Embed('<a:false:800330847865143327>  Wrong!',f'You didn\'t give a valid response! The correct answer was **{guesser.options[guesser.correct]}**. You also lost **2** '+random_lacan+'.')
                await embed.send(ctx)
                dbclient = DBClient()
                collection = dbclient.db.pointsdb
                data = await dbclient.get_array(collection, {'$and': [{'userid': str(ctx.author.id)}, {'userid': str(ctx.author.id)}]})
                async for d in data:
                    user = d
                    break
                try:
                    old = user.copy()
                    if user['userid'] == str(ctx.author.id):
                        user['points'] -= 2
                        await dbclient.update_array(collection, old, user)
                except UnboundLocalError:
                    await dbclient.create_doc({'userid': str(ctx.author.id), 'points': -2})
                
                #Embed for lacan Log
                #embed1 = discord.Embed(title=f'{random_lacan}  Lacan Log', description=str(ctx.author), color= orange)
                #embed1.add_field(name='__Lost__', value=f'2')
                #embed1.add_field(name='__Command__', value='`n.guess`')
                #embed1.add_field(name='__Type__', value='*Invalid response*')
                #embed1.add_field(name='__Total__', value=f'{total_points}')
                #embed1.add_field(name='__User ID__', value=f'`{ctx.author.id}`')
                #await channel0.send(embed=embed1)
                #await channel1.send(embed=embed1)
                

def setup(client):
    client.add_cog(Command(client))
