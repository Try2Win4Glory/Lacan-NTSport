'''Add a custom welcome Message to your server'''

from discord.ext import commands
from packages.utils import Embed, ImproperType
from mongoclient import DBClient
import discord
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
    async def welcome(self, ctx):
        has_perm = False
        if ctx.author.guild_permissions.manage_guild:
            has_perm = True
        elif ctx.author.guild_permissions.administrator:
            has_perm = True
        elif ctx.author.id == 505338178287173642:
            has_perm = True
        if has_perm == False:
            embed = Embed(':warning:  Error!', 'Seems like you don\'t have the permission to use this command.\n\nThis command requires administrator or manage server perms.')
            return await embed.send(ctx)
        dbclient = DBClient()
        collection = dbclient.db.servers
        data = await dbclient.get_array(collection, {'serverID': ctx.guild.id})
        try:
            for x in data:
                server_exists = True
                server_data = x
                break
        except:
            server_exists = False
            server_data = {}
            pass
        server_data['serverID'] = ctx.guild.id
        embed = Embed('Welcoming Message: Step 1 - Channel', 'In what channel do you want the message to be sent to?')
        embed.field('__Instructions:__', 'Type in a channel ID or mention of the channel where the message should be sent!\n\n*Example response: **#welcome***')
        await embed.send(ctx)
        msg = await self.wait_for_msg(ctx)
        if msg[0] == False:
            return await msg[1].send(ctx)
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
        c = discord.utils.get(ctx.guild.channels, id=int(channel))
        server_data['channel_id'] = c.id
        embed = Embed('Welcoming Message: Step 2 - Message', 'What message should be sent?')
        embed.field('__Instructions:__', 'Type in a message including variables to create your own custom welcoming system!')
        embed.field('__Variables:__', 'Put `{{` and `}}` around text to define a variable.')
        embed.field('__Types Of Variables:__', '`user.mention`, `user.id`, `user.racer.username`, `user.racer.speed`, `user.racer.accuracy`, `user.racer.races`, `user.racer.membership')
        embed.field('__Example:__', '{{user.mention}} has joined the server. :tada:\n\nThey are linked to {{user.racer.username}}.\n\nFollowing roles should be given:\n{{user.racer.races}}, {{user.racer.speed}}, {{user.racer.accuracy}}')
        await embed.send(ctx)
        msg = await self.wait_for_msg(ctx)
        if msg[0] == False:
            return await msg[1].send(ctx)
        else:
            msg = msg[1]
        server_data['message'] = msg.content
        embed = Embed('Your Welcoming System Is Complete!', 'YAY')
        embed.field('Channel', c.mention)
        embed.field('Message', msg.content)
        await embed.send(ctx)
        
        if server_exists:
            await dbclient.update_array(collection, {'serverID': ctx.guild.id}, server_data)
        else:
            await dbclient.create_doc(collection, server_data)
def setup(client):
    client.add_cog(Command(client))
