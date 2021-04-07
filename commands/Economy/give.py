'''Give your friend some <:lacan_economy:800335440719642704> after they beg'''

from discord.ext import commands
from packages.utils import Embed, ImproperType
from mongoclient import DBClient
import discord
import random
class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def give(self, ctx, giveto: discord.Member, amount):
        #return await ctx.send('This command is currently under maintenance. The developers will try to get it up again as soon as possible. In the meantime feel free to use `n.help` to get the other commands. Thank you for your understanding!')

        list_of_lacans = ['<:lacan_economy_1:801006407536607262>','<:lacan_economy_2:801004873612132382>','<:lacan_economy_3:801004873214722079>','<:lacan_economy_4:801004868126113822>','<:lacan_economy_5:801004868348936203>','<:lacan_economy_6:801004863433605160>','<:lacan_economy_7:801004870643220481>','<:lacan_economy_8:801004872820457483>','<:lacan_economy_9:801004872417804298>','<:lacan_economy_10:801004872811413514>']
        random_lacan = random.choice(list_of_lacans)

        dbclient = DBClient()
        collection = dbclient.db.pointsdb
        data = await dbclient.get_array(collection, {'$and': [{'userid': str(ctx.author.id)}, {'userid': str(ctx.author.id)}]})
        async for d in data:
            user = d
            break
        old = user.copy()
        try:
            if user['userid'] == str(ctx.author.id):
                if user['points'] < int(amount):
                    embed = Embed('Error!', 'You don\'t have that amount of '+random_lacan+'!')
                    return await embed.send(ctx)
                user['points'] -= int(amount)
                await dbclient.update_array(dbclient.db.pointsdb, old, user)
        except:
            embed = Embed('Error!', 'Unfortunately, you haven\'t won a guess game yet so you have no '+random_lacan+' to give!', '<a:error:800338727645216779>')
            return await embed.send(ctx)
        userid = giveto.id or giveto
        data = await dbclient.get_array(collection, {'$and': [{'userid': str(userid)}, {'userid': str(userid)}]})
        async for d in data:
            user = d
            break
        old = user.copy()
        try:
            if user['userid'] == str(giveto):
                user['points'] += int(amount)
            elif user['userid'] == str(giveto.id):
                user['points'] += int(amount)
            await dbclient.update_array(collection, old, user)
        except:
            embed = Embed('Error!', 'This person you want to send to doesn\'t exist in the database!', 'rofl')
            return await embed.send(ctx)

        embed = Embed('<a:success:800340618579935233>  Success!', '<@'+str(ctx.author.id)+'> has succesfully given '+giveto.mention+' **'+amount+'** '+random_lacan+'.')

        if (ctx.author.id) not in [505338178287173642, 637638904513691658, 396075607420567552]:
          try:
            await giveto.send(':gift: **You just received a gift!** :gift: \n\nYou have been sent **'+amount+'** '+random_lacan+' from '+str(ctx.author)+'!')
          except:
            embed=Embed('<a:error:800338727645216779>  Error!',''+giveto.mention+' has received '+str(ctx.author)+'\'s **'+amount+'** '+random_lacan+', but they have their DMs turned off so I couldn\'t Direct message '+giveto.mention+'.')
          await embed.send(ctx)
          await dbclient.update_array(collection, old, user)
          try:
            await ctx.message.delete()
          except:
            pass
          return await embed.send(ctx)
        else:
          try:
            await giveto.send(':tada: :gift: :tada: **WOAH Dude! One of the __DEVS__ just sent you a gift!** :tada: :gift: :tada:\n\nYou have been sent **'+amount+'** '+random_lacan+'> from '+str(ctx.author)+'!')
          except:
            embed=Embed('Error!',''+giveto.mention+' has received '+str(ctx.author)+'\'s **'+amount+'** '+random_lacan+', but they have their DMs turned off so I couldn\'t Direct message '+giveto.mention+'.', 'warning')
        await embed.send(ctx)
        try:
            await ctx.message.delete()
        except:
            pass
        return
        
def setup(client):
    client.add_cog(Command(client))