'''Shows the stats of a NT team.'''

from discord.ext import commands
from packages.utils import Embed, ImproperType
from packages.nitrotype import Team, Racer
import json, os, requests
from datetime import datetime
from mongoclient import DBClient
class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def team(self, ctx, team_name=''):
        #return await ctx.send('This command is currently under maintenance. The developers will try to get it up again as soon as possible. In the meantime feel free to use `n.help` to get the other commands. Thank you for your understanding!')
        #thedata = json.loads(requests.get('https://test-db.nitrotypers.repl.co', data={'key': os.getenv('DB_KEY')}).text)
        dbclient = DBClient()
        collection = dbclient.db.NT_to_discord
        thedata = await dbclient.get_array(collection, {})
        print(thedata)
        if team_name == '': 
            async for player in thedata:
                if player['userID'] == str(ctx.author.id):
                    racer = await Racer(player['NTuser'])
                    tname = ''.join(list(racer.tag)[1:-1])
                    team = await Team(tname)
                    if tname == '':
                        return await Embed('Error!', 'Couldn\'t find that team', 'warning').send(ctx)
                    break
        else:
            team = await Team(team_name)
        if team.data == {} or team.success == False:
            userid = str(''.join(list(team_name)[3:-1]))
            async for elem in thedata:
                if userid == elem['userID']:
                    racer = await Racer(elem['NTuser'])
                    team_name = racer.tag
                    team = await Team(team_name)
                    if team_name == '':
                        return await Embed('Error!', 'Couldn\'t find that team', 'warning').send(ctx)
                    break
                if str(''.join(list(team_name)[2:-1])) == elem['userID']:
                    racer = await Racer(elem['NTuser'])
                    team_name = racer.tag
                    team = await Team(team_name)
                    if team_name == '':
                        return await Embed('Error!', 'Couldn\'t find that team', 'warning').send(ctx)
                    break
            else:
                async for elem in thedata:
                    if str(team_name) == elem['userID']:
                        racer = await Racer(elem['NTuser'])
                        team_name = racer.tag
                        team = await Team(team_name)
                        if team_name == '':
                            return await Embed('Error!', 'Couldn\'t find that team', 'warning').send(ctx)
                        break
                else:
                    return await Embed('Error!', 'Couldn\'t find that team', 'warning').send(ctx)
        if team.data == {} or team.success == False:
            await Embed('Error!', 'Couldn\'t find that team', 'warning').send(ctx)
            return            

        info = team.info
        results = team.data
        #info section of embed
        embed = Embed(f"[{info['tag']}] {info['name']}", team.tag_and_name, 'race car')
        #'race car')
        createdstamp = info['createdStamp']
        birthday = datetime.fromtimestamp(int(createdstamp))
        teamid = info["teamID"]
        enrollment = info["enrollment"]
        activeperc = info["activePercent"]

        embed.field('Info', f" :busts_in_silhouette: Members: {str(len(results['members']))}\n:id: Team ID: {teamid}\n:eyes: Team Views: {info['profileViews']}\n:birthday: Birthday: {birthday}\n<:team_competitions:800330847915868220> Enrollment: **{enrollment}**\n:bar_chart: Activity Percentage: {activeperc}%\n:hourglass: Last Activity: {team.lastact}\n:pencil: Last Modification: {team.lastmod}")
        #requirements to be able to join/apply for the team
        embed.field('Requirements', f":stopwatch: Min Speed: {info['minSpeed']}\n:checkered_flag: Min Races: {info['minRaces']}")
        #officers/captain of team       
        leaders = f":tools: **{team.captain[1]}**[:link:](https://www.nitrotype.com/racer/{team.captain[0]})\n"
        try:
            for elem in team.leaders:
                if elem[1] is None:
                  leaders += ':man_police_officer: **'+elem[0]+'**[:link:](https://www.nitrotype.com/racer/'+elem[0]+')\n'
                else:
                  leaders += ':man_police_officer: **'+elem[1]+'**[:link:](https://www.nitrotype.com/racer/'+elem[0]+')\n'
        except IndexError as e:
            print(e)
        embed.field('Leaders', leaders)
        otherreqs = info['otherRequirements']
        if otherreqs:
            embed.field('Description', f"{otherreqs}")
        else:
            embed.field('Description', 'No description for this team exists.')
        #team stats
        try:
          embed.field('Stats', f":trophy: **Daily**\n{team.daily_races} races ({round(int(team.daily_speed), 2)} wpm, {round(team.daily_accuracy, 2)}% acc)\n{round(team.daily_points, 2)} points\n:trophy: **Season**\n{team.season_races} races ({round(int(team.season_speed), 2)} wpm, {round(team.season_accuracy, 2)}% acc)\n{round(team.season_points, 2)} points\n:trophy: **All-Time**\n{team.alltime_races} races ({round(int(team.alltime_speed), 2)} wpm, {round(team.alltime_accuracy, 2)}% acc)\n{round(team.alltime_points, 2)} points")
          return await embed.send(ctx)
        except IndexError:
          try:
             embed.field('Stats', f":trophy: **Season**\n{team.season_races} races ({round(int(team.season_speed), 2)} wpm, {round(team.season_accuracy, 2)}% acc)\n{round(team.season_points, 2)} points\n:trophy: **All-Time**\n{team.alltime_races} races ({round(int(team.alltime_speed), 2)} wpm, {round(team.alltime_accuracy, 2)}% acc)\n{round(team.alltime_points, 2)} points")
             return await embed.send(ctx)
          except IndexError:
             try:
                embed.field('Stats', f":trophy: **All-Time**\n{team.alltime_races} races ({round(int(team.alltime_speed), 2)} wpm, {round(team.alltime_accuracy, 2)}% acc)\n{round(team.alltime_points, 2)} points")
                return await embed.send(ctx)
             except IndexError:
                embed.field('Stats', f"No stats could be found!")
        #send the embed
        await embed.send(ctx)
    
def setup(client):
    client.add_cog(Command(client))
