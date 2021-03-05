from discord.ext import commands

import dbl
import os
from mongoclient import DBClient
class TopGG(commands.Cog):
    """
    This example uses dblpy's webhook system.
    In order to run the webhook, at least webhook_port must be specified (number between 1024 and 49151).
    """

    def __init__(self, bot):
        self.bot = bot
        self.token = os.getenv('top_token')  # set this to your DBL token
        self.dblpy = dbl.DBLClient(self.bot, self.token, webhook_path='/', webhook_auth=self.token, webhook_port=5000)
    
    @commands.Cog.listener()
    async def on_dbl_vote(self, data):
        """An event that is called whenever someone votes for the bot on top.gg."""
        member = data['user']
        member = await self.bot.fetch_user(int(member))
        dbclient = DBClient()
        collection = dbclient.db.pointsdb
        data = await dbclient.get_array(collection, {'$and': [{'userid': str(member.id)}, {'userid': str(member.id)}]})
        async for d in data:
            user = d
            break
        old = user.copy()
        try:
            if user['userid'] == str(member.id):
                print(user)
                user['points'] += 5
        except:
            dbclient.create_doc(collection, {'userid': str(member.id), 'points': 5})
        await dbclient.update_array(collection, old, user)
        try:
          await member.send('Thanks for voting! You\'ve been given 5 Lacans!')
        except:
          pass
    @commands.Cog.listener()
    async def on_dbl_test(self, data):
        """An event that is called whenever someone tests the webhook system for your bot on top.gg."""
        member = data['user']
        member = await self.bot.fetch_user(int(member))
        dbclient = DBClient()
        collection = dbclient.db.pointsdb
        data = await dbclient.get_array(collection, {'$and': [{'userid': str(member.id)}, {'userid': str(member.id)}]})
        async for d in data:
            user = d
            break
        old = user.copy()
        try:
            if user['userid'] == str(member.id):
                print(user)
                user['points'] += 5
        except:
            dbclient.create_doc(collection, {'userid': str(member.id), 'points': 5})
        await dbclient.update_array(collection, old, user)
        try:
          await member.send('Thanks for voting! You\'ve been given 5 Lacans!')
        except:
          pass


def setup(bot):
    bot.add_cog(TopGG(bot))