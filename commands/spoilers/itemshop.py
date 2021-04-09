'''Get Spoilers of next days itemshop!'''
import requests
from discord.ext import commands
from packages.utils import Embed, ImproperType
import json
from PIL import Image
import os
import PIL
import glob
class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def itemshop(self, ctx):
      def get(url):
          # Returns text from a GET request
          return requests.get(url).text

      def itemSearch(itemList, id, searchTerm):
          #Returns details about an item from bootstrap
          for item in itemList:
              if item[searchTerm] == id:
                  return item


      def parse(bootstrapText):
          leakedList = []

          # Parsing the bootstrap to get loot information
          bootstrapLoot = bootstrapText.split("'LOOT', ")[1].split("]);")[0]
          lootDictionary = json.loads(bootstrapLoot)

          # Parse the bootstrap to get car information
          bootstrapCars = bootstrapText.split("'CARS', ")[1].split("]);")[0]
          carDictionary = json.loads(bootstrapCars)


          # Get a JSON list of leaked items
          bootstrapText = bootstrapText.split('items":')
          items = bootstrapText[len(bootstrapText)-1].split("}]]);")[0]
          leaked = json.loads(items)
          
          # Return a new structure with information about each item
          for item in leaked:
              itemID = item["id"]
              if item["type"] == "car":
                  itemInfo = itemSearch(carDictionary, itemID, "carID")
              else:
                  itemInfo = itemSearch(lootDictionary, itemID, "lootID")
              leakedList.append(itemInfo)

          return(leakedList)



      text = get('https://www.nitrotype.com/index//bootstrap.js')
      a = parse(text)
      
      # Title
      a1 = a[0]
      # Car
      a2 = a[1]
      # Sticker
      a3 = a[2]

      # Variables Titles
      #titletype = a[0]['type']
      titlename = a[0]['name']
      titledesc = a[0]['longDescription']
      titleid = a[0]['lootID']
      titleprice = a[0]['price']
      title_comma_price = "{:,}".format(titleprice)

      # Variables Cars
      #cartype = a[1]['type']
      carname = a[1]['name']
      cardesc = a[1]['longDescription']
      carid = a[1]['carID']
      carpic = a[1]['options']['largeSrc']
      carprice = a[1]['price']
      car_comma_price = "{:,}".format(carprice)
      car_smallpic = a[1]['options']['smallSrc']

      # Variables Stickers
      #stickertype = a[2]['type']
      stickername = a[2]['name']
      stickerdesc = a[2]['longDescription']
      stickerid = a[2]['lootID']
      stickerprice = a[2]['price']
      sticker_comma_price = "{:,}".format(stickerprice)
      stickerpic = a[2]['options']['src']

      # Embed
      embed=Embed(':eyes:  Itemshop spoilers!  :eyes:', f'What\'s going to be in the next shop?\n\n__**Title:**__\n**Name:** *"{titlename}"*\n**ID:** `{titleid}`\n**Price:** $**{title_comma_price}**\n**Description:** {titledesc}\n\n__**Car:**__\n**Name:** *"{carname}"*\n**ID:** `{carid}`\n**Price:** $**{car_comma_price}**\n**Description:** {cardesc}\n**Picture:** https://nitrotype.com/cars/{carpic}\n\n__**Sticker:**__\n**Name:** *"{stickername}"*\n**ID:** `{stickerid}`\n**Price:** $**{sticker_comma_price}**\n**Description:** {stickerdesc}\n**Picture:** https://nitrotype.com{stickerpic}')
      try:
        embed.image(f'https://assets.nitrotype.com/cars/{carpic}')
      except:
        pass
      stickerpic_whole = f'https://nitrotype.com{stickerpic}'
      #resized_sticker_img = str(stickerpic_whole.resize(20,20))
      try:
        embed.thumbnail(f'{stickerpic_whole}')
      except:
        pass



      # Raw Code  
      '''#Basic Code to display everything in a separate field
      for x in a:
        for k, v in x.items():
          k = k.replace("''", "")
          embed.field(k, v)'''

      '''# Code to display everything clean looking
      embed.field('Type', a[0]['type'])
      embed.field('Name', a[0]['name'])
      embed.field('Description', a[0]['longDescription'])
      embed.field('loot ID', a[0]['lootID'])
      try:
        embed.image('https://assets.nitrotype.com/cars/a[0]'+['options']['largeSrc'])
      except:
        pass'''
      '''# Code to display everything alltogether in one field
      embed.field('__Spoiler:__', f'```{a1}```\n\n```{a2}```\n\n```{a3}```')'''
      return await embed.send(ctx)
def setup(client):
    client.add_cog(Command(client))