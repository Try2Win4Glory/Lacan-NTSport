'''End your competitions earlier than you said when running the command.'''
from discord.ext import commands
import nitrotype, discord, json
import shutil, requests
from datetime import datetime
from compsmongo import DBClient
from packages.utils import Embed
class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    @commands.command()
    async def endcomp(self, ctx, compid):
        await nitrotype.update_comp(compid)
        dbclient = DBClient()
        collection = dbclient.db['test']
        data = await dbclient.get_array(collection, {'$and': [{'compid': compid}, {'compid': compid}]})
        async for d in data:
            data = d
            old = data.copy()
        data = data
        other = data['other']
        if other['ended'] == True:
            embed = Embed('Error!', 'You already ended the comp before!')
            return await embed.send(ctx)
        if ctx.author.id != other['author'] and ctx.author.id not in [505338178287173642]:
            embed = Embed("Bruh Alert", "Yes thank you for trying to delete someone **else\'s** competition!", "warning")
            
            return await embed.send(ctx)
        embed = discord.Embed(title=":white_check_mark:  Sucess!", description=f"You have succesfully ended the competition ***manually*** for Team **{other['team']}** and Comp ID `{compid}`. View the results **[here](https://nitrotype-competitions.try2win4code.repl.co/comp/{compid})**!")
        date = other['endcomptime']
        timestamp = datetime.fromtimestamp(date)
        embed.set_footer(text=f"This competition was scheduled to end at {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        await ctx.send(embed=embed)
        '''lb = await nitrotype.l(str(compid))
        embed = discord.Embed(
            title='Competition results',
            description='This is where you can view everyone\'s progress during the competition!',
            color=0x15E700
        )
        usernames = []
        races = []
        for stat in lb[1]:
            if stat[1] == '':
                usernames.append(f'{stat[0]}\n')
            else:
                usernames.append(f'{stat[1]}\n')
            races.append(str(stat[2]))
        usernames = ''.join(usernames)
        races = '\n'.join(races)
        embed.add_field(
            name='Team Members',
            value=usernames
        )
        embed.add_field(
            name="Races",
            value=races
        )
        user = await self.client.fetch_user(other['author'])
        try:
            await user.send(embed=embed)
            await user.send('Your competition has ended! Comp ID: `'+compid+'`.  Check out the other categories of your competition by doing `n.lb '+compid+'` and adding `speed`, `accuracy`, `races`, or `points`. Ex: `n.lb '+compid+' points`')
        except:
            pass'''
          
          
        
        
        requests.post('https://backupcomps.adl212.repl.co/backupcomp', data={"id": compid, "comp_data": json.dumps(data['players'])})
        other['ended'] = True
        await dbclient.update_array(collection, old, data)
def setup(client):
    client.add_cog(Command(client))
