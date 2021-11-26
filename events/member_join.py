from discord.ext import commands
from packages.utils import Embed
from mongoclient import DBClient
from discord.utils import get
import discord
from nitrotype import NT_to_discord
class Events(commands.Cog):
    def __init__(self, client):
        self.client = client
    @commands.Cog.listener('on_member_join')
    async def event(self, member):
        dbclient = DBClient()
        collection = dbclient.db.servers
        server = await dbclient.get_array(collection, {'serverID': member.guild.id})
        try:
            async for x in server:
                data = x
                break
        except:
            return
        try:
            print(data)
            channel_id = data['channel_id']
            channel = discord.utils.get(self.client.get_all_channels(), id=channel_id)
            message = data['message']
        except:
            return
        try:
            racer = await NT_to_discord(member.id)
            racer = racer[1]
            username = racer.username
            speed = racer.speed_role
            #accuracy = racer.accuracy_role
            races = racer.race_role
            if racer.gold_role == None:
                gold = 'Basic'
            else:
                gold = racer.gold_role
        #except Exception as e:
            #print(e)
        except:
            embed=Embed('Welcome to the server! :wave:', f'{member.mention} unfortunately isn\'t associated to a Nitro Type account yet. Please type `n.register` to start the registration process.')
            return await channel.send(embed=embed.default_embed())
        message = message.replace('{{user.mention}}', member.mention)
        message = message.replace('{{user.id}}', str(member.id))
        message = message.replace('{{user.racer.username}}', username)
        message = message.replace('{{user.racer.speed}}', speed)
        #message = message.replace('{{user.racer.accuracy}}', accuracy)
        message = message.replace('{{user.racer.races}}', races)
        message = message.replace('{{user.gold}}', gold)
        embed=Embed(f'Welcome to the server! :wave:', message)
        
        dbclient = DBClient()
        pcollection = dbclient.db.premium
        pdata = await dbclient.get_big_array(pcollection, 'premium')
        for server in pdata['premium']:
            if str(member.guild.id) == server['serverID']:
                roles_to_add=[]
        
                try:
                    role = get(member.guild.roles, name=speed)
                    await roles_to_add.append(role)
                except Exception as e:
                    print(e)

                try:
                    role = get(member.guild.roles, name=races)
                    await roles_to_add.append(role)
                except Exception as e:
                    print(e)

                try:
                    role = get(member.guild.roles, name=gold)
                    await roles_to_add.append(role)
                except Exception as e:
                    print(e)

                await member.add_roles(*roles_to_add)
                
                autochannel = discord.utils.get(self.client.get_all_channels(), id=channel_id)
                embed=Embed(':white_check_mark: Updated Member', f'{member.mention}\'s roles were automatically updated upon joining.')
                return await autochannel.send(embed=embed.default_embed())
        
        try:
            await channel.send(embed=embed.default_embed())
        except:
            embed=Embed('Welcome to the server! :wave:', f'{member.mention} unfortunately isn\'t associated to a Nitro Type account yet. Please type `n.register` to start the registration process.')
            return await channel.send(embed=embed.default_embed())
def setup(client):
    client.add_cog(Events(client))
