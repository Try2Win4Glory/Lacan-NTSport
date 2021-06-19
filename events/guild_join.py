from discord.ext import commands
from packages.utils import Embed
class Events(commands.Cog):
    def __init__(self, client):
        self.client = client
    @commands.Cog.listener('on_guild_join')
    async def event(self, guild):
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                try:

                    embed=Embed('Thanks for inviting me!', 'Thank you for inviting me to your server.\n\n**__FAQ:__**\n\nWho am I?\nI\'m Lacan NTSport, a multi purpose discord bot for the game [nitrotype](https://nitrotype.com/).\n\nWhat\'s my prefix?\nMy prefix is `n.` or `N.`.\n\nHow do I get a list of commands?\nIn order to get a full list of commands make sure to run `n.help`.\n\nHow can you invite me to your server?\nIn order to invite me to your server, run `n.invite`.\n\nWho are my developers?\nI was developed by <@505338178287173642>, <@396075607420567552>, <@637638904513691658>.\n\nWhat\'s premium? How can I get it?\nIn order to learn more about premium, make sure to run `n.premium`.', 'information source')
                    return await embed.send
                    break
                except:
                    pass
def setup(client):
    client.add_cog(Events(client))
