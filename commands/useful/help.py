'''Shows a list of commands and their descriptions'''
import discord
from discord.ext import commands
from packages.utils import Embed, ImproperType
from discord import Reaction, User
from asyncio import TimeoutError
from os import listdir
from discord.ext import commands
from packages.utils import Embed, ImproperType

def commands_pagination(current_page):
    global categories
    categories = ['nitrotype', 'Competitions', 'Economy', 'Premium', 'useful' #'dev'
    ]
    category_emoji = {'nitrotype': 'race car',
                      'Competitions': 'trophy',
                      'Economy' : 'coin',
                      'Premium': 'diamond shape with a dot inside',
                      #'spoilers': 'eyes',
                      #'market': 'shopping cart',
                      #'images': 'frame photo',
                      #'server': 'zap',
                      #'giveaways': 'tada',
                      'useful' : 'wrench'
                      #'dev': 'tools'
                      }
    commands = ''
    for command in sorted(listdir(f'./commands/{categories[current_page]}')):
        if command.endswith('.py'):
            file = open(f'./commands/{categories[current_page]}/{command}')
            description = file.readline()[3:-4]
            file.close()

            commands += f'``n.{command[:-3]}`` - {description}\n'

    return Embed(f'Category - {categories[current_page].title()}', commands, category_emoji.get(categories[current_page]))

class Command(commands.Cog):

    def __init__(self, client):
        self.client= client
    
    @commands.command()
    async def help(self, ctx):
        if await ImproperType.check(ctx): return
        page = 0

        def check(reaction:Reaction, user:User):
            return user.id == ctx.author.id

        embed =  commands_pagination(page)
        message = await ctx.send(embed=embed.default_embed(), content=None)
        await message.add_reaction('🔄')

        while True:
            try:
                reaction, user = await self.client.wait_for('reaction_add', timeout=120, check=check)
            except TimeoutError:
                break
            else:
                if str(reaction) == '🔄':
                    if page == len(categories) - 1:
                        page = 0
                    else:
                        page += 1
                    
                    await message.remove_reaction(reaction, user)
                    await message.edit(embed=commands_pagination(page).default_embed(), content=None)
                else:
                    await message.remove_reaction(reaction, user)


        

def setup(client):
    client.add_cog(Command(client))
