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
        
        dbclient = DBClient()
        pcollection = dbclient.db.premium
        pdata = await dbclient.get_big_array(pcollection, 'premium')
        for server in pdata['premium']:
            rolelist = []
            #if str(member.guild.id) == server['serverID']:
            supportedservers = [719414661686099989, 763774963102122014]
            if str(member.guild.id) in supportedservers:
                try:
                    try:
                        role = get(member.guild.roles, name='Registered')
                        await member.add_roles(role)
                        rolelist.append(role)
                    except Exception as e:
                        print(e)
                        
                    try:
                        role = get(member.guild.roles, name=speed)
                        await member.add_roles(role)
                        rolelist.append(role)
                    except Exception as e:
                        print(e)

                    try:
                        role = get(member.guild.roles, name=races)
                        await member.add_roles(role)
                        rolelist.append(role)
                    except Exception as e:
                        print(e)

                    try:
                        try:
                            role = get(member.guild.roles, name=gold)
                            await member.add_roles(role)
                            rolelist.append(role)
                        except:
                            gold = racer.classic_gold_role
                            role = get(member.guild.roles, name=gold)
                            await member.add_roles(role)
                            rolelist.append(role)
                    except Exception as e:
                        print(e)
                        
                        
                    #OTHER ROLES
                    # NT Server Category Roles
                    roles_to_add = []
                    if member.guild.id in [564880536401870858]:
                        role = get(member.guild.roles, id=654804415747850241)
                        roles_to_add.append(role)
                        role = get(member.guild.roles, id=654801298297847838)
                        roles_to_add.append(role)
                        role = get(member.guild.roles, id=654802074034503681)
                        roles_to_add.append(role)
                        rolelist.append('Category Roles')

                    # Other Fun Roles  
                    try:
                        if int(racer.created_timestamp) <= 1430172000:
                                role = get(member.guild.roles, name="v1 Veteran")
                                if role != None:
                                    roles_to_add.append(role)
                                    rolelist.append(role)
                    except:
                        pass
                    try:
                        if int(racer.created_timestamp) > 1430172000 and racer.created_timestamp <= 1559685600:
                                role = get(member.guild.roles, name="v2 Veteran")
                                if role != None:
                                    roles_to_add.append(role)
                                    rolelist.append(role)
                    except:
                        pass
                    try:
                        if int(racer.longest_session_sessionist) >= 800:
                                role = get(member.guild.roles, name="Sessionist")
                                if role != None:
                                    roles_to_add.append(role)
                                    rolelist.append(role)
                    except:
                        pass

                    try:
                        if int(racer.popular_views) >= 10000:
                            role=get(member.guild.roles, name="Popular")
                            if role != None:
                                roles_to_add.append(role)
                                rolelist.append(role)
                    except:
                        pass
                    
                    #Other fun roles
                    try:
                        if int(racer.nitro_enthusiast) >= 10000:
                            role = get(member.guild.roles, name="Nitro Enthusiast")
                            if role != None:
                                roles_to_add.append(role)
                                rolelist.append(role)
                    except:
                        pass
                    try:
                        if int(racer.car_collector) >= 200:
                            role = get(member.guild.roles, name="Car Collector")
                            if role != None:
                                roles_to_add.append(role)
                                rolelist.append(role)
                    except:
                        pass
                    try:
                        if int(racer.high_speed)-int(racer.average_speed) >= 50:
                            role = get(member.guild.roles, name="Undulation Master")
                            if role != None:
                                roles_to_add.append(role)
                                rolelist.append(role)
                    except:
                            pass
                    try:
                        if int(racer.high_speed)-int(racer.average_speed) <= 25:
                            role = get(member.guild.roles, name="Try Hard")
                            if role != None:
                                roles_to_add.append(role)
                                rolelist.append(role)
                    except:
                        pass
            
                    try:
                        await member.add_roles(*roles_to_add)
                    except:
                        pass
                    
                    oldnick = member.display_name
                    
                    try:
                        await member.edit(nick=racer.tag+' ' +racer.name)
                    except:
                        pass
                    
                    newnick = member.display_name

                    autochannel = discord.utils.get(self.client.get_all_channels(), id=channel_id)
                    embed=Embed(':white_check_mark:  Updated Member', f'{member.mention}\'s roles were automatically updated upon joining.\nThey are currenty linked to **[{username}](https://nitrotype.com/racer/{username})**.\n\nNickname: {oldnick} :arrow_right: {newnick}\n__Added:__\n```{rolelist[name]}```')
                    await autochannel.send(embed=embed.default_embed())
                except:
                    pass
                
        try:
            embed=Embed(f'Welcome to the server! :wave:', message)
            await channel.send(embed=embed.default_embed())
        except:
            embed=Embed('Welcome to the server! :wave:', f'{member.mention} unfortunately isn\'t associated to a Nitro Type account yet. Please type `n.register` to start the registration process.')
            await channel.send(embed=embed.default_embed())

def setup(client):
    client.add_cog(Events(client))
