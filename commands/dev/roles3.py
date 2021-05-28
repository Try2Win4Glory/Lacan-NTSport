'''Add roles to a server'''

from discord.ext import commands
from packages.utils import Embed, ImproperType
import requests, json, os
import discord

class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def roles3(self, ctx):
        #return await ctx.send('This command is currently under maintenance. The developers will try to get it up again as soon as possible. In the meantime feel free to use `n.help` to get the other commands. Thank you for your understanding!')
        if (ctx.author.id) not in [396075607420567552, 505338178287173642, 637638904513691658]:
            embed = Embed('Error!', 'You\'re not a developer of this bot! Click [here](https://www.latlmes.com/entertainment/dev-application-1) to apply for dev.', 'warning')

            embed.footer(f'⚙️This command is a 🛠️developer🛠️ only command.⚙️', 'https://cdn.discordapp.com/attachments/719414661686099993/754971786231283712/season-callout-badge.png')
            return await embed.send(ctx)
        embed = Embed('Success!', f'The roles for `{str(ctx.author.guild.id)}` were created by '+str(ctx.author.name + '#' + ctx.author.discriminator)+'.','white_check_mark')
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
        otherraceroles = ['"I < 3 Typing"', '"I Really Love Typing!"', '"Bonkers About Typing"', '"Bananas About Typing"', '"You\'ve Gotta Be Kidding"', '"Corsair"', '"Pirc"', '"Carrie"', '"Anne"', '"Lackin\' Nothin\'"', '"Outback Officer"', '"I Love Shoes 2"', '"I Love Shoes 12.5"', '"I Love Shoes 15.0"', '"I Love Shoes 20.0"', '"The Wildest of Flowers"', '"The Wild Legend"']
        await guild.create_role(name=otherraceroles[16])
        await guild.create_role(name=otherraceroles[15])
        await guild.create_role(name=otherraceroles[14])
        await guild.create_role(name=otherraceroles[13])
        await guild.create_role(name=otherraceroles[12])
        await guild.create_role(name=otherraceroles[11])
        await guild.create_role(name=otherraceroles[10])
        await guild.create_role(name=otherraceroles[9])
        await guild.create_role(name=otherraceroles[8])
        await guild.create_role(name=otherraceroles[7])
        await guild.create_role(name=otherraceroles[6])
        await guild.create_role(name=otherraceroles[5])
        await guild.create_role(name=otherraceroles[4])
        await guild.create_role(name=otherraceroles[3])
        await guild.create_role(name=otherraceroles[2])
        await guild.create_role(name=otherraceroles[1])
        await guild.create_role(name=otherraceroles[0])
def setup(client):
    client.add_cog(Command(client))
