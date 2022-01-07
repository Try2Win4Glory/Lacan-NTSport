'''Update the User\'s Donator Roles'''
import discord
from discord.ext import commands
from discord.utils import get
from packages.utils import Embed, ImproperType

class Command(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def donor(self, ctx, user, amount):
      
    # No Arguments are given.
      if user == None or amount == None:
        embed=Embed(':warning:  Error!', 'Please use the correct format.\n\n```n.donor <User ID / Mention> <Amount>```.')
        embed.field('Example', 'n.donor <@505338178287173642> 100')
        return await embed.send(ctx)
      
    # Set Permissions to use the command.
      allowed = False
      permitted = []
      permittedservers = [
      # SSH Server
        788547373701136425
      ]
      
      if ctx.guild.id in permittedservers:
        permitted = [
        # SSH Server Server Support
            788549207149248562,
        # SSH Server Developer -> ONLY FOR TESTING PURPOSES
            797709977569591317
        ]

    # Check for Author Permissions.
      for role in ctx.author.roles:
        if role.id in permitted:
          allowed = True

    # Author doesn't have Permissions.
      if allowed == False:
        embed=Embed(':warning:  Error!', 'You do not have the permission to use this command.')
        return await embed.send(ctx)
    # Author does have Permissions.
      else:
        user = user.replace("<@", "")
        user = user.replace("!", "")
        user = user.replace(">", "")
        try:
          user = await ctx.guild.fetch_member(user)
        except:
          embed = Embed(':warning:  Error!', 'I was unable to fetch the Discord User. Please use a valid ID or Mention.')
          return await embed.send(ctx)

      # Check if Donortype is Million or Billion.
        if 'b' in list(amount):
          donortype = 'billion'
        else:
          donortype = 'million'

      # Set all used Variables to Empty to not have an undefined Variable Error at a later point.
        removebill = []
        removemill = []
        textaddbill = []
        textaddmill = []
        removelogging = []
        removerolenamesmill = []
        removerolenamesbill = []

      # Event happening if no "b" was used in the amount.
        if donortype == 'million':
          remove = ['1', '10', '25', '50', '100', '250']
          removebill = ['1', '2', '3']
          textadd = 'm Donator'
          textaddbill = 'b Donator'
          removerolenames = ['$'+ x + textadd for x in remove]
          removerolenamesbill = ['$'+ x + textaddbill for x in removebill]
      # Event happening if "b" was used in the amount.
        else:
          remove = ['1', '2', '3']
          removemill = ['1', '10', '25', '50', '100', '250']
          textadd = ' Donator'
          textaddmill = 'm Donator'
          removerolenames = ['$'+ x + textadd for x in remove]
          removerolenamesmill = ['$'+ x + textaddmill for x in removemill]
        
      # Checking which Role should be added.
        addrolenames = ['$'+ amount + textadd]
        print(addrolenames)

      # Removing all Donator roles of the User.
        for role in (user.roles):
          name = role.name
          if name in removerolenames or name in removerolenamesbill or name in removerolenamesmill:
              role = get(ctx.message.guild.roles, id=role.id)
              removelogging.append(role)
              await user.remove_roles(role)

      # Get the role and add it to the User.
        try:
          name = role.name
          role = get(ctx.message.guild.roles, name="".join(addrolenames))
          await user.add_roles(role)
        except Exception as e:
          print(e)
          embed = Embed(':warning:  Error!', 'An unexpected error occured. Please try again later.')
          return await embed.send(ctx)
      
      # Visually Updating the List for Logging.
        try:
          formatremove = ', '.join(removelogging)
        except:
          formatremove = removelogging
        formatadd = ', '.join(addrolenames)
      
      # No Role was removed - Success Embed.
        if removelogging != []:
          embed=Embed(':white_check_mark:  Success!', f'{user.mention}\'s Donator roles have been updated by {ctx.author.mention}.\n\n**__Removed:__**\n```{formatremove}```\n\n**__Added:__**\n```{formatadd}```')
          return await embed.send(ctx)
        
      # At least 1 Role was removed - Success Embed.
        else:
          embed=Embed(':white_check_mark:  Success!', f'{user.mention}\'s Donator roles have been updated by {ctx.author.mention}.\n\n**__Added:__**\n```{formatadd}```')
          return await embed.send(ctx)

def setup(client):
    client.add_cog(Command(client))
