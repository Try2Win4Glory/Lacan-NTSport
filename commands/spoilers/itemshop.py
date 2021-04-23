'''What\'s going to be in tomorrow\'s itemshop?'''
import aiohttp
import json
from discord.ext import tasks, commands
import discord
import asyncio
from discord.ext import commands
from packages.utils import Embed, ImproperType

class Command(commands.Cog):
    def __init__(self, client):
        self.client = client
    async def get(self, session, url):
        async with session.get(url) as response:
            return await response.text()



    def itemSearch(self, itemList, id, searchTerm):
        #Returns details about an item from bootstrap
        for item in itemList:
            if item[searchTerm] == id:
                return item


    def parse(self, bootstrapText):
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
        #print(leaked)        
        # Return a new structure with information about each item
        for item in leaked:
                itemID = item["id"]
                if item["type"] == "car":
                    itemInfo = self.itemSearch(carDictionary, itemID, "carID")
                else:
                    itemInfo = self.itemSearch(lootDictionary, itemID, "lootID")
                leakedList.append(itemInfo)

        return(leakedList)

    async def create_embed(self):
        async with aiohttp.ClientSession() as session:
            text = await self.get(session, 'https://www.nitrotype.com/index//bootstrap.js')
        parsedItemShop = self.parse(text)
        print(parsedItemShop)
        
        try:
          titleortrail = parsedItemShop[2]['type']
          if titleortrail == 'trail':
            titleortrailminus = 'Trail'
            traillink = f'https://nitrotype.com/assets/trails/{parsedItemShop[2]["name"]}'
          else:
            titleortrailminus = 'Title'
            titleortrail = 'title'
          titlename = parsedItemShop[1]["name"]
          titleid = parsedItemShop[1]["lootID"]
          titleprice = parsedItemShop[1]["price"]
          titledesc = parsedItemShop[1]["longDescription"]
          title_comma_price = "{:,}".format(titleprice)
        except:
          try:
            titleortrail = parsedItemShop[2]['type']
            if titleortrail == 'trail':
              titleortrailminust = 'Trail'
              traillink = f'https://nitrotype.com/assets/trails/{parsedItemShop[2]["name"]}'
            else:
              titleortrailminus = 'Title'
              titleortrail = 'title'
            titlename = parsedItemShop[2]["name"]
            titleid = parsedItemShop[2]["lootID"]
            titleprice = parsedItemShop[2]["price"]
            titledesc = parsedItemShop[2]["longDescription"]
            title_comma_price = "{:,}".format(titleprice)
          except:
            try:
              titleortrail = parsedItemShop[0]['type']
              if titleortrail == 'trail':
                titleortrailminus = 'Trail'
                traillink = f'https://nitrotype.com/assets/trails/{parsedItemShop[0]["name"]}'
              else:
                titleortrailminus = 'Title'
                titleortrail = 'title'
              titlename = parsedItemShop[0]["name"]
              titleid = parsedItemShop[0]["lootID"]
              titleprice = parsedItemShop[0]["price"]
              titledesc = parsedItemShop[0]["longDescription"]
              title_comma_price = "{:,}".format(titleprice)
            except:
              pass

        try:
          stickername = parsedItemShop[0]["name"]
          stickerid = parsedItemShop[0]["lootID"]
          stickerprice = parsedItemShop[0]["price"]
          stickerdesc = parsedItemShop[0]["longDescription"]
          stickerpic = parsedItemShop[0]["options"]["src"]
          sticker_comma_price = "{:,}".format(stickerprice)
        except:
          try:
            stickername = parsedItemShop[1]["name"]
            stickerid = parsedItemShop[1]["lootID"]
            stickerprice = parsedItemShop[1]["price"]
            stickerdesc = parsedItemShop[1]["longDescription"]
            stickerpic = parsedItemShop[1]["options"]["src"]
            sticker_comma_price = "{:,}".format(stickerprice)
          except:
            try:
              stickername = parsedItemShop[2]["name"]
              stickerid = parsedItemShop[2]["lootID"]
              stickerprice = parsedItemShop[2]["price"]
              stickerdesc = parsedItemShop[2]["longDescription"]
              stickerpic = parsedItemShop[2]["options"]["src"]
              sticker_comma_price = "{:,}".format(stickerprice)
            except:
              pass

        try:
          carname = parsedItemShop[0]["name"]
          carid = parsedItemShop[0]["carID"]
          carprice = parsedItemShop[0]["price"]
          cardesc = parsedItemShop[0]["longDescription"]
          carpic = parsedItemShop[0]["options"]["largeSrc"]
          car_comma_price = "{:,}".format(carprice)
        except:
          try:
            carname = parsedItemShop[1]["name"]
            carid = parsedItemShop[1]["carID"]
            carprice = parsedItemShop[1]["price"]
            cardesc = parsedItemShop[1]["longDescription"]
            carpic = parsedItemShop[1]["options"]["largeSrc"]
            car_comma_price = "{:,}".format(carprice)
          except:
            carname = parsedItemShop[2]["name"]
            carid = parsedItemShop[2]["carID"]
            carprice = parsedItemShop[2]["price"]
            cardesc = parsedItemShop[2]["longDescription"]
            carpic = parsedItemShop[2]["options"]["largeSrc"]
            car_comma_price = "{:,}".format(carprice)


        embed = discord.Embed(title=":eyes:  Itemshop spoilers!  :eyes:", description = "What's going to be in the next shop?", color=0xFFA500)
        try:
          embed.set_image(url = f"https://nitrotype.com/cars/{carpic}")
        except:
          pass
        try:
          embed.set_thumbnail(url = f"https://nitrotype.com{stickerpic}")
        except:
          pass
        try:
          embed.add_field(name = f'__**{titleortrailminus}:**__',value = f'**Name:** *"{titlename}"*\n**ID:** `{titleid}`\n**Price:** $**{title_comma_price}**\n**Description:** {titledesc}\n**Picture:** {traillink}', inline = True)
        except:
          try:
            embed.add_field(name = f'__**{titleortrailminus}:**__',value = f'**Name:** *"{titlename}"*\n**ID:** `{titleid}`\n**Price:** $**{title_comma_price}**\n**Description:** {titledesc}', inline = True)
          except:
            pass
        try:
          embed.add_field(name = '__**Sticker:**__',value = f'**Name:** *"{stickername}"*\n**ID:** `{stickerid}`\n**Price:** $**{sticker_comma_price}**\n**Description:** {stickerdesc}\n**Picture:** https://nitrotype.com{stickerpic}', inline = True)
        except:
          pass
        try:
          embed.add_field(name = '__**Car:**__', value = f'**Name:** *"{carname}"*\n**ID:** `{carid}`\n**Price:** $**{car_comma_price}**\n**Description:** {cardesc}\n**Picture:** https://nitrotype.com/cars/{carpic}')
        except:
          pass
        return embed
    @commands.command()
    async def itemshop(self, ctx):
        embed = await self.create_embed()
        await ctx.send(embed = embed)
def setup(client):
    client.add_cog(Command(client))