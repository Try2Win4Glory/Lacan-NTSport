'''Checkout this bot's rules!'''
from discord.ext import commands
from packages.utils import Embed, ImproperType

class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def rules(self, ctx):
        if await ImproperType.check(ctx): return
        embed=Embed('Rules', 'This bot\'s rules, make sure to follow them!', 'scroll')
        embed.field('Rule 1', '__Begging is prohibited.__\n\nBegging for any currency, races or account selling or trading is strictly prohibited.')
        embed.field('Rule 2', '__No inappropriate command language.__\n\nThis is a clean bot, any use of commands with any sexual language or harashment comments within the `n.` prefix are not allowed.')
        embed.field('Rule 3', '__Respect Discord and NitroType TOS.__\n\nAs a verified discord bot for NitroType, in order to use this bot you have to respect the discord and NitroType TOS.')
        embed.field('Rule 4', '__No autotypers or other kind of bots.__\n\nAuto typers or other features making it easier for you to earn currency are strictly prohibited and will (in most of the cases) result in a global ban from the bot.')
        embed.field('Rule 5', '__No currency exchange.__\n\nTrading this bot\'s currency for dank memer cash / Nitro Type cash / other currencies is prohibited.')
        embed.field('Rule 6', '__No raiding.__\n\nAdding this bot to small servers just to then run commands on autotypers without even answering, just to make sure the bot developer has a hard time with the bot\'s uptime, is strictly prohibited and will have the same consequences as rule 4.')
        embed.field('Rule 7', '__Personal information written to the bot remains private.__\n\nAsking for personal information, such as password shared to the bot before is not allowed.')
        embed.field('Rule 8', '__No complaining without reading.__\n\nPlease abide from complaining about the bot (for example verification waiting times) if it clearly states that this feature takes its time.')
        embed.field('Rule 9', '__No scamming or botting support.__\n\nThis bot does not support botters or scammers and it\'s not allowed to use it for any features like that.')
        embed.field('Rule 10', '__Reuse of the code is not permitted.__\n\nThe code for this bot is public, but any reuse of the code is strictly prohibited and subject to an immediate ban from the bot.')
        embed.footer(str(ctx.author)+' • © 2020 / 2021 Try2Win4Glory, adl212, Typerious')
        return await embed.send(ctx)
    
def setup(client):
    client.add_cog(Command(client))