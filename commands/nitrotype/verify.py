'''Verify your account ownership after registering!'''
from discord.ext import commands
from packages.utils import Embed, ImproperType
from packages.nitrotype import Racer, cars
import requests
import os
import json
import random, copy
from mongoclient import DBClient
from nitrotype import verify, verify_race, verify_friend, verify_link, verify_switch
import aiohttp
import cloudscraper
import asyncio
import functools
import time
try:
    from dotenv import load_dotenv

    load_dotenv()
except:
    pass
class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    async def fetch(self, session, url, method='POST', data=None):
        if method == 'POST':
            async with session.post(url, data=data) as response:
                return await response.text()
        if method == 'GET':
            async with session.get(url) as response:
                return await response.text()
    @commands.command()
    async def verify(self, ctx, type="friend"):
        #return await ctx.send('This command is currently under maintenance. The developers will try to get it up again as soon as possible. In the meantime feel free to use `n.help` to get the other commands. Thank you for your understanding!')
        if type == 'car':
            return await verify(ctx)
        if type == 'race':
            return await verify_race(ctx)
        if type == 'switch':
            return await verify_switch(ctx)
        if type == 'friend':
            return await verify_friend(ctx)
        else:
            return await verify_friend(ctx)
def setup(client):
    client.add_cog(Command(client))
