'''Nitrotype Leaderboards'''

from discord.ext import commands
from packages.utils import Embed, ImproperType
import requests, json
from discord import Reaction, User
from packages.misc import format_number as fn
from asyncio.exceptions import TimeoutError
class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    def create_embed(self, starting, ending):
        data = requests.get('https://NTLB.adl212.repl.co/data.json').text
        data = json.loads(data)
        players = []
        points = []
        speeds = []
        accuracys = []
        races = []
        displays = []
        cars = []
        for elem in data['users']:
            players.append(elem['username'])
            points.append(elem['points'])
            speeds.append(round(elem['speed']))
            accuracys.append(round(elem['accuracy']))
            races.append(elem['races'])
            displays.append(elem['displayname'])
            cars.append(elem['carID'])
        
        zipped_lists = zip(points, players)
        sorted_zipped_lists = sorted(zipped_lists, reverse=True)
        sortedlb = [element for _, element in sorted_zipped_lists]

        zipped_lists = zip(points, displays)
        sorted_zipped_lists = sorted(zipped_lists, reverse=True)
        sorteddisplay = [element for _, element in sorted_zipped_lists]

        zipped_lists = zip(points, players)
        sorted_zipped_lists = sorted(zipped_lists, reverse=True)
        sortedusername = [element for _, element in sorted_zipped_lists]

        zipped_lists = zip(points, cars)
        sorted_zipped_lists = sorted(zipped_lists, reverse=True)
        sortedcars = [element for _, element in sorted_zipped_lists]

        zipped_lists = zip(points, races)
        sorted_zipped_lists = sorted(zipped_lists, reverse=True)
        sortedraces = [element for _, element in sorted_zipped_lists]

        zipped_lists = zip(points, speeds)
        sorted_zipped_lists = sorted(zipped_lists, reverse=True)
        sortedspeeds = [element for _, element in sorted_zipped_lists]

        zipped_lists = zip(points, accuracys)
        sorted_zipped_lists = sorted(zipped_lists, reverse=True)
        sortedaccuracy = [element for _, element in sorted_zipped_lists]

        zipped_lists = zip(points, points)
        sorted_zipped_lists = sorted(zipped_lists, reverse=True)
        sortedpoints = [element for _, element in sorted_zipped_lists]
    
        embed = Embed('Nitrotype Leaderboards!', f'{str(starting)} - {str(ending)} Players in Our Database!')
        links = []
        x = starting
        for display in sorteddisplay[starting:ending]:
            links.append(f'[:link:](https://www.nitrotype.com/racer/{sortedlb[x]})')
            x = x + 1
        points = []
        for point in sortedpoints[starting:ending]:
            points.append(fn(point))
        embed.field('Racers', '\n'.join(sorteddisplay[starting:ending]))

        embed.field('Points', '\n'.join(points))
        embed.field('Links', '\n'.join(links))
        return embed
    @commands.command()
    async def ntlb(self, ctx):
        page = 0
        starting = 0
        ending = 10
        embed = self.create_embed(starting, ending)
        message = await ctx.send(embed=embed.default_embed(), content=None)
        await message.add_reaction('⬅️')
        await message.add_reaction('➡️')
        def check(reaction:Reaction, user:User):
            return user.id == ctx.author.id
        while True:
            try:
                reaction, user = await self.client.wait_for('reaction_add', timeout=120, check=check)
            except TimeoutError:
                break
            else:
                if str(reaction) == '⬅️':
                    if page == 0:
                        pass
                    else:
                        page = page - 1
                    
                    await message.remove_reaction(reaction, user)
                    await message.edit(embed=self.create_embed(starting+10*page, ending+10*page).default_embed(), content=None)
                if str(reaction) == '➡️':
                    try:
                        page = page + 1
                        await message.remove_reaction(reaction, user)
                        await message.edit(embed=self.create_embed(starting+10*page, ending+10*page).default_embed(), content=None)
                    except:
                        await message.remove_reaction(reaction, user)
                        embed = Embed('Oops!', 'You\'ve reached the end!')
                        await message.edit(embed=embed.default_embed(), content=None)
                else:
                    await message.remove_reaction(reaction, user)
def setup(client):
    client.add_cog(Command(client))