'''What\'s going to be in tomorrow\'s Itemshop?'''
import discord
import asyncio
import calendar
import datetime
from datetime import date
from discord.ext import commands
from packages.utils import Embed, ImproperType
class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def itemshop(self, ctx):
      curr_date = date.today()
      weekday = calendar.day_name[curr_date.weekday()]
      #if weekday == 'Thursday' or weekday == 'Friday':
      if weekday == 'Friday':
        display = 'weekly'
      else:
        display = 'daily'
      dailyspoiler = 'https://www.nitrotype.com'
      weeklyspoiler = 'https://www.nitrotype.com'
      dailyspoiler = 'https://itemshopspoilers.adl2212.repl.co/daily.png'
      weeklyspoiler = 'https://itemshopspoilers.adl2212.repl.co/weekly.png'
      tomorrow = datetime.date.today() + datetime.timedelta(days=1)
      embed=Embed(f'Itemshop of {tomorrow.month}/{tomorrow.day}/{tomorrow.year}', 'Those Items can be purchased in tomorrow\'s Itemshop.', 'eyes')
      embed.field('Spoilers', f'Itemshop {tomorrow.month}/{tomorrow.day}/{tomorrow.year}')
      if display == 'daily':
        try:
          embed.image(dailyspoiler)
        except:
          embed.field('Error', 'Unfortunately no Spoiler for tomorrow\'s Items could be retrieved. Please try again later.', 'warning')
      if display == 'weekly':
        try:
          embed.image(weeklyspoiler)
        except:
          embed.field('Error', 'Unfortunately no Spoiler for tomorrow\'s Items could be retrieved. Please try again later.', 'warning')
      return await embed.send(ctx)
def setup(client):
    client.add_cog(Command(client))
