'''Fetches a meme from Reddit'''

from discord.ext import commands
from packages.utils import Embed, ImproperType
from packages.reddit import ImageFetcher

class Command(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.fetcher = ImageFetcher({'dankmemes' : 150, 'memes' : 150, 'meirl' : 50})
    
    @commands.command()
    async def meme(self, ctx):
        #return await ctx.send('This command is currently under maintenance. The developers will try to get it up again as soon as possible. In the meantime feel free to use `n.help` to get the other commands. Thank you for your understanding!')
        if await ImproperType.check(ctx): return
        post = self.fetcher.image()
        if post == None:
            embed = Embed('Error!', 'We couldn\'t fetch the memes!', 'sob')
        embed = Embed('', f':frame_photo:  **[{post["title"]}]({post["url"]})**')
        embed.image(post['image'])
        embed.footer(f'👍{post["upvotes"]:,d} | 💬{post["comments"]:,d}')
        await embed.send(ctx)
    
def setup(client):
    client.add_cog(Command(client))
