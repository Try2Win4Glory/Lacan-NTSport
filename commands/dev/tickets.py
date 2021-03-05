'''Shows the tickets of a user'''
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
    async def tickets(self, ctx, user:discord.User=None):
        id = ctx.author.id
        if user != None:
            id = user.id
        with open('tickets.json') as f:
            data = json.load(f)
        count = 0
        for ticket in data['tickets']:
            if ticket == id:
                count += 1
        if user != None:
            
            embed=Embed('Tickets', f'{str(user)} has `{str(count)}` tickets!', 'tickets')
            await embed.send(ctx)
            return
            
        embed=Embed('Tickets', f'You have `{str(count)}` tickets!', 'tickets')
        await embed.send(ctx)
        return
        
def setup(client):
    client.add_cog(Command(client))