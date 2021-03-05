'''Look Through The Cars You Bought'''
from discord.ext import commands
from packages.utils import Embed, ImproperType
from mongoclient import DBClient
from discord import Reaction, User
from asyncio.exceptions import TimeoutError
class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def cars(self, ctx, user=None):
        dbclient = DBClient()
        collection = dbclient.db.pointsdb
        dbdata = await dbclient.get_array(collection, {'$and': [{'userid': str(ctx.author.id)}, {'userid': str(ctx.author.id)}]})
        async for d in dbdata:
            data = d
            break
        page = 0
        def check(reaction:Reaction, user:User):
            return user.id == ctx.author.id
        embed = Embed('Cars You Own!', 'The cars you bought with lacans!')
        embed.field('Equipped Car!', data['equipped']['car'])
        embed.image('https://www.nitrotype.com/cars/'+data['equipped']['img'].replace('small', 'large'))
        embed.footer('You can buy cars or equip cars using n.buy or n.equip!')
        message = await ctx.send(embed=embed.default_embed())
        await message.add_reaction('🔄')
        while True:
            try:
                reaction, user = await self.client.wait_for('reaction_add', timeout=120, check=check)
            except TimeoutError:
                break
            embed = Embed('Cars You Own!', 'The cars you bought with lacans!')
            embed.field(f'Car Index {page+1}', data["cars"][page]["car"])
            embed.image(f"https://www.nitrotype.com/cars/{data['cars'][page]['img'].replace('small', 'large').strip()}")
            await message.remove_reaction(reaction, user)
            await message.edit(embed=embed.default_embed())
            page += 1
            if page >= len(data['cars']):
                page = 0
def setup(client):
    client.add_cog(Command(client))