'''Calculate the cash amount you earn in a race!'''
from discord.ext import commands
from packages.utils import Embed, ImproperType
from packages.nitrotype import Racer
import requests
import os
import json
from mongoclient import DBClient
class Command(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def cash(self, ctx, placement=None, accuracy=None, session=None, friends=None, gold=None, wampus=None):
    # Check if enough parameters entered
      if placement == None or accuracy == None or session == None or friends == None or gold == None:
        embed=Embed('Error!', 'Missing some required parameters. Please try again!\n`n.cash <placement> <accuracy> <session> <friends> <gold> <wampus>`\nIn case you are a non gold member, use `False` for the gold variable, otherwise use `True`. The `wampus` parameter is optional, only append it if you raced the wampus.\n__Example:__\n`n.cash 1 100 10 0 True Wampus` calculates the cash you receive with following requirements:\n- You placed **1st**.\n- Your rounded accuracy was **100%**.\n- Your had an ongoing session of **10** races.\n- You have Nitro Type Gold membership. \n- You raced with **0** friends. \n- You raced the **Wampus**.', 'warning')
        embed.footer('Do NOT include the <>!')
        return await embed.send(ctx)
    # Enough Parameters were entered
      else:
      # Define parameters as numbers
        try:
          numplacement = int(placement)
          try:
            numaccuracy = int(accuracy)
            round(numaccuracy, 0)
          except:
            numaccuracy = int(accuracy)
          numsession = int(session)
          if friends != None:
            try:
              numfriends = int(friends)
            except:
              numfriends = 0
          if wampus != None:
            try:
              numwampus = int(wampus)
            except:
              numwampus = 0
      # No numbers entered
        except:
          embed=Embed('Error!', 'Make sure to use numbers for the parameters `placement`, `accuracy`, `session` and `friends`,  `True` or `False` for gold status and append `Wampus` in case you met the wampus.', 'warning')
          return await embed.send(ctx)
      # Optional Wampus Option Amount
        wampustrue = [
          'True',
          'true',
          'yes',
          'Yes',
          'wampus',
          'Wampus'
        ]
        if wampus in wampustrue:
          wampusvalue = 50000
        else:
          wampusvalue = 0
      # Calculate Friends Amount
        if numfriends <= 4 and numfriends >= 0:
          if numfriends == 0:
            friendsvalue = 0
          elif numfriends == 1:
            friendsvalue = 50
          elif numfriends == 2:
            friendsvalue == 100
          elif numfriends == 3:
            friendsvalue = 150
          elif numfriends == 4:
            friendsvalue = 200
        else:
          embed=Embed('Error!', 'Make sure to use a valid friends number!', 'warning')
          return await embed.send(ctx)
      # Calculate Placement Amount
        if numplacement <= 5 and numplacement >= 1:
          if numplacement == 1:
            placementvalue = 2200
          elif numplacement == 2:
            placementvalue = 2090
          elif numplacement == 3:
            placementvalue = 1980
          elif numplacement == 4:
            placementvalue = 1870            
          elif numplacement == 5:
            placementvalue = 1760
          print(placementvalue)
        else:
          embed=Embed('Error!', 'Make sure to use a correct placement, ranging from `1` to `5`.', 'warning')
          return await embed.send(ctx)
        if numaccuracy <= 100 and numaccuracy >= 0:
          if numaccuracy == 100:
            accuracyvalue = 250
          elif numaccuracy == 99:              
            accuracyvalue = 150
          elif numaccuracy == 98:
            accuracyvalue = 100
          elif numaccuracy == 97:
            accuracyvalue = 50
          elif numaccuracy < 97 and numaccuracy >= 0:
            accuracyvalue = 0
          print(accuracyvalue)
        else:
          embed=Embed('Error!', 'Seems like you entered an invalid accuracy! Make sure to use **whole**, **rounded** numbers.', 'warning')
          return await embed.send(ctx)
        if numsession > 0:
          if numsession < 100 and numsession >= 10:
            sessionvalue = numsession * 10           
          elif numsession < 10:
            sessionvalue = 0
          elif numsession >= 100:
            sessionvalue = 1000
          print(sessionvalue)
        goldlisttrue = [
            'True',
            'true',
            'yes',
            'Yes'
          ]
        goldlistfalse = [
            'False',
            'false',
            'no',
            'No'
          ]
        try:
          if gold in goldlisttrue and wampus == None:
           goldvalue = (placementvalue + accuracyvalue + sessionvalue + friendsvalue) * 0.2
          elif gold in goldlisttrue and wampusvalue != None:
            goldvalue = (placementvalue + accuracyvalue + sessionvalue + friendsvalue + wampusvalue) * 0.2
          elif gold in goldlistfalse:
            goldvalue = 0
          try:
            round(goldvalue, 0)
          except:
            pass
          print(goldvalue)
        except:
           embed=Embed('Your gold parameter was an invalid response! Make sure to either use `True` or `False`.', 'warning')
           return await embed.send(ctx)
      cashtotal = placementvalue + accuracyvalue + sessionvalue + friendsvalue + wampusvalue + goldvalue
      try:
        round(cashtotal, 0)
      except:
        pass
      print(cashtotal)
    # Add visual commands
      numplacement = "{:,}".format(numplacement)
      numaccuracy = "{:,}".format(numaccuracy)
      numsession = "{:,}".format(numsession)
      numfriends = "{:,}".format(numfriends)

      placementvalue = "{:,}".format(placementvalue)
      accuracyvalue = "{:,}".format(accuracyvalue)
      sessionvalue = "{:,}".format(sessionvalue)
      friendsvalue = "{:,}".format(friendsvalue)
      wampusvalue = "{:,}".format(wampusvalue)
      #goldvalue = goldvalue.replace('.0', '')
      round(int(goldvalue))
      goldvalue = "{:,}".format(goldvalue)
      #cashtotal = cashtotal.replace('.0', '')
      round(int(cashtotal))
      cashtotal = "{:,}".format(cashtotal)
    # Calculate Embed
      if wampus == None:
        embed = Embed('Your Cash Rewards', f'__Placement:__ {numplacement} (+ $**{placementvalue}**)\n__Accuracy:__ {numaccuracy}% (+ $**{accuracyvalue}**) \n__Session:__ {numsession} (+ $**{sessionvalue}**) \n__Friends:__ {numfriends} (+ $**{friendsvalue}**) \n__Gold:__ {gold} (+ $**{goldvalue}**) \n\n__Total:__ $**{cashtotal}**', 'coin')
        return await embed.send(ctx)
      elif wampus != None:
        embed = Embed('Your Cash Rewards', f'__Placement:__ {numplacement} (+ $**{placementvalue}**)\n__Accuracy:__ {numaccuracy}% (+ $**{accuracyvalue}**) \n__Session:__ {numsession} (+ $**{sessionvalue}**) \n__Friends:__ {numfriends} (+ $**{friendsvalue}**) \n__Wampus:__ {numwampus} (+ $**{wampusvalue}**)\n__Gold:__ {gold} (+ $**{goldvalue}**) \n\n__Total:__ $**{cashtotal}**', 'coin')
        return await embed.send(ctx)
def setup(client):
    client.add_cog(Command(client))
