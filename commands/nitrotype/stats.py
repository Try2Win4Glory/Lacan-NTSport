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
        embed.thumbnail(racer.car)


        print(racer.name+' is from '+racer.country)

        embed.field('__General Info__', f':small_blue_diamond: Level: **{racer.level}**\n:small_blue_diamond: XP: **{racer.experience}** \n:small_blue_diamond: **{racer.country}**\n:eyes: **{racer.views}** \n :birthday: **{racer.created}** \n <:nt_gold:861944319102418944> **{"Lifetime" if racer.lifetime_gold else "Gold" if racer.newdata["membership"] != "basic" else "Basic"}**', inline=True)

        #Achievement points: **{racer.points}**

        #embed.field('\n\u200b', '\n\u200b')

        embed.field('__Speed__', f':stopwatch: Avg: **{racer.wpm_average}**\n:stopwatch: High: **{racer.wpm_high}**')

        #embed.field('\n\u200b', '\n\u200b')

        embed.field('__Races__', f':checkered_flag: **{racer.races}** \n:first_place: **{racer.first}** (**{racer.first_perc}%**)\n:second_place: **{racer.second}** (**{racer.second_perc}%**)\n:third_place: **{racer.third}** (**{racer.third_perc}%**)', inline=True)

        #embed.field('\n\u200b', '\n\u200b')

        embed.field('__Cars__', f':race_car: **{racer.cars_owned}** owned\n:race_car: **{racer.cars_sold}** sold\n:race_car: **{racer.cars_total}** total\n:race_car: **{racer.current_car}**')

        #embed.field('\n\u200b', '\n\u200b')

        embed.field('__Nitros__', f':zap: **{racer.nitros}** owned\n:zap: **{racer.nitros_used}** used\n:zap: **{racer.nitros_total}** total')

        #embed.field('\u200b', '\u200b')

        '''
        embed.field('__Money__', f':dollar: **{racer.money}**\n:dollar: **{racer.money_spent}** spent\n:dollar: **{racer.money_total}** total')
        '''
        try:
            embed.field('__Daily__', f':trophy: **{fn(racer.daily_races)}** races\n :trophy: **{fn(racer.daily_pre["errs"])}** errors \n :trophy: **{fn(racer.daily_pre["typed"])}** words\n :trophy: **{str(round(racer.daily_speed, 2))}** WPM\n :trophy: **{str(round(racer.daily_accuracy, 2))}**% acc')
        except:
            pass

        try:
            embed.field('__Season__', f':trophy: **{fn(racer.season_races)}** races\n :trophy: **{fn(racer.season_pre["errs"])}** errors \n :trophy: **{fn(racer.season_pre["typed"])}** words\n :trophy: **{str(round(racer.season_speed, 2))}** WPM\n :trophy: **{str(round(racer.season_accuracy, 2))}**% acc')
        except:
            pass

        embed.field('__Settings__', f':gear: Friends: {racer.friend_reqs_allowed}\n:gear: Team invite: {racer.looking_for_team}')


        await embed.send(ctx)
    
def setup(client):
    client.add_cog(Command(client))
