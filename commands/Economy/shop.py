'''Buy epic stuff in the shop!'''
from discord.ext import commands
from packages.utils import Embed, ImproperType
import requests, json, os
from discord.utils import get
from mongoclient import DBClient
import random
import time
from asyncio.exceptions import TimeoutError
from discord import Reaction, User
class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    def format_time(self, seconds):
        hours = seconds // (60*60)
        return "%02i" % (hours)
    def get_page(self, page_number, ctx, data, dbdata=None):
        n = page_number
        embed=Embed(':shopping_cart:  Shop', f'*{str(ctx.author)} entered the shop.* \nBuy epic stuff to enjoy the bot even more!')
        if n == 0:
            try:
                embed.field('Currently equipped', f'__Name:__ `{dbdata["equipped"]["car"]}`')
                embed.image(f'https://www.nitrotype.com/cars/{dbdata["equipped"]["img"]}')
            except:
                embed.field('Currently equipped', 'None')

            embed.field('Buy / equip items', 'Use `n.buy [Item ID]` to buy an item and `n.equip [Item ID]` to equip an item')
            embed.field('Reward', 'Equip your cars and get epic multipliers in the economy category!')
            embed.footer('Get amazing perks with items!')
            return embed
        if n == 1:
            f = open('weeklyupdate.txt')
            timeleft = int(f.readlines()[0]) - round(time.time())
            embed.field('Weekly Items:', f'__Name:__ `{data["weekly"]["car"]}`\n__Price:__ `{str(data["weekly"]["price"])}` Lacans\n__Time left:__ `{self.format_time(timeleft)}` hours')
            embed.footer('Get amazing perks with items!')
            embed.image(f'https://www.nitrotype.com/cars/{data["weekly"]["img"]}')
            return embed
        if n == 2:
            f = open('dailyupdate.txt')
            timeleft = int(f.readlines()[0]) - round(time.time())
            embed.field('Daily Items:', f'__Name:__ `{data["daily"]["car"]}`\n__Price:__ `{str(data["daily"]["price"])}` Lacans\n__Time left:__ `{self.format_time(timeleft)}` hours')
            embed.footer('Get amazing perks with items!')
            embed.image(f'https://www.nitrotype.com/cars/{data["daily"]["img"]}')
            return embed
    @commands.command()
    async def shop(self, ctx):
        data = json.loads(requests.get('https://lacanitemshop.nitrotypers.repl.co/data.json').text)
        dbclient = DBClient()
        collection = dbclient.db.pointsdb
        dbdata = await dbclient.get_array(collection, {'$and': [{'userid': str(ctx.author.id)}, {'userid': str(ctx.author.id)}]})
        dbuser = dbdata
        page = 0
        def check(reaction:Reaction, user:User):
            return user.id == ctx.author.id
        embed = self.get_page(page, ctx, data, dbdata=dbuser)
        message = await ctx.send(embed=embed.default_embed())
        await message.add_reaction('🔄')
        while True:
            try:
                reaction, user = await self.client.wait_for('reaction_add', timeout=120, check=check)
            except TimeoutError:
                break
            if page+1 > 2:
                page = 0
            else:
                page += 1
            embed = self.get_page(page, ctx, data, dbdata=dbuser)
            await message.remove_reaction(reaction, user)
            await message.edit(embed=embed.default_embed())

def setup(client):
    client.add_cog(Command(client))