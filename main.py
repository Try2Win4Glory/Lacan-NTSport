#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
NitroType Bot
~~~~~~~~~~~~~
A discord bot designed for those interested in NitroType
:copyright: (c) 2020 Nitrotypers
:license: MIT, see LICENSE.txt for more details
'''

__title__ = 'Lacan NitroSport'
__version__ = 'Beta'
__author__ = 'SystematicError, Typerious, Try2Win4Glory, adl212'
__copyright__ = 'Copyright 2020 Nitrotypers'
__license__ = 'MIT'

# --- Start Code --- #
from discord.ext import commands
from discord import Streaming
from packages.server import start_server
from os import listdir, getenv, system
import json, requests
from mongoclient import DBClient
import dbl
from packages.utils import Embed, ImproperType
import asyncio, random
import subprocess
import sys
import logging
import discord
import os 
import time
from statistics import mean
from discord.utils import get
from nitrotype import check_perms, get_username
from packages.nitrotype import Team, Racer
import copy
try: import requests
except ImportError:
  print ("Trying to Install required module: motor tornado\n")
  os.system('python', '-m', 'pip', 'install', requests)
  import requests


intents = discord.Intents().default()
client = commands.Bot(command_prefix=commands.when_mentioned_or(*['N.', 'n.']), case_insensitive=True, intents=intents)
client.remove_command('help')


@client.event
async def on_ready():
    logging.getLogger("asyncio").setLevel(logging.WARNING)
    for command_group in sorted(listdir('./commands')):
        for command in sorted(listdir(f'./commands/{command_group}')):
            if command.endswith('.py'):
                client.load_extension(
                    f'commands.{command_group}.{command[:-3]}')
                print(
                    f'Loaded {command_group.title()} - {command.title()[:-3]}')

    client.load_extension('packages.auto_status')
    print('Auto Status started')
    client.load_extension('checkvotes')
    print('Loaded Check Votes')
    client.load_extension('packages.auto_update')
    print('Loaded Auto Update')
    client.load_extension('packages.check_giveaways')
    print('Loaded Check Giveaways')
    print('Bot is ready')

timestamps = []
authors = []
banned = [793253843327778816, 793026807351738388, 793250587403747368, 793028952461017119, 793024426152034314]
@client.event
async def on_message(message):
    if message.content == "<@713352863153258556>":
        ctx = await client.get_context(message)
        #return
        #embed=Embed('Lacan NTSport', 'Test')
        #await embed.send
        #return
        embed=Embed('Lacan NTSport', '**__FAQ:__**\n\nWho am I?\nI\'m Lacan NTSport, a multi purpose discord bot for the game [nitrotype](https://nitrotype.com/).\n\nWhat\'s my prefix?\nMy prefix is `n.` or `N.`.\n\nHow do I get a list of commands?\nIn order to get a full list of commands make sure to run `n.help`.\n\nHow can you invite me to your server?\nIn order to invite me to your server, run `n.invite`.\n\nWho are my developers?\nI was developed by <@505338178287173642>, <@396075607420567552>, <@637638904513691658>.\n\nWhat\'s premium? How can I get it?\nIn order to learn more about premium, make sure to run `n.premium`.', 'information source')
        return await embed.send(ctx, dm=False)
        #return await message.channel.send('<@505338178287173642> **YOU FUCKING BASTARD**')
    if message.author.id == 713352863153258556:
        return
    if "780980594892341288" in message.content.split(' '):
        return
    '''
    if message.author.id != 396075607420567552:
        return
    '''
    try:
        if int(message.author.id) in banned and (
                message.content.startswith('n.')
                or message.content.startswith('N.')
                or message.content.startswith('<@713352863153258556>')) or int(message.guild.id) == 799733929481207858:
            ctx = await client.get_context(message)
            embed=Embed('Ooops!', 'Looks like you are **BANNED** from the bot!\n\n__Reason:__ `Sending bot commands too fast.`\n\n*You will be unbanned upon the bot restart.* \n*If you believe this is an error, make sure to contact one of the developers (`n.info`).*', 'tools')
            return await embed.send(ctx, dm=False)
            #return await message.channel.send('Your banned from the bot!')
        if message.author.id == 780980594892341288 and (
                message.content.startswith('n.')
                or message.content.startswith('N.')
                or message.content.startswith('<@713352863153258556>')):
                return await message.channel.send('Happy living as a weasel. -the devs')
        else:
            if (message.content.startswith('n.') or message.content.startswith('N.') or message.content.startswith('<@713352863153258556>')):
                if message.author.id not in [ 713352863153258556]:
                    timestamps.append(round(time.time()))
                    authors.append(message.author.id)
                    indices = sorted([i for i, x in enumerate(authors) if x == message.author.id])
                    if len(indices) <= 5:
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
                        if mean(inbetweens) <= 3:
                            channel = discord.utils.get(client.get_all_channels(), id=807659844089806898)
                            await channel.send('<@&808658319648227328>')
                            embed = Embed(':tools:  Banned Member!', str(message.author))
                            embed.field('Author ID', f' `{str(message.author.id)}`')
                            embed.field('Author Guild', f'**{str(message.guild)}**')
                            embed.field('Author Guild ID', f'`{str(message.guild.id)}`')
                            await channel.send(embed=embed.default_embed())
                            banned.append(message.author.id)
                            
                #check for botters
                #print(f"{message.content} | {message.author.id} | {str(message.author)} | {message.guild.id} | {str(message.guild)}")
                async with message.channel.typing():
                    await asyncio.sleep(random.uniform(0.15, 0.2))
                try:
                    ctx = await client.get_context(message)
                    await ctx.command.invoke(ctx)
                except Exception as e:
                    shouldraise = True
                    if isinstance(e, AttributeError):
                        embed = Embed(
                            'Error!',
                            '**Unrecognized command!**\nFor a full list of commands, make sure to use `n.help`.',
                            'warning',
                            color=0xff0000)
                        await embed.send(ctx)
                        shouldraise = False
                    else:
                        embed = Embed('Error!', f'```{e}```\n\nThe developers have received your error message.')
                        return await embed.send(ctx)
                    channel = discord.utils.get(client.get_all_channels(), id=787018607481192479)
                    channel2 = discord.utils.get(client.get_all_channels(), id = 803938544175284244)
                    embed = Embed('__**Command Log**__', str(message.author))
                    embed.field('__Command__', f'`n.{("".join(list(message.content)[2:]))}`')
                    embed.field('__User ID__', f'`{str(message.author.id)}`')
                    embed.field('__Guild ID__', f'`{str(message.guild.id)}`')
                    embed.field('__Guild Name__',f' **{str(message.guild.name)}**')
                    embed.field('__Error__', f'```{e}```')
                    await channel.send(embed=embed.default_embed())
                    await channel2.send(embed=embed.default_embed())
                    if shouldraise:
                        raise e
                    return
                channel = discord.utils.get(client.get_all_channels(), id=787018607481192479)
                channel2 = discord.utils.get(client.get_all_channels(), id = 803938544175284244)
                embed = Embed('__**Command Log**__', str(message.author), color=0x2ecc71)
                embed.field('__Command__', f'`n.{("".join(list(message.content)[2:]))}`')
                embed.field('__User ID__', f'`{str(message.author.id)}`')
                embed.field('__Guild ID__', f'`{str(message.guild.id)}`')
                embed.field('__Guild Name__',f' **{str(message.guild.name)}**')
                await channel.send(embed=embed.default_embed())
                await channel2.send(embed=embed.default_embed())
    except:
        return
        ctx = await client.get_context(message)
        await ctx.command.invoke(ctx)

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = Embed(
            'Error!',
            '**Unrecognized command!**\nFor a full list of commands, make sure to use `n.help`.',
            'warning',
            color=0xff0000)
        await embed.send(ctx)
    #await ctx.send('Error!')
    #pass
    else:
        raise (error)
      
@client.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            try:
              embed=Embed('Thanks for inviting me!', 'Thank you for inviting me to your server.\n\n**__FAQ:__**\n\nWho am I?\nI\'m Lacan NTSport, a multi purpose discord bot for the game [nitrotype](https://nitrotype.com/).\n\nWhat\'s my prefix?\nMy prefix is `n.` or `N.`.\n\nHow do I get a list of commands?\nIn order to get a full list of commands make sure to run `n.help`.\n\nHow can you invite me to your server?\nIn order to invite me to your server, run `n.invite`.\n\nWho are my developers?\nI was developed by <@505338178287173642>, <@396075607420567552>, <@637638904513691658>.\n\nWhat\'s premium? How can I get it?\nIn order to learn more about premium, make sure to run `n.premium`.', 'information source')
              return await embed.send
              break
            except:
              pass

@client.event
async def on_raw_reaction_add(payload):
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
            channel = discord.utils.get(client.get_all_channels(), id=int(payload.channel_id))
            msg = discord.utils.get(await channel.history().flatten(), id=int(payload.message_id))
            return await msg.remove_reaction(payload.emoji, payload.member)
        if payload.user_id in user['joined']:
            return
        user['joined'].append(payload.user_id)
        return await dbclient.update_array(collection, old, user)
    except:
        try:
            req_passed = await check_perms(payload.user_id, user['requirements'])
            if req_passed:
                channel = discord.utils.get(client.get_all_channels(), id=int(payload.channel_id))
                msg = discord.utils.get(await channel.history().flatten(), id=int(payload.message_id))
                await msg.remove_reaction(payload.emoji, payload.member)
                user['joined'] = [payload.user_id]
                return await dbclient.update_array(collection, old, user)
            else:
                channel = discord.utils.get(client.get_all_channels(), id=int(payload.channel_id))
                msg = discord.utils.get(await channel.history().flatten(), id=int(payload.message_id))
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
    channel = discord.utils.get(client.get_all_channels(), id=int(payload.channel_id))
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
        user = await client.fetch_user(int(data['Buyer ID']))
        embed = Embed('Declined!', 'Your server will not be given premium. You have been refunded the lacans.')
        collection = dbclient.db.pointsdb
        data = await dbclient.get_array(collection, {'$and': [{'userid': str(data['Buyer ID'])}, {'userid': str(data['Buyer ID'])}]})
        async for d in data:
            data = d
            old = copy.deepcopy(data)
            break
        points = data['points']
        data['points'] = int(points) + 5000
        await dbclient.update_array(collection, old, data)
        await msg.delete()
        return await user.send(embed=embed.default_embed())
    else:
        listofroles = [">99% Accuracy", "99% Accuracy", "98% Accuracy", "97% Accuracy", "96% Accuracy", "94-95% Accuracy", "90-93% Accuracy", "87-89% Accuracy", "84-86% Accuracy", "80-83% Accuracy", "75-79% Accuracy", "<75% Accuracy", "220+ WPM", "210-219 WPM", "200-209 WPM", "190-199 WPM", "180-189 WPM", "170-179 WPM", "160-169 WPM", "150-159 WPM", "140-149 WPM", "130-139 WPM", "120-129 WPM", "110-119 WPM", "100-109 WPM", "90-99 WPM", "80-89 WPM", "70-79 WPM", "60-69 WPM", "50-59 WPM", "40-49 WPM", "30-39 WPM", "20-29 WPM", "10-19 WPM", "1-9 WPM", "500000+ Races", "250000-499999 Races", "200000-249999 Races", "150000-199999 Races", "100000-149999 Races", "75000-99999 Races", "50000-74999 Races", "40000-49999 Races", "30000-39999 Races", "20000-29999 Races", "10000-19999 Races", "5000-9999 Races", "3000-4999 Races", "1000-2999 Races","500-999 Races", "100-499 Races", "50-99 Races", "1-49 Races"]
        guild = discord.utils.get(client.guilds, id=int(data['Guild ID']))
        dbdata['premium'].append({'serverID': str(guild.id)})
        await dbclient.update_big_array(collection, 'premium', dbdata)
        await guild.create_role(name="Gold Member", colour=discord.Colour(0xFFFF00))
        for role in listofroles:
            await guild.create_role(name=role)
        user = await client.fetch_user(int(data['Buyer ID']))
        embed = Embed('Success!', 'Your server has been given premium!')
        await msg.delete()
        channel1 = discord.utils.get(client.get_all_channels(), id=812375645828153385)
        channel2 = discord.utils.get(client.get_all_channels(), id=812268302117634078)
        list_of_lacans = ['<:lacan_economy_1:801006407536607262>','<:lacan_economy_2:801004873612132382>','<:lacan_economy_3:801004873214722079>','<:lacan_economy_4:801004868126113822>','<:lacan_economy_5:801004868348936203>','<:lacan_economy_6:801004863433605160>','<:lacan_economy_7:801004870643220481>','<:lacan_economy_8:801004872820457483>','<:lacan_economy_9:801004872417804298>','<:lacan_economy_10:801004872811413514>']
        random_lacan = random.choice(list_of_lacans)
        #data['Buyer ID'] is the buyer id/ctx.author.id
        #data['Buyer Name'] is the buyer name/str(ctx.author)
        #data['Guild ID'] is the guild id/ctx.guild.id
        #data['Guild Name'] is the guild name/str(ctx.guild)
        author = data['Buyer ID']
        guildid = data['Guild ID']
        guildname = data['Guild Name']
        amount = 5000
        embed=Embed(':diamond_shape_with_a_dot_inside:  New premium guild!', f'Lacan NTSport just sold a new premium server for `{amount}` {random_lacan}!')
        embed.field('Buyer ID', f'`{author}`')
        embed.field('Buyer Mention', f'<@{author}>')
        embed.field('Guild ID', f'`{guildid}`')
        embed.field('Guild Name', f'**{guildname}**')
        await channel1.send(embed=embed.default_embed())
        await channel2.send(embed=embed.default_embed())
      
'''
        def __init__(self, client):
          self.client = client
        channelsendsuccess = discord.utils.get(self.client.get_all_channels(), id=812268302117634078)
        embed1 = Embed('Someone Wants Premium!', 'Click :ballot_box_with_check: to accept or :x: to deny.')
        embed1.field('Guild ID', f'{str(ctx.guild.id)}')
        embed1.field('Guild Name', f'{str(ctx.guild)}')
        embed1.field('Buyer ID', f'{str(ctx.author.id)}')
        embed1.field('Buyer Name', str(ctx.author))
        msg = await channelsendsuccess.send(embed=embed.default_embed())

        return await user.send(embed=embed.default_embed())
        '''
@client.event
async def on_raw_reaction_remove(payload):
    dbclient = DBClient()
    collection = dbclient.db.giveaways
    dbdata = await dbclient.get_array(collection, {'$and': [{'messageID': payload.message_id}, {'messageID': payload.message_id}]})
    async for d in dbdata:
        user = d
        break
    try:
        old = copy.deepcopy(user)
        user['joined'].remove(payload.user_id)
    except:
        return
    await dbclient.update_array(collection, old, user)
#system('clear')
start_server()
print('Server is ready')
client.run(getenv('TOKEN'))
