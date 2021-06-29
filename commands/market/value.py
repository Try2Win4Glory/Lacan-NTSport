'''Get The Value Of A Racer'''

from discord.ext import commands
from packages.utils import Embed, ImproperType
from sklearn.tree import DecisionTreeRegressor
from packages.nitrotype import Racer
import pandas
class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def value(self, ctx, username):
        dtree = DecisionTreeRegressor()
        df = pandas.read_csv('./commands/market/data.csv')
        f_names = ['races','wpm_average','wpm_high','longestSession','membership','cars_owned','views','first','second','third','created']

        features = df[f_names]
        targets = df['price']
        dtree = dtree.fit(features, targets)
        racer = await Racer(username)
        if not racer.success:
            return
        l = f"{int(racer.races.replace(',', ''))},{racer.wpm_average},{racer.wpm_high},{racer.newdata['longestSession']},{1 if racer.newdata['membership'] == 'gold' else 0},{racer.cars_owned},{racer.views.replace(',', '')},{racer.first.replace(',', '')},{racer.second.replace(',', '')},{racer.third.replace(',', '')},{racer.newdata['createdStamp']}".split(',')
        return await ctx.send(str(dtree.predict([l])))
def setup(client):
    client.add_cog(Command(client))
