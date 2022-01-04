'''An interactive view of the latest nitrotype news'''

from discord.ext import commands
from discord import Reaction, User
from packages.utils import Embed, ImproperType
from packages.nitrotype import News
from asyncio import TimeoutError

def cycle_news(news, current_page):
    if current_page == 4:
        return 0
    else:
        return current_page + 1

class Command(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def news(self, ctx):
        if await ImproperType.check(ctx): return
        page = 0

        def check(reaction:Reaction, user:User):
            return user.id == ctx.author.id

        #return await ctx.send('This command is currently under maintenance. The developers will try to get it up again as soon as possible. In the meantime feel free to use `n.help` to get the other commands. Thank you for your understanding!')

        news = await News()
        news = news.data[page]

        embed = Embed('', f':race_car:  ***[{news["title"]}]({news["link"]})***\n{news["description"]}')
        embed.footer(f'{news["author"]} wrote this on {news["created"]} UTC')
        embed.image(news['image'])
        message = await ctx.send(embed=embed.default_embed(), content=None)
        await message.add_reaction('🔄')

        while True:
            try:
                reaction, user = await self.client.wait_for('reaction_add', timeout=120, check=check)
            except TimeoutError:
                await reaction.delete()
                break
            else:
                if str(reaction) == '🔄':
                    news = await News()
                    page = cycle_news(news.data, page)
                    news = await News()
                    news = news.data[page]

                    embed = Embed('', f':race_car:  ***[{news["title"]}]({news["link"]})***\n{news["description"]}')
                    embed.footer(f'{news["author"]} wrote this on {news["created"]} UTC')
                    embed.image(news['image'])
                    await message.remove_reaction(reaction, user)
                    await message.edit(embed=embed.default_embed())
                else:
                    await message.remove_reaction(reaction, user)

def setup(client):
    client.add_cog(Command(client))
