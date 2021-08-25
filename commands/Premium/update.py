'''Update your role and nick (premium only)'''

from discord.ext import commands
from packages.utils import Embed, ImproperType
from discord.utils import get
from packages.nitrotype import Racer
import packages.nitrotype
import requests, json, os
import datetime
from datetime import date
import random
from mongoclient import DBClient
from nitrotype import get_username
class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def update(self, ctx):
        #return await ctx.send('This command is currently under maintenance. The developers will try to get it up again as soon as possible. In the meantime feel free to use `n.help` to get the other commands. Thank you for your understanding!')
      #Define Time variables
        #Variables = date(year, month, day)
        d1 = date(2021, 4, 1)
        dcurrent = date.today()

        thelistofroles = ["Gold Member", [">99% Accuracy", "99% Accuracy", "98% Accuracy", "97% Accuracy", "96% Accuracy", "94-95% Accuracy", "90-93% Accuracy", "87-89% Accuracy", "84-86% Accuracy", "80-83% Accuracy", "75-79% Accuracy", "<75% Accuracy"], ["220+ WPM", "210-219 WPM", "200-209 WPM", "190-199 WPM", "180-189 WPM", "170-179 WPM", "160-169 WPM", "150-159 WPM", "140-149 WPM", "130-139 WPM", "120-129 WPM", "110-119 WPM", "100-109 WPM", "90-99 WPM", "80-89 WPM", "70-79 WPM", "60-69 WPM", "50-59 WPM", "40-49 WPM", "30-39 WPM", "20-29 WPM", "10-19 WPM", "1-9 WPM"], ["500000+ Races", "250000-499999 Races", "200000-249999 Races", "150000-199999 Races", "100000-149999 Races", "75000-99999 Races", "50000-74999 Races", "40000-49999 Races", "30000-39999 Races", "20000-29999 Races", "10000-19999 Races", "5000-9999 Races", "3000-4999 Races", "1000-2999 Races","500-999 Races", "100-499 Races", "50-99 Races", "1-49 Races"]]
        listofroles = ["Gold Member", ">99% Accuracy", "99% Accuracy", "98% Accuracy", "97% Accuracy", "96% Accuracy", "94-95% Accuracy", "90-93% Accuracy", "87-89% Accuracy", "84-86% Accuracy", "80-83% Accuracy", "75-79% Accuracy", "<75% Accuracy", "220+ WPM", "210-219 WPM", "200-209 WPM", "190-199 WPM", "180-189 WPM", "170-179 WPM", "160-169 WPM", "150-159 WPM", "140-149 WPM", "130-139 WPM", "120-129 WPM", "110-119 WPM", "100-109 WPM", "90-99 WPM", "80-89 WPM", "70-79 WPM", "60-69 WPM", "50-59 WPM", "40-49 WPM", "30-39 WPM", "20-29 WPM", "10-19 WPM", "1-9 WPM", "500000+ Races", "250000-499999 Races", "200000-249999 Races", "150000-199999 Races", "100000-149999 Races", "75000-99999 Races", "50000-74999 Races", "40000-49999 Races", "30000-39999 Races", "20000-29999 Races", "10000-19999 Races", "5000-9999 Races", "3000-4999 Races", "1000-2999 Races","500-999 Races", "100-499 Races", "50-99 Races", "1-49 Races"]
        achievementroles = ['"I < 3 Typing"', '"I Really Love Typing!"', '"Bonkers About Typing"', '"Bananas About Typing"', '"You\'ve Gotta Be Kidding"', '"Corsair"', '"Pirc"', '"Carrie"', '"Anne"', '"Lackin\' Nothin\'"', '"Outback Officer"', '"I Love Shoes 2"', '"I Love Shoes 12.5"', '"I Love Shoes 15.0"', '"I Love Shoes 20.0"', '"The Wildest of Flowers"', '"The Wild Legend"']
        teamswithroles = [
          # Insert Global Team Tags Here
        ]

        #Team N8TE | Server Owner: 630761745140547625
        if ctx.guild.id in [
          636582509429260289
        ]:
          teamswithroles.append('[N8TE]')
        #Team DRPT | Server Owner: 723224207651111003
        if ctx.guild.id in [
          742854336618561608
        ]:
          teamswithroles.append('[DRPT]')
        #Team RRN | Server Owner: 653772108815532053
        if ctx.guild.id in [
          696055942055198760
        ]:
          teamswithroles.append('[RRN]')
        #Team NEWS | Server Owner: 272370019894165505
        if ctx.guild.id in [
          835305919679692850
        ]:
          teamswithroles.append('[NEWS]')
        #Team TEST | Server Owner: 505338178287173642
        if ctx.guild.id in [
          833317505888026644
        ]:
          teamswithroles.append('[TEST]')
        #Team TBZ | Server Owner: 657296213087092756
        if ctx.guild.id in [
            857697272317345792
        ]:
            teamswithroles.append('[TBZ]')
        #Team SSH | Server Owner: 363082908270985217
        if ctx.guild.id in [
            788547373701136425
        ]:
            teamswithroles.append('[SSH]')
          #Team NYM | Server Owner: 714147755974721556
        if ctx.guild.id in [
            860954147342909440
        ]:
            teamswithroles.append('[NYM]')
        #Team 5TORM | Server Owner: 850880126979932180
        if ctx.guild.id in [
            862845786580582401
          ]:
            teamswithroles.append('[5TORM]')
        #Team RXV | Server Owner: 638050308899209247
        if ctx.guild.id in [
            747188472661540884
        ]:
            teamswithroles.append('[RXV]')
        #data = requests.get('https://test-db.nitrotypers.repl.co', data={"key": os.getenv('DB_KEY')}).text
        #data = json.loads(data)
        dbclient = DBClient()
        pcollection = dbclient.db.premium
        pdata = await dbclient.get_big_array(pcollection, 'premium')
        for server in pdata['premium']:
            if str(ctx.author.guild.id) == server['serverID']:
                break
        else:
            embed = Embed('Error!', 'Unfortunately, this isn\'t a premium server! Run `n.premium` to learn more about premium!', 'warning')
            
            if (ctx.author.id) not in [505338178287173642, 637638904513691658, 396075607420567552]:
              embed.footer('Become a premium 💠 member today!', 'https://media.discordapp.net/attachments/719414661686099993/765110312482766919/NT_Server_Halloween_Logo_2020_GIF.gif')

            else:
              embed.footer('Discord user '+str(ctx.author.name + '#' + ctx.author.discriminator)+' is a 🛠️developer🛠️ of this bot. \n⚙️This command is a premium 💠 only command.⚙️', 'https://media.discordapp.net/attachments/719414661686099993/765490220858081280/output-onlinepngtools_32.png')
            
            return await embed.send(ctx)
        roles_to_remove = []
        for role in (ctx.author.roles):
            name = role.name
            if name in listofroles or name in teamswithroles or name in achievementroles:
                role = get(ctx.message.guild.roles, id=role.id)
                roles_to_remove.append(role)
        print(roles_to_remove)
        await ctx.author.remove_roles(*roles_to_remove)
        success, ntuser = await get_username(str(ctx.author.id))
        if success:
            pass
        else:
            embed = Embed('Error!', 'Doesn\'t seem like you\'re registered!', 'warning')
            return await embed.send(ctx)
        racer = ntuser
        if ctx.author.id in []:
            roles_to_add = []
            #T2W4G's Speed Role
            listofroles = thelistofroles[2]
            role = get(ctx.message.guild.roles,
            name=listofroles[12])
            roles_to_add.append(role)
            #T2W4G's Accuracy Role
            listofroles = thelistofroles[1]
            role = get(ctx.message.guild.roles,
            name=listofroles[0])
            roles_to_add.append(role)
            #T2W4G's Races Role
            listofroles = thelistofroles[3]
            role = get(ctx.message.guild.roles,
            name=listofroles[8])
            roles_to_add.append(role)
            #T2W4G's Gold Member Role
            role = get(ctx.message.guild.roles, name="Gold Member")
            roles_to_add.append(role)
            #T2W4G's Registered Role
            role = get(ctx.message.guild.roles, name='Registered')
            roles_to_add.append(role)
            await ctx.author.add_roles(*roles_to_add)
            #Add role
            '''role = get(ctx.message.guild.roles, name='Moderator')
            await ctx.author.add_roles(role)
            #Remove role
            role = get(ctx.message.guild.roles, name='Admin')
            await ctx.author.remove_roles(role)'''
            #Remove Unregistered Role Try
            try:
              role = get(ctx.message.guild.roles, name='Unregistered')
              await ctx.author.remove_roles(role)
            except:
              pass  
            #T2W4G's Edit Nickname Try
            try:
                #T2W4G's Edit Nickname Success
                await ctx.author.edit(nick='⚡Try2Win4Glory⚡')
                #T2W4G's Edit Nickname Success Embed
                embed=Embed('Success!', 'Developer '+str(ctx.author.name + '#' + ctx.author.discriminator)+' \'s roles were updated. :-)', 'white check mark')
                #T2W4G's Embed Send
                await embed.send(ctx)
            except Exception:
                #T2W4G's Edit Nickname Fail
                embed = Embed('Rip!', 'I don\'t have the `Manage Nickames` permission! \n\nI updated your roles, but am missing the permission to change your nickname. :grinning:', 'poop')
                #T2W4G's Embed Send
                await embed.send(ctx)
            '''if str(racer.tag) in teamswithroles:
                print('yessir')
                try:
                    guild=ctx.author.guild
                    role = get(ctx.message.guild.roles, name=f'{racer.tag}')
                    await ctx.author.add_roles(role)
                    print('pog')
                    return
                except:
                    guild=ctx.author.guild
                    await guild.create_role(name=racer.tag)
                    role = get(ctx.message.guild.roles, name=f'{racer.tag}')
                    await ctx.author.add_roles(role)
                    print('created')
                    return
            else:
                #embed=Embed('Error!', 'Team tag: '+racer.tag+'', 'warning')
                #return await embed.send(ctx)
                 pass'''
            
            return
            
        else:
            roles_to_add = []
            role = get(ctx.message.guild.roles, name=racer.speed_role)
            roles_to_add.append(role)
            #role = get(ctx.message.guild.roles, name=racer.accuracy_role)
            #roles_to_add.append(role)
            try:
              role = get(ctx.message.guild.roles, name=racer.race_role)
              await ctx.author.add_roles(role)
            except:
              otherraceroles = ['"I < 3 Typing"', '"I Really Love Typing!"', '"Bonkers About Typing"', '"Bananas About Typing"', '"You\'ve Gotta Be Kidding"', '"Corsair"', '"Pirc"', '"Carrie"', '"Anne"', '"Lackin\' Nothin\'"', '"Outback Officer"', '"I Love Shoes 2"', '"I Love Shoes 12.5"', '"I Love Shoes 15.0"', '"I Love Shoes 20.0"', '"The Wildest of Flowers"', '"The Wild Legend"']
              print(otherraceroles)
              races = int(racer.races.replace(',', ''))
              print(races)
              if int(races) >= 500000:
                role = get(ctx.message.guild.roles, name=otherraceroles[16])
                roles_to_add.append(role)
              elif int(races) >= 250000:
                role = get(ctx.message.guild.roles, name=otherraceroles[15])
                roles_to_add.append(role)
              elif int(races) >= 200000:
                role = get(ctx.message.guild.roles, name=otherraceroles[14])
                roles_to_add.append(role)
              elif int(races) >= 150000:
                role = get(ctx.message.guild.roles, name=otherraceroles[13])
                roles_to_add.append(role)
              elif int(races) >= 125000:
                role = get(ctx.message.guild.roles, name=otherraceroles[12])
                roles_to_add.append(role)
              elif int(races) >= 100000:
                role = get(ctx.message.guild.roles, name=otherraceroles[11])
                roles_to_add.append(role)
              elif int(races) >= 75000:
                role = get(ctx.message.guild.roles, name=otherraceroles[10])
                roles_to_add.append(role)
              elif int(races) >= 50000:
                role = get(ctx.message.guild.roles, name=otherraceroles[9])
                roles_to_add.append(role)
              elif int(races) >= 40000:
                role = get(ctx.message.guild.roles, name=otherraceroles[8])
                roles_to_add.append(role)
              elif int(races) >= 30000:
                role = get(ctx.message.guild.roles, name=otherraceroles[7])
                roles_to_add.append(role)
              elif int(races) >= 20000:
                role = get(ctx.message.guild.roles, name=otherraceroles[6])
                roles_to_add.append(role)
              elif int(races) >= 10000:
                role = get(ctx.message.guild.roles, name=otherraceroles[5])
                roles_to_add.append(role)
              elif int(races) >= 5000:
                role = get(ctx.message.guild.roles, name=otherraceroles[4])
                roles_to_add.append(role)
              elif int(races) >= 1000:
                role = get(ctx.message.guild.roles, name=otherraceroles[3])
                roles_to_add.append(role)
              elif int(races) >= 500:
                role = get(ctx.message.guild.roles, name=otherraceroles[2])
                roles_to_add.append(role)
              elif int(races) >= 100:
                role = get(ctx.message.guild.roles, name=otherraceroles[1])
                roles_to_add.append(role)
              elif int(races) >= 0:
                role = get(ctx.message.guild.roles, name=otherraceroles[0])
                roles_to_add.append(role)
              print(role)
              print(roles_to_add)

            #roles_to_add.append(role)
            
            if racer.membership == 'gold': 
                role = get(ctx.message.guild.roles, name="Gold Member")
                await ctx.author.add_roles(role)

            role = get(ctx.message.guild.roles, name='Registered')
            try:
                await ctx.author.add_roles(role)

            except Exception:
                embed = Embed('Error!', 'The bot is not able to update your roles. Make sure I have the `Manage Roles` permission, am ranked higher than that roles and you did a season race yet.')
                await embed.send(ctx)
           #Teamroles
            if str(racer.tag) in teamswithroles:
                print('yessir')
                try:
                    guild=ctx.author.guild
                    role = get(ctx.message.guild.roles, name=f'{racer.tag}')
                    roles_to_add.append(role)
                    print('pog')
                except:
                    guild=ctx.author.guild
                    await guild.create_role(name=racer.tag)
                    role = get(ctx.message.guild.roles, name=f'{racer.tag}')
                    roles_to_add.append(role)
                    print('created')
            else:
                #embed=Embed('Error!', 'Team tag: '+racer.tag+'', 'warning')
                #return await embed.send(ctx)
                 pass
            #print(*roles_to_add)
            await ctx.author.add_roles(*roles_to_add)
            try:
              role = get(ctx.message.guild.roles, name='Unregistered')
              await ctx.author.remove_roles(role)
            except:
              pass     

            #Start of April Script
            if d1 == dcurrent:
              #The current date matches the specified date:
              print('Hehe april fools day')
              random_names = [
                'Huge Elephant',
                'Slimy Snail',
                'Fat Panda',
                'April Cat',
                'Silent Spy',
                'Lacan NTSport Developer',
                '10FF better than NT?',
                'April Joke',
                'Joker Typer',
                'Keyboard Pig',
                'Typing Nerd',
                'adl212 is cool',
                '⚡Try2Win4Glory⚡ is pog',
                'Lacan = Best Car',
                'I love Typerush.com!',
                'Whining Dog',
                'Potaytoes',
                'Chicken Typer',
                'Command Spammer',
                'The one and only',
                'I bot on NitroType!',
                'Ban me plz!',
                'Happy April fools day!']
              random_name = random.choice(random_names)
              try:
                await ctx.author.edit(nick='[APRIL] '+random_name+'')
                embed = Embed('Success!', 'Successfully updated your roles and nickname!', 'white_check_mark')
                embed.footer('Happy April fools day! :-)')
                return await embed.send(ctx)
              except Exception:
                embed = Embed('Error!', 'The bot needs following permissions: `Manage Nicknames` \n \n **Note:** If you are the server owner or not ranked lower than my highest role, I won\'t be able to update your nickname, but I will update your roles. :grinning:', 'warning')
                embed.footer('This command is a premium 💠 only command. Run n.premium to learn more about premium.','https://cdn.discordapp.com/attachments/719414661686099993/754971786231283712/season-callout-badge.png')
                return await embed.send(ctx)
            else:
              try:
                await ctx.author.edit(nick=racer.tag+' ' +racer.name)
              except Exception:
                embed = Embed('Error!', 'The bot needs following permissions: `Manage Nicknames` \n \n **Note:** If you are the server owner or not ranked lower than my highest role, I won\'t be able to update your nickname, but I will update your roles. :grinning:', 'warning')
                if (ctx.author.id) not in [505338178287173642, 637638904513691658, 396075607420567552]:
                    embed.footer('This command is a premium 💠 only command. Run n.premium to learn more about premium.','https://cdn.discordapp.com/attachments/719414661686099993/754971786231283712/season-callout-badge.png')

                else:
                      embed.footer('Discord user '+str(ctx.author.name + '#' + ctx.author.discriminator)+' is a 🛠️developer🛠️ of this bot. \nThis command is a premium 💠 only command.', 'https://media.discordapp.net/attachments/719414661686099993/765490220858081280/output-onlinepngtools_32.png')
                      return await embed.send(ctx)
            embed = Embed('<a:Check:797009550003666955>  Success!', 'Successfully updated your roles and nickname!')        
            if (ctx.author.id) not in [505338178287173642, 637638904513691658, 396075607420567552]:
                embed.footer('This command is a premium 💠 only command. Run n.premium to learn more about premium.','https://cdn.discordapp.com/attachments/719414661686099993/754971786231283712/season-callout-badge.png')
            else:
                embed.footer('Discord user '+str(ctx.author.name + '#' + ctx.author.discriminator)+' is a 🛠️developer🛠️ of this bot. \nThis command is a premium 💠 only command.', 'https://media.discordapp.net/attachments/719414661686099993/765490220858081280/output-onlinepngtools_32.png')
            await embed.send(ctx)
def setup(client):
    client.add_cog(Command(client))
