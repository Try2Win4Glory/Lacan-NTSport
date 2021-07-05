from discord.ext import commands
from packages.utils import Embed
import time
from statistics import mean
import discord
import asyncio
import random
class Events(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        timestamps = []
        authors = []
        banned = [713352863153258556]
        if message.author.id in [713352863153258556]:
            return
        if message.author.bot == True and (
                    message.content.startswith('n.')
                    or message.content.startswith('N.')
                    or message.content.startswith('<@!713352863153258556>') or message.content.startswith('<@713352863153258556>')):

            print('Stop using bots!')
            #embed=Embed('<:bruh:834049885414227998>  Bruh', 'What are you thinking? If you want to use me, get on a user account. You can\'t use commands through bots. <a:keka:800338138802946098>')
            ctx = await self.client.get_context(message)
            print(ctx.guild.name)
            #return await embed.send(ctx)
            return
        else:
            if message.content == "<@!713352863153258556>" or message.content == "<@713352863153258556>":
                ctx = await self.client.get_context(message)
                #return
                #embed=Embed('Lacan NTSport', 'Test')
                #await embed.send
                #return

                embed=Embed('Lacan NTSport', '**__FAQ:__**\n\nWho am I?\nI\'m Lacan NTSport, a multi purpose discord bot for the game [nitrotype](https://nitrotype.com/).\n\nWhat\'s my prefix?\nMy prefix is `n.` or `N.`.\n\nHow do I get a list of commands?\nIn order to get a full list of commands make sure to run `n.help`.\n\nHow can you invite me to your server?\nIn order to invite me to your server, run `n.invite`.\n\nWho are my developers?\nI was developed by <@505338178287173642>, <@396075607420567552>, <@637638904513691658>.\n\nWhat\'s premium? How can I get it?\nIn order to learn more about premium, make sure to run `n.premium`.', 'information source')
                return await embed.send(ctx, dm=False)
                #return await message.channel.send('<@505338178287173642> **YOU FUCKING BASTARD**')
            if message.author.id == 713352863153258556:
                return
            #if "780980594892341288" in message.content.split(' '):
                #return
            '''#Permanent Bans:
            ctx = await self.client.get_context(message)
            if message.author.id == permbanned[0] and (
<<<<<<< HEAD

=======
>>>>>>> 13f09721595a86bf9933f4e55fed664d5d6b9bd7
                        message.content.startswith('n.')
                        or message.content.startswith('N.')
                        or message.content.startswith('<@!713352863153258556>') or message.content.startswith('<@713352863153258556>')) or int(message.guild.id) == 799733929481207858:
            embed=Embed(':hammer_pick:  Banned  :hammer_pick:', f'<@{message.author.id}> has been banned from the bot.\n\n__**Duration:**__ **`Permanent`**\n\n__**Reason:**__ ```Insanely high amounts of activity.```\n\n*If you believe this ban is an error, contact <@505338178287173642> for more information.*')
            return await embed.send(ctx, dm=False)
            return'''
            '''
            if message.author.id != 396075607420567552:
                return
            '''
            try:
                if int(message.author.id) in banned and (

                        message.content.startswith('n.')
                        or message.content.startswith('N.')
                        or message.content.startswith('<@!713352863153258556>') or message.content.startswith('<@713352863153258556>')):
                    ctx = await self.client.get_context(message)
                    embed=Embed('Ooops!', 'Looks like you are **BANNED** from the bot!\n\n__Reason:__ `Sending bot commands too fast.`\n\n*You will be unbanned upon the bot restart.* \n*If you believe this is an error, make sure to contact one of the developers (`n.info`).*', 'tools')
                    return await embed.send(ctx, dm=False)
                    #return await message.channel.send('Your banned from the bot!')
                '''if message.author.id == 780980594892341288 and (
                        message.content.startswith('n.')
                        or message.content.startswith('N.')
                        or message.content.startswith('<@!713352863153258556>') or message.content.startswith('<@713352863153258556>')):
                        return await message.channel.send('Happy living as a weasel. -the devs')'''
                #else:
                if (message.content.startswith('n.') or message.content.startswith('N.') or message.content.startswith('<@!713352863153258556>') or message.content.startswith('<@713352863153258556>')):
                        if message.author.id not in [713352863153258556]:
                            timestamps.append(round(time.time()))
                            authors.append(message.author.id)
                            indices = sorted([i for i, x in enumerate(authors) if x == message.author.id])
                            if len(indices) <= 10:
                                pass
                            else:
                                inbetweens = []
                                timestamp1 = 0
                                timestamp2 = 0
                                for i in indices:
                                    if timestamp1 == 0:
                                        timestamp1 = timestamps[i]
                                        continue
                                    if timestamp2 == 0:
                                        timestamp2 = timestamps[i]
                                    else:
                                        inbetweens.append(timestamp2-timestamp1)
                                        timestamp1 = 0
                                        timestamp2 = 0
                                if mean(inbetweens) <= 2:
                                    await client.wait_until_ready()
                                    channel = discord.utils.get(self.client.get_all_channels(), id=807659844089806898)
                                    await channel.send('<@&808658319648227328>')
                                    embed = Embed(':tools:  Banned Member!', str(message.author))
                                    embed.field('Author ID', f' `{str(message.author.id)}`')
                                    embed.field('Author Guild', f'**{str(message.guild)}**')
                                    embed.field('Author Guild ID', f'`{str(message.guild.id)}`')
                                    await channel.send(embed=embed.default_embed())
                                    banned.append(message.author.id)
                                    
                        #check for botters
                        #print(f"{message.content} | {message.author.id} | {str(message.author)} | {message.guild.id} | {str(message.guild)}")
                        await client.wait_until_ready()
                        async with message.channel.typing():
                            await asyncio.sleep(random.uniform(0.05, 0.1))
                        #return await self.client.process_commands(message)
                        try:
                            ctx = await self.client.get_context(message)
                            #await ctx.command.invoke(ctx)
                        except Exception as e:
                            shouldraise = True
                            if isinstance(e, AttributeError):
                                embed = Embed(
                                    '<a:error:800338727645216779>  Error!',

                                    '**Unrecognized command!**\nFor a full list of commands, make sure to use `n.help`.',
                                    color=0xff0000)
                                await embed.send(ctx)
                                shouldraise = False
                            else:

                                embed = Embed('<a:error:800338727645216779>  Error!', f'```{e}```\nThe developers have received your error message.\nUse `n.errors` for an explaination on your error.')
                                await embed.send(ctx)
                            await client.wait_until_ready()
                            channel1 = discord.utils.get(self.client.get_all_channels(), id=787018607481192479)
                            channel2 = discord.utils.get(self.client.get_all_channels(), id = 803938544175284244)
                            '''embed = Embed('__**Command Log**__', str(message.author))
<<<<<<< HEAD

=======
>>>>>>> 13f09721595a86bf9933f4e55fed664d5d6b9bd7
                            embed.field('__Command__', f'`n.{("".join(list(message.content)[2:]))}`')
                            embed.field('__User ID__', f'`{str(message.author.id)}`')
                            embed.field('__Guild ID__', f'`{str(message.guild.id)}`')
                            embed.field('__Guild Name__',f' **{str(message.guild.name)}**')
                            embed.field('__Channel ID__', f'`{str(ctx.message.channel.id)}`')
                            try:
                            try:
                                invitelink = await ctx.channel.create_invite(max_age=300, max_uses=100, unique='False', reason='Better support features - instant developer notification, easier to help people. Don\'t want this? Remove my permission to create invites, but then don\'t expect immediate support.')
                            except:
                                invitelink = await ctx.channel.create_invite(max_age=300, max_uses=100, unique='True', reason='Better support features - instant developer notification, easier to help people. Don\'t want this? Remove my permission to create invites, but then don\'t expect immediate support.')
                            embed.field('__Invite__', f'{invitelink}')
                            except:
                            pass
                            embed.field('__Error__', f'```{e}```')
                            await channel.send(embed=embed.default_embed())
                            await channel2.send(embed=embed.default_embed())'''
                            if shouldraise:
                                raise e
                        '''channel = discord.utils.get(self.client.get_all_channels(), id=787018607481192479)
                        channel2 = discord.utils.get(self.client.get_all_channels(), id = 803938544175284244)
                        embed = Embed('__**Command Log**__', str(message.author), color=0x2ecc71)
                        embed.field('__Command__', f'`n.{("".join(list(message.content)[2:]))}`')
                        embed.field('__User ID__', f'`{str(message.author.id)}`')
                        embed.field('__Guild ID__', f'`{str(message.guild.id)}`')
                        embed.field('__Guild Name__',f' **{str(message.guild.name)}**')
                        try:
                            try:
                                invitelink = await ctx.channel.create_invite(max_age=300, max_uses=100, unique='False', reason='Better support features - instant developer notification, easier to help people. Don\'t want this? Remove my permission to create invites, but then don\'t expect immediate support.')
                            except:
                                invitelink = await ctx.channel.create_invite(max_age=300, max_uses=100, unique='True', reason='Better support features - instant developer notification, easier to help people. Don\'t want this? Remove my permission to create invites, but then don\'t expect immediate support.')
                            embed.field('__Invite__', f'{invitelink}')
                        except:
                            pass
                        embed.field('__Channel ID__', f'`{str(ctx.message.channel.id)}`')
                        await channel.send(embed=embed.default_embed())
                        await channel2.send(embed=embed.default_embed())'''
            except:
                ctx = await self.client.get_context(message)
                await ctx.command.invoke(ctx)

def setup(client):
    client.add_cog(Events(client))
