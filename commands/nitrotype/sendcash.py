'''Send Nitrotype cash to a user'''
import json, requests, re, asyncio
from discord.ext import commands
from bs4 import BeautifulSoup
from cryptography.fernet import Fernet
import os
from mongoclient import DBClient
from packages.utils import Embed
from nitrotype import NT_to_discord
import urllib.parse
class Command(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def get_user_id(self, racer):

        newdata = {}
        response = requests.get(
            f'https://www.nitrotype.com/racer/{racer}').content
        soup = BeautifulSoup(response, 'html5lib')
        for script in soup.find('head'):
            if 'RACER_INFO' in str(script):
                newdata = json.loads(re.findall('{".+}', str(script))[0])
                newdata = json.loads(re.findall('{".+}', str(script))[0])
        if newdata == {}:
            self.success = False
            return
        return newdata['userID']
    async def decrypt(self, message, key=os.getenv('encrypt_key')):
        """
        Encrypts a message
        """
        encoded_message = message.encode()
        f = Fernet(key)
        encrypted_message = f.decrypt(encoded_message)

        return (encrypted_message.decode())
    async def get_user_cred(self, userid):
        dbclient = DBClient()
        collection = dbclient.db.NT_to_discord
        data = await dbclient.get_big_array(collection, 'registered')
        for user in data['registered']:
            if user['userID'] == str(userid):
                return user['NTuser'], await self.decrypt(user['password'])

    async def sendto_func(self, sendto):
        sendto = list(str(sendto))
        if ''.join(sendto[:3]) == "<@!":
            return await NT_to_discord(''.join(sendto[3:-1]))
        if ''.join(sendto[:2]) == "<@":
            return await NT_to_discord(''.join(sendto[2:-1]))
        if len(sendto) in [17, 18]:
            return await NT_to_discord(''.join(sendto))
        else:
            return sendto
    @commands.command()
    async def sendcash(self, ctx, sendto=None, amount=None):
      if ctx.message.guild.id in [564880536401870858]:
        embed=Embed('Error!', 'This server has been **blacklisted** from using this command.', 'warning')
        await embed.send(ctx)
        print('not permitted in this server')
        return
      else:
        if not sendto or not amount:
            #embed = Embed('Make sure to send an amount of money to a person! `n.sendcash [NT username] [amount]`')
            #await embed.send(ctx)
            await ctx.send(
                'Make sure send an amount of money to a person! `n.sendcash [NT username] [amount]`'
            )
            return
        sendto = await self.sendto_func(sendto)
        if sendto[0] == False:
            return await sendto[1].send(ctx)
        else:
            try:
                sendto = sendto[1].username
            except:
                sendto = sendto[1]
        amount = amount.replace('k', '000').replace('m', '000000')
        creds = await self.get_user_cred(ctx.author.id)
        if creds == None:
            embed = Embed('Error!', "You don't have a password connected to your account! Do it by running `n.password`!")
            return await embed.send(ctx)
        username = creds[0]
        password = creds[1]
        sendto_id = await self.get_user_id(sendto)
        if sendto_id == None:
            embed=Embed('Error!', 'Couldn\'t find the user you want to send to.', 'warning')
            await embed.send(ctx)
            #return await ctx.send(
                #'Couldn\'t find the user you want to send to!')
        session = requests.Session()
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {'username': username, 'password': password}
        response = session.post('https://www.nitrotype.com/api/login',
                                data=data,
                                headers=headers).text
        response = json.loads(response)
        data = f"amount={amount}&password={urllib.parse.quote(password)}&playersCash={str(response['data']['money'])}&recipient={sendto_id}&feePercent=0&uhash={session.cookies['ntuserrem']}"
        response2 = session.post(
            f'https://www.nitrotype.com/api/friends/{sendto_id}/sendcash',
            data=data,
            headers=headers).text
        response2_json = json.loads(response2)
        success = response2_json['success']
        if not success:
            try:
                await ctx.send(response2_json['data']['password'])
            except:
                await ctx.send(
                    'An unknown error occurred. Please try again.')
        else:
            embed=Embed('Success!',f'{ctx.author.mention}just sent `{sendto}` **{amount}** NT cash!', 'white check mark')
            await embed.send(ctx)


def setup(client):
    client.add_cog(Command(client))
