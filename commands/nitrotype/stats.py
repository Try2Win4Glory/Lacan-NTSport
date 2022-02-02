'''Shows the stats of a nitrotype user'''

from discord.ext import commands
from packages.utils import Embed, ImproperType
from packages.nitrotype import Racer
from packages.misc import format_number as fn
import requests
import json
import os
from mongoclient import DBClient
from nitrotype import get_username
class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def stats(self, ctx, user=None):
        #return await ctx.send('This command is currently under maintenance. The developers will try to get it up again as soon as possible. In the meantime feel free to use `n.help` to get the other commands. Thank you for your understanding!')
        #data = json.loads(requests.get('https://test-db.nitrotypers.repl.co', data={'key': os.getenv('DB_KEY')}).text)
        if user == None:
            try:
              racer = await get_username(str(ctx.author.id))
            except:
              embed=Embed('Error!', 'Couldn\'t find that user', 'warning')
        else:
            racer = await get_username(user, bypass=True)
        try:
            if racer[0] == True:
                racer = racer[1]
            else:
                return await racer[1].send(ctx)
        except:
            embed = Embed('Error!', 'Couldn\'t find that user', 'warning')
            return await embed.send(ctx)
        
        if racer.membership == 'basic':
          embed = Embed(f'{racer.username} ({racer.name})\'s stats', racer.tag_and_name, 'race car', 0xfc3503)
          embed.footer(f'{racer.name.title()} has a Standard account. \nThese stats are brought to you by adl212, Try2Win4Glory and Joshua_Kim.', 'https://media.discordapp.net/attachments/719414661686099993/765110312482766919/NT_Server_Halloween_Logo_2020_GIF.gif')

          if (ctx.author.id) not in []:
              embed.footer(f'{racer.name.title()} has a Standard account.\nThese stats are brought to you by adl212 and Try2Win4Glory','https://media.discordapp.net/attachments/719414661686099993/765110312482766919/NT_Server_Halloween_Logo_2020_GIF.gif')
          else:
              embed.footer('Discord user '+str(ctx.author.name + '#' + ctx.author.discriminator)+' is a developer of this bot.', 'https://media.discordapp.net/attachments/719414661686099993/765490220858081280/output-onlinepngtools_32.png')

        elif racer.membership == 'gold':
          embed = Embed(f'{racer.username} ({racer.name})\'s stats', racer.tag_and_name, 'race car', 0xfac32d)
          embed.footer(f'{racer.name.title()} has a Gold account. \nThese stats are brought to you by adl212, Try2Win4Glory and Joshua_Kim.', 'https://cdn.discordapp.com/attachments/719414661686099993/754971786231283712/season-callout-badge.png')

          if (ctx.author.id) not in []:
              embed.footer(f'{racer.name.title()} has a Gold account. Become a premium 💠 member today! \nThese stats are brought to you by adl212 and Try2Win4Glory.','https://media.discordapp.net/attachments/719414661686099993/765110312482766919/NT_Server_Halloween_Logo_2020_GIF.gif')
          else:
              embed.footer('Discord user '+str(ctx.author.name + '#' + ctx.author.discriminator)+' is a developer of this bot.', 'https://media.discordapp.net/attachments/719414661686099993/765490220858081280/output-onlinepngtools_32.png')
        
        '''try:
          if racer.car == 'https://www.nitrotype.com/cars/17_large_1.png' and racer.car.id != '17':
            pass
            print(racer.car.name)
          else:
            embed.thumbnail(racer.car)
            print(racer.car.name)
        except:
          embed.thumbnail(racer.car)'''
        '''if racer.car == 'https://www.nitrotype.com/cars/110_large_1.png':
            print('Minnie the coper alarm')
        else:'''
        #embed.image(f'https://nitrotype.com{racer.trail_image}')
        embed.thumbnail(racer.car)


        #print(racer.name+' is from '+racer.country)

        if racer.lifetime_gold:
          gold = 'Lifetime'
        elif racer.newdata["membership"] != "basic":
          gold = 'Yearly'
        else:
          gold = 'Basic'
        
        header = '-------------------'
        space = '       '
        if racer.trailname != 'None':
          trail_created = racer.newdata['loot'][0]['createdStamp']
        else:
          pass
        
        created = racer.newdata['createdStamp']
        hammercreated = f'<t:{created}:f>'

        races = racer.newdata['racesPlayed']
        nitros = racer.newdata['nitrosUsed']
        nitrosperrace = (races)/(nitros)
        roundednitrosperrace = round(nitrosperrace, 2)

        embed.field(f':race_car:{space}Racing', f'{header}:checkered_flag: **{racer.races}**\n:timer: **{racer.longest_session}**\n:stopwatch: Average: **{racer.wpm_average}**\n:stopwatch: High: **{racer.wpm_high}**')

        embed.field(f'<:info:938430460227358771>{space}Useful', f'{header}:diamond_shape_with_a_dot_inside: Level **{racer.level}**\n:diamond_shape_with_a_dot_inside: **{racer.experience} XP**\n:eyes: **{racer.views}**\n:tada: {hammercreated}')

        if gold == 'Lifetime':
          goldemoji = '<:old_nt_gold:938434881933938699>'
        elif gold == 'Yearly':
          goldemoji = '<:nt_gold:861944319102418944>'
        else:
          goldemoji = '<:nt_basic:868772526321438740>'

        if gold != 'Yearly':
          embed.field(f':medal:{space}Gold Info', f'{header}{goldemoji} `{gold}`')
        else:
          embed.field(f':medal:{space}Gold Info', f'{header}{goldemoji} `{gold}`\n{goldemoji} Expires: <t:{racer.gold_until}:d>\n{goldemoji} Purchased: {racer.last_purchase}')
          

        embed.field(f':police_car:{space}Cars', f'{header}:blue_car: Owned: {racer.cars_owned}\n:blue_car: ID: `{racer.carid}`')

        if racer.trailname != 'None':
          embed.field(f':star: {space}Trails', f'{header}🌠 **{racer.trailname}**\n🌠 **{racer.trail_rarity}**\n🌠 <t:{trail_created}:d> <t:{trail_created}:t>')
        else:
          pass

        embed.field(f'<:nitro:938450286488457327>{space}Nitros', f'{header}:zap: **∞** owned\n:zap: **{racer.nitros_used}** used\n:zap: **{roundednitrosperrace}**/:checkered_flag:')

        embed.field(f':gear:{space}Add / Invite', f'{header}\n:bust_in_silhouette: Friends: {racer.friend_reqs_allowed}\n:bust_in_silhouette: Teams: {racer.looking_for_team}')



        #embed.field('__General Info__', f':small_blue_diamond: Level: **{racer.level}**\n:small_blue_diamond: XP: **{racer.experience}**\n:eyes: **{racer.views}** \n :birthday: **{racer.created}** \n <:nt_gold:861944319102418944> **{"Lifetime" if racer.lifetime_gold else "Gold" if racer.newdata["membership"] != "basic" else "Basic"}**', inline=True)

        #Achievement points: **{racer.points}**

        #embed.field('\n\u200b', '\n\u200b')

        #embed.field('__Speed__', f':stopwatch: Avg: **{racer.wpm_average}**\n:stopwatch: High: **{racer.wpm_high}**')

        #embed.field('\n\u200b', '\n\u200b')

        #embed.field('__Races__', f':checkered_flag: **{racer.races}**\n:timer: **{racer.longest_session}**', inline=True)

        #embed.field('\n\u200b', '\n\u200b')

        #embed.field('__Cars__', f':race_car: **{racer.cars_owned}** owned\n:race_car: **{racer.cars_sold}** sold\n:race_car: **{racer.cars_total}** total')

        #embed.field('\n\u200b', '\n\u200b')
        
        #if racer.trailname != 'None':
            #embed.field('__Trails__', f'🌠 Name: **{racer.trailname}**\n🌠 Asset Key: **{racer.trail_asset}**\n🌠 Rarity: **{racer.trail_rarity}**\n🌠 Created: **{racer.trail_created}**\n🌠 Image: [Link](https://nitrotype.com{racer.trail_image})')
        #else:
            #pass
        #embed.field('\n\u200b', '\n\u200b')

        #embed.field('__Nitros__', f':zap: **{racer.nitros}** owned\n:zap: **{racer.nitros_used}** used\n:zap: **{racer.nitros_total}** total')

        #embed.field('\u200b', '\u200b')

        '''
        embed.field('__Money__', f':dollar: **{racer.money}**\n:dollar: **{racer.money_spent}** spent\n:dollar: **{racer.money_total}** total')
        '''

        try:
            embed.field('__Daily__', f':trophy: **{fn(racer.daily_races)}** races')
        except:
            pass

        try:
            embed.field('__Season__', f':trophy: **{fn(racer.season_races)}** races')
        except:
            pass

        #embed.field('__Settings__', f':gear: Friends: {racer.friend_reqs_allowed}\n:gear: Team invite: {racer.looking_for_team}')


        await embed.send(ctx)
    
def setup(client):
    client.add_cog(Command(client))
