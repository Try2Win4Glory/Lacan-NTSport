'''Is The Account A Bot?'''

from discord.ext import commands
from packages.utils import Embed, ImproperType
import aiohttp, pandas, numpy, discord
import matplotlib.pyplot as plt
from packages.nitrotype import Racer
import os
class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    async def fetch(self, url, session, data=None, method='GET'):
        if method == 'GET':
            async with session.get(url,data=data) as response:
                try:
                    return await response.json()
                except:
                    return await response.text()
        if method == 'POST':
            async with session.post(url,data=data) as response:
                return await response.json()
    @commands.command()
    async def checkbot(self, ctx, username):
       # return await ctx.send('**Your** security is important for **us**! Because of security reasons, this command has been taken down and will be back soon. Thanks for your understanding.')
        racer = await Racer(username)
        async with aiohttp.ClientSession() as s:
            botornot = await self.fetch('https://Lacan-Checkbot.try2win4code.repl.co', s, data={'username': username})
            print(botornot)
            csvdata = await self.fetch('https://Lacan-Checkbot.try2win4code.repl.co/data.csv',s)
        with open('data.csv', 'w') as f:
            f.write(csvdata)
        df = pandas.read_csv("data.csv")
        features = ['avgSpeed', 'highSpeed', 'racesTotal', 'highestSession']
        avgdivhigh = []
        racesTotal = list(df['racesTotal'])
        highest = []
        highest_int = 0
        for x in df['racesTotal']:
            avgSpeed = int(list(df['avgSpeed'])[list(df['racesTotal']).index(x)])
            highSpeed = int(list(df['highSpeed'])[list(df['racesTotal']).index(x)])
            highestSession = int(list(df['highestSession'])[list(df['racesTotal']).index(x)])
            if list(df['Go'])[list(df['racesTotal']).index(x)] == 1:
                del racesTotal[list(racesTotal).index(x)]
                continue
            avgdivhigh.append((int(x)-highestSession)*(highSpeed-avgSpeed))
        plt.scatter(racesTotal, avgdivhigh, color='blue')
        '''
        slope, intercept, r, p, std_err = stats.linregress(racesTotal, avgdivhigh)
        def myfunc(x):
            return slope * x + intercept
        #print(myfunc(234061))
        mymodel = list(map(myfunc, racesTotal))
        '''
        mymodel = numpy.poly1d(numpy.polyfit(racesTotal, avgdivhigh, 3))
        myline = numpy.linspace(1, 700000, 700000)
        plt.plot(myline, mymodel(myline), color='blue')
        plt.xlabel('Races')
        plt.ylabel('Formula')
        plt.scatter([int(racer.races.replace(',', ''))],[(int(racer.races.replace(',', ''))-int(racer.newdata['longestSession']))*(int(racer.wpm_high.replace(',', ''))-int(racer.wpm_average.replace(',', '')))],color='red')
        plt.savefig('graph.png')
        plt.cla()
        embed = Embed('Botting Or Not?', 'Analysis of **'+username+'**')
        if botornot['botornot'] == 'error':
            embed.field('Error!', 'I could not find that account!')
        else:
            embed.field('Bot Or Not', '__BOT__' if botornot['botornot'][0] == 1 else '__LEGIT__')
            embed.field('Chance Of Being A Bot', str(botornot['botornot'][1]*100)+'%')
            embed.field('Accuracy', '`'+str(((botornot['accuracy'][0]*100)+(botornot['accuracy'][1]*100))/2)+'`%')
        file = discord.File("graph.png", filename="graph.png")
        embed.image(url="attachment://graph.png")
        await ctx.send(file=file, embed=embed.default_embed())
def setup(client):
    client.add_cog(Command(client))
