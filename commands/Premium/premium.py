'''What is premium?'''
from discord.ext import commands
from packages.utils import Embed, ImproperType

class Command(commands.Cog):

    def __init__(self, client):
        self.client= client
    
    @commands.command()
    async def premium(self, ctx):
        #return await ctx.send('This command is currently under maintenance. The developers will try to get it up again as soon as possible. In the meantime feel free to use `n.help` to get the other commands. Thank you for your understanding!')
        if await ImproperType.check(ctx): return

        embed=Embed('Premium', 'Premium is a one time purchase for your Discord server. \n It will make your server appearance a lot better. \n There are lots of benefits you will get for being a premium server. \n \n Your benefits are: \n :small_blue_diamond: **LIFETIME** server access to **all** features of this bot. \n :small_blue_diamond: You don\'t have to do anything, the bot will create speed, gold member, accuracy and race roles for your server. \n :small_blue_diamond: Role registering / updating system through the command `n.update`. \n :small_blue_diamond: Nickname updating system through the command `n.update`. \n  :small_blue_diamond: The feeling that you helped the developers a lot through your purchasement. \n :small_blue_diamond: More things coming soon:tm:, so stay tuned. \n \n :small_orange_diamond: In order to receive these Premium features, check your class down below. Then send `10M` to [this](https://nitrotype.com/racer/theteamracer) account and DM <@505338178287173642> on discord.', 'diamond_shape_with_a_dot_inside')
        #\n\n **__List of Premium 💠 Server Prizes__** (since December 20th 2020)\n\n:small_orange_diamond: ***Class I:*** Human Members: __<50__, Age: __>3 months__: `5M`.\n\n:small_orange_diamond: ***Class II:*** Human members: __50-99__, Age: __>3 months__: `10M`.\n\n:small_orange_diamond: ***Class III:*** Human members: 100-150, Age: __>3 months__: `15M`. \n\n:small_orange_diamond: ***Class IV:*** Human members: __150-199__, Age __>3 months__: `20M`. \n\n:small_orange_diamond: ***Class V: ***Human members: __200+__, Age: __>3 months__: `25M`. \n\n:small_orange_diamond: ***Class VI: ***Human members: __ANY__, Age: __<3 months__: `20M`.')
        embed.footer(f'{ctx.author} • Become a premium 💠 member today! 💗')
        embed.thumbnail('https://media.discordapp.net/attachments/719414661686099993/754971786231283712/season-callout-badge.png')
        await embed.send(ctx)
        try:
          await ctx.message.delete()
        except:
          pass
    
def setup(client):
    client.add_cog(Command(client))