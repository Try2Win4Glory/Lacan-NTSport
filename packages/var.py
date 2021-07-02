'''Most Used Variables'''

import discord
from discord.ext import commands
import random

devs = [
  # Try2Win4Glory
    505338178287173642
]

globalupdateperms = [
  # Try2Win4Glory
    505338178287173642,
  # adl212
    396075607420567552
]

globalregisterperms = [
  # Try2Win4Glory
    505338178287173642,
  # adl212
    396075607420567552
]

globalunregisterperms = [
  # Try2Win4Glory
    505338178287173642,
  # adl212
    396075607420567552
]

roleallperms = [
  # SSH Administrator
    788549177545588796,
  # SSH Moderator
    788549154560671755,
  # SSH Server Support
    788549207149248562
]

roleupdateperms = [
]

roleregisterperms = [
]

roleunregisterperms = [
]

# Team Roles

teamswithroles = [
]

# Team N8TE | Server Owner: 630761745140547625
if ctx.guild.id in [
  636582509429260289
]:
  teamswithroles.append('[N8TE]')
  
# Team DRPT | Server Owner: 723224207651111003
if ctx.guild.id in [
  742854336618561608
]:
  teamswithroles.append('[DRPT]')
  
# Team RRN | Server Owner: 653772108815532053
if ctx.guild.id in [
  696055942055198760
]:
  teamswithroles.append('[RRN]')
  
# Team NEWS | Server Owner: 272370019894165505
if ctx.guild.id in [
  835305919679692850
]:
  teamswithroles.append('[NEWS]')
  
# Team TEST | Server Owner: 505338178287173642
if ctx.guild.id in [
  833317505888026644
]:
  teamswithroles.append('[TEST]')
  
# Team TBZ | Server Owner: 657296213087092756
if ctx.guild.id in [
   857697272317345792
]:
   teamswithroles.append('[TBZ]')
    
# Team SSH | Server Owner: 363082908270985217
if ctx.guild.id in [
  788547373701136425
]:
  teamswithroles.append('[SSH]')
]

list_of_lacans = [
  '<:lacan_economy_1:801006407536607262>',
  '<:lacan_economy_2:801004873612132382>',
  '<:lacan_economy_3:801004873214722079>',
  '<:lacan_economy_4:801004868126113822>',
  '<:lacan_economy_5:801004868348936203>',
  '<:lacan_economy_6:801004863433605160>',
  '<:lacan_economy_7:801004870643220481>',
  '<:lacan_economy_8:801004872820457483>',
  '<:lacan_economy_9:801004872417804298>',
  '<:lacan_economy_10:801004872811413514>'
]

random_lacan = random.choice(list_of_lacans)
