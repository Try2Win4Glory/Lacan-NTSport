'''Reroll The Winner!'''

from discord.ext import commands
from packages.utils import Embed, ImproperType
from mongoclient import DBClient
from discord.utils import get
import random
class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def reroll(self, ctx, messageID: int):
        dbclient = DBClient()
        collection = dbclient.db.giveaways
        dbdata = await dbclient.get_array(collection, {"$and": [{"messageID": messageID}, {"messageID": messageID}]})
        giveaway = dbdata
        try:
            giveaway['ended']
        except:
            embed = Embed('Error!', f'No giveaway found with message ID `{messageID}`', 'warning')
            return await embed.send(ctx)
        if giveaway['ended'] == False:
            embed = Embed('Error!', 'This giveaway hasn\'t ended! Try `n.end` to end the giveaway!', 'warning')
            return await embed.send(ctx)
        channel = get(self.client.get_all_channels(), id=giveaway['channelID'])
        msg = get(await channel.history(limit=1000).flatten(), id=giveaway['messageID'])
        try:
          if ctx.message.channel.id == giveaway['channelID']:
            users = await msg.reactions[0].users().flatten()
            print(users)
            winner = []
            print(winner)

            list_of_lacans = ['<:lacan_economy_1:801006407536607262>','<:lacan_economy_2:801004873612132382>','<:lacan_economy_3:801004873214722079>','<:lacan_economy_4:801004868126113822>','<:lacan_economy_5:801004868348936203>','<:lacan_economy_6:801004863433605160>','<:lacan_economy_7:801004870643220481>','<:lacan_economy_8:801004872820457483>','<:lacan_economy_9:801004872417804298>','<:lacan_economy_10:801004872811413514>']
            random_lacan = random.choice(list_of_lacans)
            #lacan = ctx.message.get_member("713352863153258556")
            #reaction = random_lacan
            winner = random.choice(users)
            for winner in ['713352863153258556']:
              print('1')
              print(winner)
              if winner == '713352863153258556':
                print('wintrue')
                winner = random.choice(users)
              while winner == '713352863153258556':
                  print('2')
                  winner = random.choice(users)
                  continue
              else:
                  print('3')
                  break
            if giveaway['joined'] == []:
                await msg.channel.send(f':weary:No one won\n{msg.jump_url}:weary:')
            else:
                await msg.channel.send(f':tada:The new winner is {winner.mention}{msg.jump_url} ! :tada:')
          else:
            print('wrong server')
            return
                
        except KeyError:
            await msg.channel.send(f'No one won because no one joined!\n{msg.jump_url}')

def setup(client):
    client.add_cog(Command(client))