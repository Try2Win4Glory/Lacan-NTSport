'''Create Giveaways With Custom Requirements'''

from discord.ext import commands
from packages.utils import Embed, ImproperType
import discord
from mongoclient import DBClient
from asyncio.exceptions import TimeoutError
from datetime import datetime
import random
import discord.permissions
from discord import Member
from discord.utils import get
from packages.nitrotype import Team
class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    def check(self, author, channel):
        def inner_check(message):
            return message.author == author and message.channel.id == channel
        return inner_check
    async def wait_for_msg(self, ctx):
        try:
            msg = await self.client.wait_for('message', check=self.check(ctx.author, ctx.channel.id), timeout=30)
            return True, msg
        except TimeoutError:
            embed = Embed('Error!', 'You didn\'t answer in time!')
            return False, embed
    @commands.command()
    async def giveaway(self, ctx):
        role1 = get(ctx.message.guild.roles, name='Giveaways')
        for role in ctx.author.roles:
            if role.name.lower() == "giveaways":
                has_perm = True
                break
        #else:
            #has_perm = False
        #if has_perm == False:
            #pass
        if ctx.author.guild_permissions.manage_guild:
            has_perm = True
        elif ctx.author.guild_permissions.administrator:
            has_perm = True
        elif ctx.author.id in [505338178287173642]:
            has_perm = True
        else:
            has_perm = False
        if has_perm == False:
          pass
        print(has_perm)
        if has_perm == False:
            embed = Embed(':warning:  Error!', 'Seems like you don\'t have the permission to use this command.\n\nThis command requires a role called `Giveaways`.')
            return await embed.send(ctx)
        embed = Embed(':partying_face:  Create A Giveaway: Step 1 - Channel  :partying_face:', 'In what channel do you want the giveaway to be hosted?', color=0x00FF00)
        embed.field('__Instructions:__', 'Type in a channel ID or mention of the channel where the giveaway should be hosted!\n\n*Example response: **#giveaways***')
        await embed.send(ctx)
        msg = await self.wait_for_msg(ctx)
        if msg[0] == False:
            return msg[1].send(ctx)
        else:
            msg = msg[1]
        if ''.join(list(msg.content)[:2]) == "<#":
            channel = ''.join(list(msg.content)[2:-1])
        elif list(msg.content)[:2] == "<!#":
            channel = ''.join(list(msg.content)[3:-1])
        elif msg.content.isdigit():
            channel = msg.content
        else:
            embed = Embed(':warning:  Error!', 'You didn\'t give a valid channel ID or mention!')
            return await embed.send(ctx)
        embed = Embed(':partying_face:  Create A Giveaway: Step 2 - Duration  :partying_face:', 'How Long Is Your Giveaway going to last?', color=0x00FF00)
        embed.field('__Instructions:__', 'Use `s` for seconds, `m` for minutes, `h` for hours and `d` for days.\n\n*Example response: **1d***')
        await embed.send(ctx)
        msg = await self.wait_for_msg(ctx)
        if msg[0] == False:
            return msg[1].send(ctx)
        else:
            msg = msg[1]
        msg = msg.content
        if len(msg.split('s')) == 2:
            msg = msg.split('s')
            if not msg[0].isdigit():
                embed = Embed(':warning:  Error!', 'Invalid amount of time!')
                return await embed.send(ctx)
            gwtime = ('seconds', int(msg[0]))
        elif len(msg.split('m')) == 2:
            msg = msg.split('m')
            if not msg[0].isdigit():
                embed = Embed(':warning:  Error!', 'Invalid amount of time!')
                return await embed.send(ctx)
            gwtime = ('minutes', int(msg[0]))
        elif len(msg.split('h')) == 2:
            msg = msg.split('h')
            if not msg[0].isdigit():
                embed = Embed(':warning:  Error!', 'Invalid amount of time!')
                return await embed.send(ctx)
            gwtime = ('hours', int(msg[0]))
        elif len(msg.split('d')) == 2:
            msg = msg.split('d')
            if not msg[0].isdigit():
                embed = Embed(':warning:  Error!', 'Invalid amount of time!')
                return await embed.send(ctx)
            gwtime = ('days', int(msg[0]))
        else:
            embed = Embed(':warning:  Error!', 'You didn\'t give a valid amount of time!')
            return await embed.send(ctx)
        embed = Embed(':partying_face:  Create A Giveaway: Step 3 - Winners  :partying_face:', 'How Many Winners should this giveaway have?', color=0x00FF00)
        embed.field('__Instructions:__', 'Reply with the amount of winners you wish this giveaway to have.\n\n*Example response: **1***')
        await embed.send(ctx)
        msg = await self.wait_for_msg(ctx)
        if msg[0] == False:
            return msg[1].send(ctx)
        else:
            msg = msg[1]
        msg = msg.content
        if msg.isdigit:
            winners = msg
        else:
            embed = Embed(':warning:  Error!', 'You didn\'t give a valid number of winners!')
            return await embed.send(ctx)
        embed = Embed(':partying_face:  Create A Giveaway: Step 4 - Prize  :partying_face:', 'What should the prize of this giveaway be?', color=0x00FF00)
        embed.field('__Instructions:__', 'What are you giving away?\n\n*Example response: **100K NT cash ~courtesy of ⚡Try2Win4Glory⚡***')
        await embed.send(ctx)
        msg = await self.wait_for_msg(ctx)
        if msg[0] == False:
            return msg[1].send(ctx)
        else:
            msg = msg[1]
        prize = msg.content
        embed = Embed(':partying_face:  Create A Giveaway: Step 5 - Requirements  :partying_face:', 'Should this giveaway have requirements?', color=0x00FF00)
        embed.field('__Instructions:__', 'Reply with `y` if you want to include requirements, reply with `n` if you\'d like to start the giveaway without requirements\n\n*Example response: **y***')
        await embed.send(ctx)
        msg = await self.wait_for_msg(ctx)
        if msg[0] == False:
            return msg[1].send(ctx)
        else:
            msg = msg[1]
        requirements = {}
        if msg.content.lower() in ['y', 'n']:
            if msg.content.lower() in ['y']:
                while True:
                    embed = Embed(':partying_face:  Create A Giveaway: Step 5 - Requirements  :partying_face:', 'What type of requirement do you want?', color=0x00FF00)
                    embed.field('__Instructions:__', 'You can have `team` and `membership` requirements currently! Type one of them in! Type `none` to create the giveaway!')
                    await embed.send(ctx)
                    msg = await self.wait_for_msg(ctx)
                    if msg[0] == False:
                        return msg[1].send(ctx)
                    else:
                        msg = msg[1]
                    if msg.content.lower() == "team":
                        embed = Embed(':partying_face:  Create A Giveaway: Step 5 - Requirements  :partying_face:', 'What team does the user have to be in?', color=0x00FF00)
                        embed.field('__Instructions:__', 'Give a valid team name or team tag here!')
                        await embed.send(ctx)
                        msg = await self.wait_for_msg(ctx)
                        if msg[0] == False:
                            return msg[1].send(ctx)
                        else:
                            msg = msg[1]
                        team = await Team(msg.content)
                        if team.data == {}:
                            embed = Embed('Invalid Team!', 'Oops you messed up!')
                            await embed.send(ctx)
                            continue
                        else:
                            requirements.update({"team": msg.content})
                            continue
                    if msg.content.lower() == "membership":
                        embed = Embed(':partying_face:  Create A Giveaway: Step 5 - Requirements  :partying_face:', 'What type of membership does a person have to have?', color=0x00FF00)
                        embed.field('__Instructions:__', 'Type `gold` or `basic`, depending on the membership the users needs to have.')
                        await embed.send(ctx)
                        msg = await self.wait_for_msg(ctx)
                        if msg[0] == False:
                            return msg[1].send(ctx)
                        else:
                            msg = msg[1]
                        if msg.content.lower() == "gold":
                            requirements.update({"membership": "gold"})
                        if msg.content.lower() == "basic":
                            requirements.update({"membership": "basic"})
                        else:
                            embed = Embed('Invalid Membership', 'Oops you messed up!')
                            await embed.send(ctx)
                            continue
                    if msg.content.lower() == "none":
                        break

            else:
                if msg.content in ['n']:
                    pass
            embed = Embed(':white_check_mark:  Success!', f'You\'ve created a giveaway that will be hosted in channel <#{str(channel)}>, lasts **{gwtime[1]}** **{gwtime[0]}**, has **{winners}** winners, and you\'re giving away **{prize}**', color=0x00FF00)
            await embed.send(ctx)
            addedtime = 0
            if gwtime[0] == "seconds":
                addedtime = gwtime[1]
            elif gwtime[0] == "minutes":
                addedtime = 60*gwtime[1]
            elif gwtime[0] == "hours":
                addedtime = 60*60*gwtime[1]
            elif gwtime[0] == "days":
                addedtime = 24*60*60*gwtime[1]
            if requirements == {}:
                reqs = 'none'
            else:
                reqs = ''.join(list(str(requirements))[1:-1])
            try:
                list_of_lacans = ['<:lacan_economy_1:801006407536607262>','<:lacan_economy_2:801004873612132382>','<:lacan_economy_3:801004873214722079>','<:lacan_economy_4:801004868126113822>','<:lacan_economy_5:801004868348936203>','<:lacan_economy_6:801004863433605160>','<:lacan_economy_7:801004870643220481>','<:lacan_economy_8:801004872820457483>','<:lacan_economy_9:801004872417804298>','<:lacan_economy_10:801004872811413514>']
                random_lacan = random.choice(list_of_lacans)

                embed = Embed(':tada:  Giveaway  :tada:', f'\n\n**Entry:** React with {random_lacan}!\n\n**Prize:** {prize}\n\n**Winners:** {winners}\n\n**Hosted by:** {ctx.author.mention}', timestamp=(datetime.fromtimestamp(int(int(datetime.timestamp(datetime.now()))+addedtime))), color=0x00FF00)
                '''embed.field('Prize', gwcontent)
                embed.field('Winners', winners)
                embed.field('To Enter', f'React With {random_lacan} !')'''
                embed.field('Requirements', reqs)
                embed.footer('Ends at')
                c = discord.utils.get(ctx.guild.channels, id=int(channel))
                '''message = await c.send(content=":partying_face:", embed=embed.default_embed())'''
                message = await c.send(embed=embed.default_embed())

                await message.add_reaction(random_lacan)
            except:

                embed = Embed(':tada:  Giveaway  :tada:', f'\n\n**Entry:** React with :moneybag:!\n\n**Prize:** {prize}\n\n**Winners:** {winners}\n\n**Hosted by:** {ctx.author.mention}', timestamp=(datetime.fromtimestamp(int(int(datetime.timestamp(datetime.now()))+addedtime))), color=0x00FF00)
                '''embed.field('Prize', prize)
                embed.field('Winners', winners)
                embed.field('To Enter', 'React With :moneybag: !')'''
                embed.field('Requirements', reqs)
                embed.footer('Ends at')
                c = discord.utils.get(ctx.guild.channels, id=int(channel))
                message = await c.send(content="I am missing `Use external emoji` permissions. Make sure to give me those in order to enjoy giveaways even more!", embed=embed.default_embed())
                #message = await c.send(embed=embed.default_embed())
                await message.add_reaction('💰')
            dbclient = DBClient()
            collection = dbclient.db.giveaways
            await dbclient.create_doc(collection, {"endtime": int(int(datetime.timestamp(datetime.now()))+addedtime), "messageID": message.id, "channelID": message.channel.id, "ended": False, "requirements": requirements, "winners": winners})
        else:
            embed = Embed('Error!' 'You gave an invalid response! Your giveaway has been canceled.')
            return await embed.send(ctx)
        


def setup(client):
    client.add_cog(Command(client))
