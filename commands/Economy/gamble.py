'''Gamble Against The Corrupt Casino'''

from discord.ext import commands
from packages.utils import Embed
from mongoclient import DBClient
import random, math
class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def gamble(self, ctx, amount):

        list_of_lacans = ['<:lacan_economy_1:801006407536607262>','<:lacan_economy_2:801004873612132382>','<:lacan_economy_3:801004873214722079>','<:lacan_economy_4:801004868126113822>','<:lacan_economy_5:801004868348936203>','<:lacan_economy_6:801004863433605160>','<:lacan_economy_7:801004870643220481>','<:lacan_economy_8:801004872820457483>','<:lacan_economy_9:801004872417804298>','<:lacan_economy_10:801004872811413514>']
        random_lacan = random.choice(list_of_lacans)

        dbclient = DBClient()
        collection = dbclient.db.pointsdb
        data = await dbclient.get_array(collection, {'$and': [{'userid': str(ctx.author.id)}, {'userid': str(ctx.author.id)}]})
        user = data
        old = user.copy()
        if int(amount) <= 5:
            embed = Embed('Gambling Too Little!', f'We the casino want you to gamble more than `5` '+random_lacan+' at a time.', 'warning')
            return await embed.send(ctx)
        try:
            if user['userid'] == str(ctx.author.id):
                if int(user['points']) < int(amount):
                    embed = Embed('<a:error:800338727645216779>  Error!', 'So you want negative '+random_lacan+' if you lose right? <a:keka:800338138802946098>')
                    return await embed.send(ctx)
        except:
            embed = Embed('<a:error:800338727645216779>  Error!', 'You haven\'t won a guess game yet! You have to win a game and will then be able to gamble!')
            return embed.send(ctx)
        numbers = [1, 2, 3, 4, 5, 6]
        if ctx.author.id not in [637638904513691658, 505338178287173642, 396075607420567552]:
            bot_rolled = random.choices(numbers, [1, 1, 1, 2, 2, 3])[0]
            user_rolled = random.choices(numbers, [1, 1, 1, 1, 1, 1])[0]
        else:
            bot_rolled = random.choices(numbers, [1, 0, 0, 0, 0, 0])[0]
            user_rolled = random.choices(numbers, [0, 1, 1, 1, 1, 1])[0]
        if bot_rolled >= user_rolled:
            embed = Embed('You Lost!', 'Gambling Results', 'weary', color=0xff0000)
            embed.field('Your Roll', f'\n`{str(user_rolled)}`\n')
            embed.field('Bot Roll', f'\n`{str(bot_rolled)}`\n')
            embed.field('Loss', f'You lost {str(amount)} '+random_lacan+'!', inline=False)
            user['points'] -= int(amount)
            await embed.send(ctx)
        if bot_rolled < user_rolled:
            embed = Embed('You Won!', 'Gambling Results', 'tada', color=0x00ff00)
            embed.field('Your Roll', f'\n`{str(user_rolled)}`\n')
            embed.field('Bot Roll', f'\n`{str(bot_rolled)}`\n')
            embed.field('Winnings', f'You won {str(math.floor(int(amount)/2)+(user_rolled-bot_rolled))} '+random_lacan+'!', inline=False)
            user['points'] += math.floor(int(amount)/2)+(user_rolled-bot_rolled)
            await embed.send(ctx)
        await dbclient.update_array(collection, old, user)
        
    
def setup(client):
    client.add_cog(Command(client))