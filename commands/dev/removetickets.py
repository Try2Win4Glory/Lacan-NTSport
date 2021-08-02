'''Remove tickets from a mentioned user'''
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
    async def removetickets(self, ctx, user:discord.User=None, amount=None):
        if ctx.author.id not in [505338178287173642]:
            return await ctx.send('Even the owner can\'t run the command and you think you can???')
        if user == None:
            return await ctx.send('You didn\'t give a user!')
        if amount == None:
            return await ctx.send('You didn\'t give an amount of raffle tickets to add!')
        with open('tickets.json') as f:
            data = json.load(f)
        if amount == 'all':
            count = data['tickets'].count(user.id)
        else:
            count = int(amount)
        for x in range(count):
            data['tickets'].remove(user.id)
        self.write_json(data)
        #return await ctx.send(f'Deleted {str(amount)} tickets from {str(user)}\'s tickets!')
        embed=Embed('Success!', f'Deleted `{str(amount)}` tickets from {str(user)}\'s tickets!', 'tickets')
        await embed.send(ctx)
def setup(client):
    client.add_cog(Command(client))
