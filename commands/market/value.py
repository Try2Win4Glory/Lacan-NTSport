'''Get The Value Of A Racer'''

from discord.ext import commands
from packages.utils import Embed, ImproperType
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from packages.nitrotype import Racer
import pandas
from cooldowns.value import rateLimit, cooldown_add
class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def value(self, ctx, username=None):
        
        # Cooldown
        if str(ctx.author) in rateLimit:
            embed = Embed('Cooldown!','You are on cooldown. Wait `10` seconds before running this command again.','alarm clock')
            return await embed.send(ctx)
        if await ImproperType.check(ctx): return
        if ctx.author.id not in [
          #Try2Win4Glory
            505338178287173642, 
          #Typerious
            637638904513691658, 
          #adl212
            396075607420567552]:
            cooldown_add(str(ctx.author))
        
        linear = LinearRegression(positive=True, fit_intercept=False)
        df = pandas.read_csv('./commands/market/data.csv')
        f_names = ['races','wpm_average','wpm_high','longestSession','membership','cars_owned','views','first','second','third','created']
        features = df[f_names]
        targets = df['price']
        features = features.drop(columns=['first', 'second', 'third', 'created', 'wpm_average', 'wpm_high'])
        f_names = list(features.columns)
        linear = linear.fit(features, targets)
        racer = await Racer(username)
        if not racer.success:
            embed=Embed(':warning:  Error!', f'The requested Nitrotype User **{username}** [:link:](https://nitrotype.com/racer/{username}) couldn\'t be found.')
            return await embed.send(ctx)
        l = f"{int(racer.races.replace(',', ''))},{racer.wpm_average},{racer.wpm_high},{racer.newdata['longestSession']},{1 if racer.newdata['membership'] == 'gold' else 0},{racer.cars_owned},{racer.views.replace(',', '')},{racer.first.replace(',', '')},{racer.second.replace(',', '')},{racer.third.replace(',', '')},{racer.newdata['createdStamp']}".split(',')
        l = list(map(int, l))
        l = l[:-4]
        del l[1]
        del l[1]
        pred = linear.predict([l])
    
        rawval = str(pred[0]*10**6)
        roundval = round(float(rawval))
        formval = "{:,}".format(roundval)
        embed=Embed('Account Value', 'This value is supposed to show the price on the trading market', 'money with wings')
        embed.field('__Nitrotype User__', f'{racer.username} [:link:](https://nitrotype.com/racer/{racer.username})')
        embed.field('__Value__', f'$**{formval}**')
        for x in l:
            index = l.index(x)
            lifetime = False
            if f_names[index].lower() == 'membership':
                lifetime = racer.lifetime_gold
            embed.field(
                f'__{f_names[index]}__',
                "{:,}".format(
                    round(
                        float(
                            float(linear.coef_[index])*float(x)*10**6 if lifetime == False else float(linear.coef_[index])*float(x)*10**6*3
                        )
                    )
                )
            )
                
        await embed.send(ctx)
def setup(client):
    client.add_cog(Command(client))
