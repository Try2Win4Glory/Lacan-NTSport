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
            racer = await get_username(str(ctx.author.id))
        else:
            racer = await get_username(user)
        try:
            if racer[0] == True:
                racer = racer[1]
            else:
                return await racer[1].send(ctx)
        except:
            embed = Embed('Error!', 'Couldn\'t find that user', 'warning')
            return await embed.send(ctx)
        if racer.membership == 'basic':
          embed = Embed(f'{racer.name}\'s stats', racer.tag_and_name, 'race car', 0xfc3503)
          embed.footer(f'{racer.name.title()} has a Standard account. \nThese stats are brought to you by adl212, Try2Win4Glory and Joshua_Kim.', 'https://media.discordapp.net/attachments/719414661686099993/765110312482766919/NT_Server_Halloween_Logo_2020_GIF.gif')

          if (ctx.author.id) not in [505338178287173642, 637638904513691658, 396075607420567552]:
              embed.footer(f'{racer.name.title()} has a Standard account. \nThese stats are brought to you by adl212, Try2Win4Glory and Joshua_Kim.\nBecome a premium 💠 member today!', 'https://media.discordapp.net/attachments/719414661686099993/765110312482766919/NT_Server_Halloween_Logo_2020_GIF.gif')
          else:
              embed.footer('Discord user '+str(ctx.author.name + '#' + ctx.author.discriminator)+' is a developer of this bot.', 'https://media.discordapp.net/attachments/719414661686099993/765490220858081280/output-onlinepngtools_32.png')

        elif racer.membership == 'gold':
          embed = Embed(f'{racer.name}\'s stats', racer.tag_and_name, 'race car', 0xfac32d)
          embed.footer(f'{racer.name.title()} has a Gold account. \nThese stats are brought to you by adl212, Try2Win4Glory and Joshua_Kim.', 'https://cdn.discordapp.com/attachments/719414661686099993/754971786231283712/season-callout-badge.png')

          if (ctx.author.id) not in [505338178287173642, 637638904513691658, 396075607420567552]:
              embed.footer(f'{racer.name.title()} has a Gold account. Become a premium 💠 member today! \nThese stats are brought to you by adl212, Try2Win4Glory and Joshua_Kim.', 'https://media.discordapp.net/attachments/719414661686099993/765110312482766919/NT_Server_Halloween_Logo_2020_GIF.gif')
          else:
              embed.footer('Discord user '+str(ctx.author.name + '#' + ctx.author.discriminator)+' is a developer of this bot.', 'https://media.discordapp.net/attachments/719414661686099993/765490220858081280/output-onlinepngtools_32.png')
        
        embed.thumbnail(racer.car)

        embed.field('General Info', f':small_blue_diamond: User: **{racer.username}**\n :small_blue_diamond: Level: **{racer.level}**\n:small_blue_diamond: Experience: **{racer.experience}** \n:small_blue_diamond: **{racer.country}**\n:small_blue_diamond: Views: **{racer.views}** \n :small_blue_diamond: Achievement points: **{racer.points}**\n:small_blue_diamond: Joined: **{racer.created}**')

        embed.field('Speed', f':stopwatch: Average: **{racer.wpm_average}**\n:stopwatch: Highscore: **{racer.wpm_high}**')

        embed.field('Races', f':checkered_flag: **{racer.races}** races \n:first_place: **{racer.first}** (**{racer.first_perc})%**\n:second_place: **{racer.second}** (**{racer.second_perc})%**\n:third_place: **{racer.third}** (**{racer.third_perc})%**')

        embed.field('Cars', f':race_car: **{racer.cars_owned}** owned\n:race_car: **{racer.cars_sold}** sold\n:race_car: **{racer.cars_total}** total\n:race_car: Driving: **{racer.current_car}**')

        embed.field('Nitros', f':zap: **{racer.nitros}** owned\n:zap: **{racer.nitros_used}** used\n:zap: **{racer.nitros_total}** total')
        '''
        embed.field('Money', f':dollar: **{racer.money}**\n:dollar: **{racer.money_spent}** spent\n:dollar: **{racer.money_total}** total')
        '''
        try:
            embed.field('Season Leaderboard', f':trophy: **{fn(racer.season_races)}** races\n :trophy: **{fn(racer.season_pre["played"])}** errors \n :trophy: **{fn(racer.season_pre["errs"])}** words\n :trophy: **{str(round(racer.season_speed, 2))}** wpm\n :trophy: **{str(round(racer.season_accuracy, 2))}**% accuracy')
        except:
            pass
        try:
            embed.field('Daily Leaderboard', f':trophy: **{fn(racer.daily_races)}** races\n :trophy: **{fn(racer.daily_pre["played"])}** errors \n :trophy: **{fn(racer.daily_pre["errs"])}** words\n :trophy: **{str(round(racer.daily_speed, 2))}** wpm\n :trophy: **{str(round(racer.daily_accuracy, 2))}**% accuracy')
        except:
            pass

        embed.field('Settings', f':gear: Friends: {racer.friend_reqs_allowed}\n:gear: Team invite: {racer.looking_for_team}')


        await embed.send(ctx)
    
def setup(client):
    client.add_cog(Command(client))