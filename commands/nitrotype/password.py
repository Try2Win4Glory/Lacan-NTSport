'''Set a password for your NT account'''

from discord.ext import commands
from packages.utils import Embed, ImproperType
from mongoclient import DBClient
from nitrotype import get_username
from collections.abc import Sequence
import asyncio, os
from cryptography.fernet import Fernet
class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    def make_sequence(self, seq):
        if seq is None:
            return ()
        if isinstance(seq, Sequence) and not isinstance(seq, str):
            return seq
        else:
            return (seq,)
    def encrypt(self, message, key=os.getenv('encrypt_key')):
        """
        Encrypts a message
        """
        encoded_message = message.encode()
        f = Fernet(key)
        encrypted_message = f.encrypt(encoded_message)

        return (encrypted_message.decode())
    def message_check(self, channel=None, author=None, content=None, ignore_bot=True, lower=True):
        channel = self.make_sequence(channel)
        author = self.make_sequence(author)
        content = self.make_sequence(content)
        if lower:
            content = tuple(c.lower() for c in content)
        def check(message):
            if ignore_bot and message.author.bot:
                return False
            if channel and message.channel not in channel:
                return False
            if author and message.author not in author:
                return False
            actual_content = message.content.lower() if lower else message.content
            if content and actual_content not in content:
                return False
            return True
        return check
    @commands.command()
    async def password(self, ctx):
        
        var = await get_username(str(ctx.author.id))
        if var[0] == False:
            return await var[1].send(ctx)
        #embed=Embed('Password', 'Please enter your password **without** prefix below.')
        #await ctx.author.send(embed=embed.default_embed())
        await ctx.author.send('What is your password?')
        try:
            response = await self.client.wait_for('message', check=self.message_check(channel=ctx.author.dm_channel), timeout=30)
        except asyncio.exceptions.TimeoutError:
            return await ctx.author.send("You didn't type your password in time!")
        dbclient = DBClient()
        collection = dbclient.db.NT_to_discord
        data = await dbclient.get_array(collection, {'$or': [{'userID': str(ctx.author.id), 'NTuser': var[1].username.lower()}]})
        async for user in data:
            old = user.copy()
            user['password'] = self.encrypt(response.content)
        await dbclient.update_array(collection, old, user)
        thepassword = (response.content)
        username = user['NTuser']
        embed = Embed('Success!', f"Your password for your account `{username}` was successfuly set to `{thepassword}`, encrypted and added into the database!\n\n__Your Data:__\nusername: `{user['NTuser']}`\npassword: `{thepassword}` \n\n__Please note that:__ \n*1. This password is **safe**, it doesn't even exist unencrypted anymore.*\n*2. Wrong use of this command like putting wrong data into the bot on purpose can end in a **ban** of this bot as our database does not have enough space for wrong data.*", 'white check mark')
        await embed.send(ctx, dm=True)
        #embed = Embed('Success!', f"Your password for your account `user['NTuser']` was successfuly set to `{user['password']}`, encrypted and added into the database!")
        #embed=Embed('Success!', "Your password was successfully added into the database!", 'white check mark')
        #await embed.send(ctx, dm=True)

        
def setup(client):
    client.add_cog(Command(client))