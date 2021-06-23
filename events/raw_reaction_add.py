from discord.ext import commands
from packages.utils import Embed
import random
from mongoclient import DBClient
import copy
import discord
from nitrotype import check_perms
class Events(commands.Cog):
    def __init__(self, client):
        self.client = client
    @commands.Cog.listener('on_raw_reaction_add')
    async def event(self, payload):
        if payload.user_id == 713352863153258556:
            return
        dbclient = DBClient()
        collection = dbclient.db.giveaways
        dbdata = await dbclient.get_array(collection, {'$and': [{'messageID': payload.message_id}, {'messageID': payload.message_id}]})
        async for d in dbdata:
            user = d
            break
        try:
            old = copy.deepcopy(user)
            req_passed = await check_perms(payload.user_id, user['requirements'])
            if not req_passed:
                channel = discord.utils.get(self.client.get_all_channels(), id=int(payload.channel_id))
                msg = discord.utils.get(await channel.history().flatten(), id=int(payload.message_id))
            else:
                return await msg.remove_reaction(payload.emoji, payload.member)
            if payload.user_id in user['joined']:
                return
            user['joined'].append(payload.user_id)
            embed = Embed(':partying_face:  You entered the giveaway!  :partying_face:', 'You successfully entered the giveaway!')
            embed.field('Link', f'[Giveaway Link](https://discord.com/channels/{str(payload.guild_id)}/{str(payload.channel_id)}/{str(payload.message_id)}')
            await payload.member.send(embed=embed.default_embed())
            return await dbclient.update_array(collection, old, user)
        except:
            try:
                req_passed = await check_perms(payload.user_id, user['requirements'])
                if req_passed:
                    channel = discord.utils.get(self.client.get_all_channels(), id=int(payload.channel_id))
                    msg = discord.utils.get(await channel.history().flatten(), id=int(payload.message_id))
                    user['joined'] = [payload.user_id]
                    embed = Embed(':partying_face:  Entry approved!  :partying_face:', 'You successfully entered the giveaway!')
                    embed.field(':link:  Link', f'**[Giveaway Link](https://discord.com/channels/{str(payload.guild_id)}/{str(payload.channel_id)}/{str(payload.message_id)})**')
                    embed.field(':tools:  Support Server', 'Join the official **[Support Server](https://discord.gg/Wj96Ehg)**!')
                    embed.field(':arrow_up:  Vote', 'Vote for me **[here](https://top.gg/bot/713352863153258556)**.')
                    embed.field(':link:  Invite', 'Invite me through **[this](https://discord.com/oauth2/authorize?client_id=713352863153258556&permissions=2617633857&redirect_uri=https%3A%2F%2Fnitrotype.com&scope=bot)** link.')
                    await payload.member.send(embed=embed.default_embed())
                    return await dbclient.update_array(collection, old, user)
                else:
                    await msg.remove_reaction(payload.emoji, payload.member)
            except Exception as e:
                pass
        if int(payload.channel_id) == 810296381779476510:
            emoji = payload.emoji
        else:
            return
        if str(emoji) == '☑️':
            accepted = True
        else:
            accepted = False
        channel = discord.utils.get(self.client.get_all_channels(), id=int(payload.channel_id))
        msg = discord.utils.get(await channel.history().flatten(), id=int(payload.message_id))
        data = []
        for field in (msg.embeds[0].fields):
            data.append((field.name, field.value))
        data = dict(data)
        dbclient = DBClient()
        collection = dbclient.db.premium
        dbdata = await dbclient.get_big_array(collection, 'premium')
        if {"serverID": str(data['Guild ID'])} in dbdata['premium']:
            return
        if accepted == False:
            user = await self.client.fetch_user(int(data['Buyer ID']))
            embed = Embed(':weary:  Declined!', 'Your server\'s premium application has been denied. It will not be given premium. You have been refunded the Lacans.')
            collection = dbclient.db.pointsdb
            data = await dbclient.get_array(collection, {'$and': [{'userid': str(data['Buyer ID'])}, {'userid': str(data['Buyer ID'])}]})
            async for d in data:
                data = d
                old = copy.deepcopy(data)
                break
            points = data['points']
            data['points'] = int(points) + 3000
            await dbclient.update_array(collection, old, data)
            await msg.delete()
            return await user.send(embed=embed.default_embed())
        else:
            listofroles = [">99% Accuracy", "99% Accuracy", "98% Accuracy", "97% Accuracy", "96% Accuracy", "94-95% Accuracy", "90-93% Accuracy", "87-89% Accuracy", "84-86% Accuracy", "80-83% Accuracy", "75-79% Accuracy", "<75% Accuracy", "220+ WPM", "210-219 WPM", "200-209 WPM", "190-199 WPM", "180-189 WPM", "170-179 WPM", "160-169 WPM", "150-159 WPM", "140-149 WPM", "130-139 WPM", "120-129 WPM", "110-119 WPM", "100-109 WPM", "90-99 WPM", "80-89 WPM", "70-79 WPM", "60-69 WPM", "50-59 WPM", "40-49 WPM", "30-39 WPM", "20-29 WPM", "10-19 WPM", "1-9 WPM", "500000+ Races", "250000-499999 Races", "200000-249999 Races", "150000-199999 Races", "100000-149999 Races", "75000-99999 Races", "50000-74999 Races", "40000-49999 Races", "30000-39999 Races", "20000-29999 Races", "10000-19999 Races", "5000-9999 Races", "3000-4999 Races", "1000-2999 Races","500-999 Races", "100-499 Races", "50-99 Races", "1-49 Races"]
            guild = discord.utils.get(self.client.guilds, id=int(data['Guild ID']))
            dbdata['premium'].append({'serverID': str(guild.id)})
            await dbclient.update_big_array(collection, 'premium', dbdata)
            await guild.create_role(name="Gold Member", colour=discord.Colour(0xFFFF00))
            for role in listofroles:
                await guild.create_role(name=role)
            user = await self.client.fetch_user(int(data['Buyer ID']))
            embed = Embed('Success!', 'Your server has been given premium!')
            await msg.delete()
            channel1 = discord.utils.get(self.client.get_all_channels(), id=812375645828153385)
            channel2 = discord.utils.get(self.client.get_all_channels(), id=812268302117634078)
            list_of_lacans = ['<:lacan_economy_1:801006407536607262>','<:lacan_economy_2:801004873612132382>','<:lacan_economy_3:801004873214722079>','<:lacan_economy_4:801004868126113822>','<:lacan_economy_5:801004868348936203>','<:lacan_economy_6:801004863433605160>','<:lacan_economy_7:801004870643220481>','<:lacan_economy_8:801004872820457483>','<:lacan_economy_9:801004872417804298>','<:lacan_economy_10:801004872811413514>']
            random_lacan = random.choice(list_of_lacans)
            #data['Buyer ID'] is the buyer id/ctx.author.id
            #data['Buyer Name'] is the buyer name/str(ctx.author)
            #data['Guild ID'] is the guild id/ctx.guild.id
            #data['Guild Name'] is the guild name/str(ctx.guild)
            author = data['Buyer ID']
            guildid = data['Guild ID']
            guildname = data['Guild Name']
            amount = 3000
            embed=Embed(':diamond_shape_with_a_dot_inside:  New premium guild!', f'Lacan NTSport just sold a new premium server for `{amount}` {random_lacan}!')
            embed.field('Buyer ID', f'`{author}`')
            embed.field('Buyer Mention', f'<@{author}>')
            embed.field('Guild ID', f'`{guildid}`')
            embed.field('Guild Name', f'**{guildname}**')
            await channel1.send(embed=embed.default_embed())
            await channel2.send(embed=embed.default_embed())
        
    '''
            def __init__(self, self.client):
            self.self.client = self.client
            channelsendsuccess = discord.utils.get(self.self.client.get_all_channels(), id=812268302117634078)
            embed1 = Embed('Someone Wants Premium!', 'Click :ballot_box_with_check: to accept or :x: to deny.')
            embed1.field('Guild ID', f'{str(ctx.guild.id)}')
            embed1.field('Guild Name', f'{str(ctx.guild)}')
            embed1.field('Buyer ID', f'{str(ctx.author.id)}')
            embed1.field('Buyer Name', str(ctx.author))
            msg = await channelsendsuccess.send(embed=embed.default_embed())

            return await user.send(embed=embed.default_embed())
            '''
def setup(client):
    client.add_cog(Events(client))
