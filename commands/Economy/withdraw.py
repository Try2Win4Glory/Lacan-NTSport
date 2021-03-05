'''Beg The Devs for NT cash'''

from discord.ext import commands
from packages.utils import Embed, ImproperType
from mongoclient import DBClient
from discord.utils import get
from packages.nitrotype import Racer
import discord, random
from cooldowns.withdraw import rateLimit, cooldown_add
class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def withdraw(self, ctx, *amount):
        embed=Embed('Oops!', 'It looks like you discovered a deleted command!\nThe `withdraw` command got deleted on Feburary 6th 2021. Lacans withdrawn after that point will **NOT** be converted into NT Cash anymore.\n\n*For more details, please make sure to read the [announcement](https://discord.com/channels/763774963102122014/763791477888647188/807743177352151111) in the [support server](https://discord.gg/Wj96Ehg).*', 'cry')
        return await embed.send(ctx)
        #return await ctx.send('This command is currently under maintenance. The developers will try to get it up again as soon as possible. In the meantime feel free to use `n.help` to get the other commands. Thank you for your understanding!')

        list_of_lacans = ['<:lacan_economy_1:801006407536607262>','<:lacan_economy_2:801004873612132382>','<:lacan_economy_3:801004873214722079>','<:lacan_economy_4:801004868126113822>','<:lacan_economy_5:801004868348936203>','<:lacan_economy_6:801004863433605160>','<:lacan_economy_7:801004870643220481>','<:lacan_economy_8:801004872820457483>','<:lacan_economy_9:801004872417804298>','<:lacan_economy_10:801004872811413514>']
        random_lacan = random.choice(list_of_lacans)

        if str(ctx.author) in rateLimit:
            embed = Embed('Cooldown!','You are on cooldown. Wait `1` day before running this command again.','alarm clock')
            return await embed.send(ctx)
        if await ImproperType.check(ctx): return
        
        if int(amount) < 100:
            return await Embed('<a:error:800338727645216779>  Error!', f'How can I give you **{str(int(amount)*1000)}** NT cash?  :rofl:').send(ctx)
        dbclient = DBClient()
        collection = dbclient.db.pointsdb
        pointsdata = await dbclient.get_array(collection, {'$and': [{'userid': str(ctx.author.id)}, {'userid': str(ctx.author.id)}]})
        async for d in pointsdata:
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
            embed = Embed('<a:error:800338727645216779>  Error!', 'Unfortunately, you haven\'t won a guess game yet so you have no '+random_lacan+' to withdraw!')
            return await embed.send(ctx)

        try:
            await ctx.message.delete()
            await ctx.author.id.send(f'<a:success:800340618579935233>  You just successfully withdrew **{amount}** '+random_lacan+'. One of the developers will send you **'+str(int(amount*1000))+'** in the next days.')
        except:
            pass
        channels = self.client.get_all_channels()
        channel = get(channels, id=786341458839601243)
        collection = dbclient.db.NT_to_discord
        data = await dbclient.get_big_array(collection, 'registered')
        for elem in data['registered']:
            if str(ctx.author.id) == elem['userID']:
                if elem['verified'] == 'true':
                    racer = Racer(elem['NTuser'])
                    break
                else:
                    embed = Embed('<a:error:800338727645216779>  Error!', 'You\'re not verified yet!')
                    await embed.send(ctx)
                    return
        else:
            embed = Embed('<a:error:800338727645216779>  Error!', 'You\'re not verified yet!')
            await embed.send(ctx)
            return
        if ctx.author.id not in [505338178287173642, 637638904513691658, 396075607420567552]:
              cooldown_add(str(ctx.author))
        embed = Embed('<a:success:800340618579935233>  Success!', '<@'+str(ctx.author.id)+'> has succesfully withdrawn '+' **'+amount+'** '+random_lacan+'.')

        embed1 = discord.Embed(title='Withdraw Log', description=str(ctx.author), color=0xFF6347)
        embed1.add_field(name=''+random_lacan+' Withdrawn', value=f'{amount} '+random_lacan+'')
        embed1.add_field(name='NT Value', value=str(int(amount)*1000))
        embed1.add_field(name='NT link', value=f'[:link:](https://www.nitrotype.com/racer/{racer.username})')
        embed1.add_field(name='User ID', value=f'`{ctx.author.id}`')
        await channel.send(embed=embed1)
        await embed.send(ctx)

        return

def setup(client):
    client.add_cog(Command(client))