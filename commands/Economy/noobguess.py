'''A game where you guess a silhouetted Nitro Type car'''

from discord.ext import commands
from discord import Message
from packages.utils import Embed, ImproperType
from packages.nitrotype import Guesser
from asyncio import TimeoutError
import json
import requests
import os
import random
from cooldowns.guess import rateLimit, cooldown_add
from mongoclient import DBClient


class Command(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def noobguess(self, ctx):
        #return await ctx.send('This command is currently under maintenance. The developers will try to get it up again as soon as possible. In the meantime feel free to use `n.help` to get the other commands. Thank you for your understanding!')

        list_of_lacans = ['<:lacan_economy_1:801006407536607262>','<:lacan_economy_2:801004873612132382>','<:lacan_economy_3:801004873214722079>','<:lacan_economy_4:801004868126113822>','<:lacan_economy_5:801004868348936203>','<:lacan_economy_6:801004863433605160>','<:lacan_economy_7:801004870643220481>','<:lacan_economy_8:801004872820457483>','<:lacan_economy_9:801004872417804298>','<:lacan_economy_10:801004872811413514>']
        random_lacan = random.choice(list_of_lacans)

        if str(ctx.author) in rateLimit:
            embed = Embed('Cooldown!','You are on cooldown. Wait `5` seconds before running this command again.','alarm clock')
            return await embed.send(ctx)
        if await ImproperType.check(ctx): return
        if ctx.author.id not in [505338178287173642, 637638904513691658, 396075607420567552]:
            cooldown_add(str(ctx.author))
        def check(message: Message):
            return message.author.id == ctx.author.id

        guesser = Guesser(shadow=False)
        embed = Embed('Guess That Car!', guesser.formatted, 'game die')
        embed.image(guesser.pic)
        await embed.send(ctx)

        try:
            response = await self.client.wait_for('message', timeout=20, check=check)
        except TimeoutError:
            embed = Embed('<a:error:800338727645216779>  Error!', 'You ran out of time because you took longer than `20` seconds to respond!')
            await embed.send(ctx)
        else:
            if response.content.lower() in list('abcd'):
                if response.content.lower() == guesser.correct:
                    embed = Embed('<a:Check:797009550003666955>  Correct!', 'Your answer was right! You also earned **1** '+random_lacan+'!')
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
                            user['points'] += 1
                            await dbclient.update_array(collection, old, user)
                    except:
                        await dbclient.create_doc(collection, {'userid': str(ctx.author.id), 'points': 1})
                else:
                    embed = Embed('<a:false:800330847865143327>  Wrong!',f'Your answer was wrong! The correct answer was **{guesser.options[guesser.correct]}**. You also lost **1** '+random_lacan+'.')
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
                            user['points'] -= 1
                            await dbclient.update_array(collection, old, user)
                    except:
                        await dbclient.create_doc({'userid': str(ctx.author.id), 'points': -1})

            else:
                embed = Embed('<a:false:800330847865143327>  Wrong!',f'You didn\'t give a valid response! The correct answer was **{guesser.options[guesser.correct]}**. You also lost **1** '+random_lacan+'.')
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
                        user['points'] -= 1
                        await dbclient.update_array(collection, old, user)
                except:
                    await dbclient.create_doc({'userid': str(ctx.author.id), 'points': -1})


def setup(client):
    client.add_cog(Command(client))
