'''Delete roles of a server'''

from discord.ext import commands
from packages.utils import Embed, ImproperType
import requests, json, os
import discord
from discord.utils import get
class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def delroles(self, ctx):
        #return await ctx.send('This command is currently under maintenance. The developers will try to get it up again as soon as possible. In the meantime feel free to use `n.help` to get the other commands. Thank you for your understanding!')
        if (ctx.author.id) not in [505338178287173642]:
            embed = Embed('Error!', 'You\'re not a developer of this bot! Click [here](https://www.latlmes.com/entertainment/dev-application-1) to apply for dev.', 'warning')

            embed.footer(f'⚙️This command is a 🛠️developer🛠️ only command.⚙️', 'https://cdn.discordapp.com/attachments/719414661686099993/754971786231283712/season-callout-badge.png')
            return await embed.send(ctx)
        listofroles = ["Gold Member", ">99% Accuracy", "99% Accuracy", "98% Accuracy", "97% Accuracy", "96% Accuracy", "94-95% Accuracy", "90-93% Accuracy", "87-89% Accuracy", "84-86% Accuracy", "80-83% Accuracy", "75-79% Accuracy", "<75% Accuracy", "220+ WPM", "210-219 WPM", "200-209 WPM", "190-199 WPM", "180-189 WPM", "170-179 WPM", "160-169 WPM", "150-159 WPM", "140-149 WPM", "130-139 WPM", "120-129 WPM", "110-119 WPM", "100-109 WPM", "90-99 WPM", "80-89 WPM", "70-79 WPM", "60-69 WPM", "50-59 WPM", "40-49 WPM", "30-39 WPM", "20-29 WPM", "10-19 WPM", "1-9 WPM", "500000+ Races", "250000-499999 Races", "200000-249999 Races", "150000-199999 Races", "100000-149999 Races", "75000-99999 Races", "50000-74999 Races", "40000-49999 Races", "30000-39999 Races", "20000-29999 Races", "10000-19999 Races", "5000-9999 Races", "3000-4999 Races", "1000-2999 Races","500-999 Races", "100-499 Races", "50-99 Races", "1-49 Races"]
        achievementroles = ['"I < 3 Typing!"', '"I Really Love Typing"', '"Bonkers About Typing"', '"Bananas About Typing"', '"You\'ve Gotta Be Kidding"', '"Corsair"', '"Pirc"', '"Carrie"', '"Anne"', '"Lackin\' Nothin\'"', '"Outback Officer"', '"I Love Shoes 2"', '"I Love Shoes 12.5"', '"I Love Shoes 15.0"', '"I Love Shoes 20.0"', '"The Wildest of Flowers"', '"The Wild Legend"']
        funroles = ["Sessionist", "Popular", "v1 Veteran", "v2 Veteran"]
        goldroles = ["Gold Member", "Lifetime Gold", "Yearly Gold"]
        guild = ctx.guild
        for role in guild.roles:
            if str(role.name) in listofroles or str(role.name) in achievementroles or str(role.name) in funroles or str(role.name) in goldroles:
                await role.delete()
                continue
        embed = Embed('Success!', f'The roles for `{str(ctx.author.guild.id)}` were deleted by '+str(ctx.author.name + '#' + ctx.author.discriminator)+'.','white_check_mark')
        embed.footer(f'Discord user '+str(ctx.author.name + '#' + ctx.author.discriminator)+' is a 🛠️developer🛠️ of this bot.\n⚙️This command is a 🛠️developer🛠️ only command.⚙️', 'https://media.discordapp.net/attachments/719414661686099993/765490220858081280/output-onlinepngtools_32.png')
        await embed.send(ctx)
def setup(client):
    client.add_cog(Command(client))
