#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Lacan NTSport
~~~~~~~~~~~~~
A discord bot designed for those interested in NitroType
:copyright: (c) 2021 Try2Win4Glory
:license: GNU General Public License v3.0, see LICENSE.md for more details
'''

__title__ = 'Lacan NTSport'
__version__ = 'Full'
__author__ = 'SystematicError, Typerious, Try2Win4Glory, adl212'
__copyright__ = 'Copyright 2021 Try2Win4Glory'
__license__ = 'GNU General Public License v3.0'

# --- Start Code --- #
from discord.ext import commands
from os import listdir, getenv
import logging
import discord


intents = discord.Intents().default()
client = commands.Bot(command_prefix=commands.when_mentioned_or(*['N.', 'n.', '<@!713352863153258556>', '<@713352863153258556>']), case_insensitive=True, intents=intents)
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
    print('Loading Events')
    for event in sorted(listdir('./events')):
        if event.endswith('.py'):
            client.load_extension('events.'+event[:-3])
            print('Loaded Event on_'+event[:-3])
    print('Bot is ready')

from discord.ext import tasks
@tasks.loop(hours=1)
async def clear_cache():
  client.clear()
clear_cache.start()

if __name__ == '__main__':
    #start_server()
    print('Server is ready')
    client.run(getenv('TOKEN'))