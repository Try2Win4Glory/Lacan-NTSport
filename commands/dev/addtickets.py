'''Add tickets to a user!'''
from discord.ext import commands
import json, discord
from packages.utils import Embed, ImproperType

class Command(commands.Cog):
    def __init__(self, client):
        self.client = client
    def write_json(self, data, filename='tickets.json'): 
        with open(filename,'w') as f: 
            json.dump(data, f, indent=4) 
    @commands.command()
    async def addtickets(self, ctx, user:discord.User=None, amount=None):
        if ctx.author.id not in [505338178287173642]:
            return await ctx.send('Access DENIED!')
        if user == None:
            return await ctx.send('You didn\'t give a user!')
        if amount == None:
            return await ctx.send('You didn\'t give an amount of raffle tickets to add!')
        with open('tickets.json') as f:
            data = json.load(f)
        for ticket in range(int(amount)):
            data['tickets'].append(user.id)
        self.write_json(data)
        #await ctx.send(f'Gave user {str(user)} {str(amount)} tickets!')
        embed=Embed('Success!', f'{str(user)} has received `{str(amount)}` tickets!', 'tickets')
        await embed.send(ctx)
def setup(client):
    client.add_cog(Command(client))
