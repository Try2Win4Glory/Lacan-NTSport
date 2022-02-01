'''Create your own epic competitions with custom timer.'''
from discord.ext import commands
import nitrotype, discord
import random, time
class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
        
    @commands.command(aliases=['comp', 'comps', 'teamcomp', 'teamcomps'])
    async def competition(self, ctx, team=None, thetime=None, type=None):
        if team == None:
            return await ctx.send('Can you at least give me the Team you want the competition for? (Example: `n.competition SSH 1 h`)')
        if thetime == None:
            return await ctx.send('You didn\'t specify the time left in the competiton. (Example: `n.competition SSH 1 h`)')
        if type == None:
            return await ctx.send('You didn\'t specify if the time was by months, days, hours, or minutes. Make sure to have a space. (Example: `n.competition SSH 1 h`).')
        endcomptime = round(time.time())
        if type == 'mo':
            endcomptime += 2592000*int(thetime)
            await ctx.send(f'The competition will end in {thetime} months. Check the Link down below for Accurate Live Results.')
        if type == 'd':
            endcomptime += 86400*int(thetime)
            await ctx.send(f'The competition will end in {thetime} days. Check the Link down below for Accurate Live Results.')
        if type == 'h':
            endcomptime += 3600*int(thetime)
            await ctx.send(f'The competition will end in {thetime} hours. Check the Link down below for Accurate Live Results.')
        if type == 'm':
            endcomptime += 60*int(thetime)
            await ctx.send(f'The competition will end in {thetime} minutes. Check the Link down below for Accurate Live Results.')
        if type not in ['mo', 'd', 'h', 'm']:
            await ctx.send('You can use `mo` for month, `d` for day, `h` for hour, `m` for minutes.')
            return
        f = open('usedids', 'a+')
        ids = f.readlines()
        while True:
            compid = ''
            for x in range(8):
                compid += str(random.randint(0, 9))
            if compid+'\n' in ids:
                continue
            else:
                break
        f.write(compid+'\n')
        team = team.upper()
        await nitrotype.create_comp(team, compid, endcomptime, ctx.author.id)
        embed = discord.Embed(
            title=':white_check_mark:  Competition Created!',
            description=f'The competition for Team **{team}** ({thetime}{type}) has been created. Check **[this](https://nitrotype-competitions.try2win4code.repl.co/comp/{compid})** link to see the live leaderboards!',
            color=0x15E700
        )
        embed.add_field(name="Competition ID", value=f'`{compid}`')
        embed.set_footer(text="Don't lose your competition ID! You need it to check results!")
        await ctx.send(embed=embed)
    
def setup(client):
    client.add_cog(Command(client))
