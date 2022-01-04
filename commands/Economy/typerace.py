'''Type Some Text For Lacans!'''
from PIL import Image, ImageDraw, ImageFont
from discord.ext import commands
from packages.utils import Embed, ImproperType
import random, os, base64, discord, time
from mongoclient import DBClient
from discord.utils import get
import asyncio, json, requests, copy
from cooldowns.typerace import rateLimit, cooldown_add
class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    async def create_image(self, content):

        img = Image.new('RGB', (400, 50), color = (73, 109, 137))
        fontsize = 1  # starting font size

        # portion of image width you want text width to be
        img_fraction = 0.5

        font = ImageFont.truetype("font.otf", fontsize)
        while font.getsize(content)[0] < img_fraction*img.size[0]:
            # iterate until the text size is just larger than the criteria
            fontsize += 1
            font = ImageFont.truetype("font.otf", fontsize)

        d = ImageDraw.Draw(img)
        d.text((10,10), content, fill=(255, 255, 0), font=font)
        
        img.save('text.png')
    @commands.command()
    async def typerace(self, ctx):

        list_of_lacans = ['<:lacan_economy_1:801006407536607262>','<:lacan_economy_2:801004873612132382>','<:lacan_economy_3:801004873214722079>','<:lacan_economy_4:801004868126113822>','<:lacan_economy_5:801004868348936203>','<:lacan_economy_6:801004863433605160>','<:lacan_economy_7:801004870643220481>','<:lacan_economy_8:801004872820457483>','<:lacan_economy_9:801004872417804298>','<:lacan_economy_10:801004872811413514>']
        random_lacan = random.choice(list_of_lacans)
        channels = self.client.get_all_channels()
        channel = get(channels, id=803879362226946088)
        green =0x40AC7B
        red = 0xE84444
        orange = 0xF09F19
        
        if str(ctx.author) in rateLimit:
            embed = Embed('Cooldown!','You are on cooldown. Wait `10` seconds before running this command again.','alarm clock')
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
        
        
        with open('text.txt') as f:
            sentences = f.readlines()
        t = random.choice(sentences).strip()
        start = random.randint(1, 5)
        end = random.randint(start+4, start+8)
        t = ' '.join(((base64.standard_b64decode(t)).decode().split())[start:end])
        await self.create_image(t)
        embed = Embed("Type The Text!", "Type faster for bonus "+random_lacan+"!", "keyboard") #creates embed
        file = discord.File("text.png", filename="text.png")
        embed.image(url="attachment://text.png")
        await ctx.send(file=file, embed=embed.default_embed())
        def check(message: discord.Message):
            return message.author.id == ctx.author.id
        start = round(time.time())
        try:
            response = await self.client.wait_for('message', timeout=15, check=check)
        except asyncio.exceptions.TimeoutError:
            embed = Embed('<a:error:800338727645216779>  Error!', 'You ran out of time because you took longer than `15` seconds to respond!')
            return await embed.send(ctx)
        list_of_lacans = ['<:lacan_economy_1:801006407536607262>','<:lacan_economy_2:801004873612132382>','<:lacan_economy_3:801004873214722079>','<:lacan_economy_4:801004868126113822>','<:lacan_economy_5:801004868348936203>','<:lacan_economy_6:801004863433605160>','<:lacan_economy_7:801004870643220481>','<:lacan_economy_8:801004872820457483>','<:lacan_economy_9:801004872417804298>','<:lacan_economy_10:801004872811413514>']
        random_lacan = random.choice(list_of_lacans)
        channels = self.client.get_all_channels()
        #channel = get(channels, id=message.channel)
        green =0x40AC7B
        red = 0xE84444
        orange = 0xF09F19

        if ctx.author.id not in [505338178287173642, 637638904513691658, 396075607420567552]:
            cooldown_add(str(ctx.author))
        if response.content == t:
            dbclient = DBClient()
            scollection = dbclient.db.shop
            data = {"data": "", "weekly": ""}
            async for x in scollection.find({}):
                if x['type'] == 'weekly':
                    data['weekly'] = x
                if x['type'] == 'daily':
                    data['daily'] = x
            shopcars = [data['daily']['img'], data['weekly']['img']]
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
                    carbonus = False
            except:
                carbonus = False
            end = round(time.time())
            total = end-start
            bonus = round(5/total)
            if carbonus:
                default = 5
                earned = (default+bonus)*2
            else:
                default = 5
                earned = default+bonus
            embed = Embed('<a:Check:797009550003666955>  Congrats!', f'You Earned {random_lacan}!')
            embed.field('Default', str(default))
            embed.field('Bonus', str(bonus))
            embed.field('Total', str(earned))
            if carbonus:
                embed.field('Multiplier', 'X2')
                embed.footer('You earned double lacans by equipping the daily or weekly car!')
            await embed.send(ctx)
            try:
                if user['userid'] == str(ctx.author.id):
                    user['points'] += earned
                    await dbclient.update_array(collection, old, user)
            except UnboundLocalError:
                await dbclient.create_doc(collection, {'userid': str(ctx.author.id), 'points': earned})

        else:
            embed = Embed('<a:false:800330847865143327>  Oops!', 'You messed up sadly... and lost **5** '+random_lacan+'.')
            await embed.send(ctx)
            #Loose lacans
            dbclient = DBClient()
            collection = dbclient.db.pointsdb
            data = await dbclient.get_array(collection, {'$and': [{'userid': str(ctx.author.id)}, {'userid': str(ctx.author.id)}]})
            lost = -5
            async for d in data:
                user = d
                break
            try:
                old = user.copy()
                if user['userid'] == str(ctx.author.id):
                    user['points'] += lost
                    await dbclient.update_array(collection, old, user)
                else:
                    await dbclient.create_doc(collection, {'userid': str(ctx.author.id), 'points': lost})
            except UnboundLocalError:
                await dbclient.create_doc(collection, {'userid': str(ctx.author.id), 'points': lost})
            return


def setup(client):
    client.add_cog(Command(client))
