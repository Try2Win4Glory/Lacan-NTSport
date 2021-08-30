'''Check the live leaderboard if the competition is still running or check the results after it ended.'''
from discord.ext import commands
import nitrotype, discord
from packages.utils import Embed, ImproperType
class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command(aliases=['lb', 'leaderboards', 'lbs'])
    async def leaderboard(self, ctx, compid, category=None):
        '''#return await ctx.send('Looks like comps are currently under maintenance! Sorry, trying to bring them up again as soon as possible. In the meantime, make sure to use our other commands in `n.help`!')
        if category not in ['races', 'speed', 'points', 'accuracy']:
            embed=Embed('Invalid category!', f'Make sure to use a valid category for this command!\nValid categorys are `races`, `points`, `speed` or `accuracy`.\n\n__How do I use a category?__\nJust simply run one of these commands:\n`n.lb {compid} races`\n`n.lb {compid} points`\n`n.lb {compid} speed`\n`n.lb {compid} accuracy`\n\n*Please note that commands might take a while to compile!*', 'warning')
            #embed = Embed('Error!', 'The only categories for competitions are: `races`, `speed`, `accuracy`, or `points`.')
            return await embed.send(ctx)
        else:
            await nitrotype.update_comp(compid)
            lb = await nitrotype.l(compid, category=category)
            embed = discord.Embed(
                title='Live Leaderboards',
                description='This is where you can view everyone\'s progress during the competition!',
                color=0x15E700
            )
            usernames = []
            races = []
            for stat in lb[1]:
                #if stat[1] == '':
                usernames.append(f'{stat[0]}\n')
                #else:
                    #usernames.append(f'{stat[1]}\n')
                races.append(str(round(stat[2], 2)))
            usernames = ''.join(usernames)
            races = '\n'.join(races)
            embed.add_field(
                name='Team Members',
                value=usernames
            )
            embed.add_field(
                name=category,
                value=races
            )
            await ctx.send(embed=embed)'''
        try:
            await nitrotype.update_comp(compid)
        except:
            embed = Embed('Competition Error', f'No Competition with the Competition ID `{compid}` exists. Please check again if you are actually using the correct ID.', 'x')
            return await embed.send(ctx)
        if category not in ['races', 'speed', 'points', 'accuracy']:
            embed = Embed('Competition Leaderboard', f'View the Leaderboard of the Competition `{compid}` by clicking **[here](https://nitrotype-competitions.try2win4code.repl.co/comp/{compid})**.', 'medal')
            return await embed.send(ctx)
        else:
            # Replace the category to get the correct link
            if category == 'speed':
                category = 'wpm'
            if category == 'accuracy':
                category = 'acc'
            embed = Embed(f'Competition {category} Leaderboard', f'View the __{category}__ Leaderboard of the Competition `{compid}` by clicking **[here](https://nitrotype-competitions.try2win4code.repl.co/comp/{compid}?sortby={category})**.', 'medal')
            return await embed.send(ctx)
def setup(client):
    client.add_cog(Command(client))
