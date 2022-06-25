'''Let the raffle begin!'''
from discord.ext import commands
import json, random
class Command(commands.Cog):
    def __init__(self, client):
        self.client = client
    def write_json(self, data, filename='tickets.json'): 
        with open(filename,'w') as f: 
            json.dump(data, f, indent=4) 
    @commands.command()
    async def draw(self, ctx):
        if ctx.author.id not in [505338178287173642, 990119147826454628]:
            return await ctx.send('Access DENIED!')
        with open('tickets.json') as f:
            data = json.load(f)
            tickets = len(data['tickets'])
            if tickets-1 < 0:
                return await ctx.send('There aren\'t any tickets bought :man_facepalming:')
            winner = random.randint(0, tickets-1)
        await ctx.send(f'The winner is <@{data["tickets"][winner]}>!')
def setup(client):
    client.add_cog(Command(client))
