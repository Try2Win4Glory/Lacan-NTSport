'''Add roles to a server'''

from discord.ext import commands
from packages.utils import Embed, ImproperType
import requests, json, os
import discord

class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def numroles(self, ctx):
        #return await ctx.send('This command is currently under maintenance. The developers will try to get it up again as soon as possible. In the meantime feel free to use `n.help` to get the other commands. Thank you for your understanding!')
        if (ctx.author.id) not in [505338178287173642]:
            embed = Embed('Error!', 'You\'re not a developer of this bot! Click [here](https://www.latlmes.com/entertainment/dev-application-1) to apply for dev.', 'warning')

            embed.footer(f'⚙️This command is a 🛠️developer🛠️ only command.⚙️', 'https://cdn.discordapp.com/attachments/719414661686099993/754971786231283712/season-callout-badge.png')
            return await embed.send(ctx)
        embed = Embed('Success!', f'The roles for `{str(ctx.author.guild.id)}` were created by '+str(ctx.author.name + '#' + ctx.author.discriminator)+'.\n\n**Type:** __Racecount Roles__','white_check_mark')
        embed.footer(f'Discord user '+str(ctx.author.name + '#' + ctx.author.discriminator)+' is a 🛠️developer🛠️ of this bot.\n⚙️This command is a 🛠️developer🛠️ only command.⚙️', 'https://media.discordapp.net/attachments/719414661686099993/765490220858081280/output-onlinepngtools_32.png')
        guild = ctx.guild
        await embed.send(ctx)
        await guild.create_role(name="Gold Member", colour=discord.Colour(0xFFFF00))
        await guild.create_role(name="Registered")
        await guild.create_role(name=">99% Accuracy")
        await guild.create_role(name="99% Accuracy")
        await guild.create_role(name="98% Accuracy")
        await guild.create_role(name="97% Accuracy")
        await guild.create_role(name="96% Accuracy")
        await guild.create_role(name="94-95% Accuracy")
        await guild.create_role(name="90-93% Accuracy")
        await guild.create_role(name="87-89% Accuracy")
        await guild.create_role(name="84-86% Accuracy")
        await guild.create_role(name="80-83% Accuracy")
        await guild.create_role(name="75-79% Accuracy")
        await guild.create_role(name="<75% Accuracy")
        await guild.create_role(name="220+ WPM")
        await guild.create_role(name="210-219 WPM")
        await guild.create_role(name="200-209 WPM")
        await guild.create_role(name="190-199 WPM")
        await guild.create_role(name="180-189 WPM")
        await guild.create_role(name="170-179 WPM")
        await guild.create_role(name="160-169 WPM")
        await guild.create_role(name="150-159 WPM")
        await guild.create_role(name="140-149 WPM")
        await guild.create_role(name="130-139 WPM")
        await guild.create_role(name="120-129 WPM")
        await guild.create_role(name="110-119 WPM")
        await guild.create_role(name="100-109 WPM")
        await guild.create_role(name="90-99 WPM")
        await guild.create_role(name="80-89 WPM")
        await guild.create_role(name="70-79 WPM")
        await guild.create_role(name="60-69 WPM")
        await guild.create_role(name="50-59 WPM")
        await guild.create_role(name="40-49 WPM")
        await guild.create_role(name="30-39 WPM")
        await guild.create_role(name="20-29 WPM")
        await guild.create_role(name="10-19 WPM")
        await guild.create_role(name="1-9 WPM")
        await guild.create_role(name="500000+ Races")
        await guild.create_role(name="250000-499999 Races")
        await guild.create_role(name="200000-249999 Races")
        await guild.create_role(name="150000-199999 Races")
        await guild.create_role(name="100000-149999 Races")
        await guild.create_role(name="75000-99999 Races")
        await guild.create_role(name="50000-74999 Races")
        await guild.create_role(name="40000-49999 Races")
        await guild.create_role(name="30000-39999 Races")
        await guild.create_role(name="20000-29999 Races")
        await guild.create_role(name="10000-19999 Races")
        await guild.create_role(name="5000-9999 Races")
        await guild.create_role(name="3000-4999 Races")
        await guild.create_role(name="1000-2999 Races")
        await guild.create_role(name="500-999 Races")
        await guild.create_role(name="100-499 Races")
        await guild.create_role(name="50-99 Races")
        await guild.create_role(name="1-49 Races")
def setup(client):
    client.add_cog(Command(client))
