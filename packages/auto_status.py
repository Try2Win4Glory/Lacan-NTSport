from discord.ext import tasks, commands
from discord import Streaming, Game, Activity, ActivityType, Status
from random import choice

class AutoStatus(commands.Cog):
    def __init__(self, client):
        self.auto_status.start()
        self.client = client

    @tasks.loop(seconds=10)
    async def auto_status(self):
        statuses = {
            'streaming' : [ 
              'n.help', 
              'on YouTube', 
              'Nitrotype', 
              'alone',
              #'Verified on 20/11/2020!',
              f'on {len(self.client.guilds)} servers', 
              #f'with {self.users()} users',
              'Buy premium 💠 today!',
              'n.premium'],

            'playing' : [
              'n.help', 
              'Nitrotype', 
              'games', 
              'alone', 
              'with the devs!',
              #'Verified on 20/11/2020!',
              f'on {len(self.client.guilds)} servers', 
              #f'with {self.users()} users',
              'Buy premium 💠 today!',
              'n.premium'],

            'watching' : [
              'n.help', 
              'Nitro Type Videos', 
              'YouTube', 
              'alone', 
              #'Verified on 20/11/2020!',
              f'on {len(self.client.guilds)} servers', 
              'you', 
              #f'with {self.users()} users',
              'Buy premium 💠 today!',
              'n.premium'],

            'listening' : [
              'n.help', 
              'songs alone', 
              #'Verified on 20/11/2020!',
              f'songs on {len(self.client.guilds)} servers', 
              'I need gold', 
              #f'songs with {self.users()} users', 
              'Buy premium 💠 today!',
              'n.premium']
           
        }
        
        status_type = choice([status for status in statuses])
        if status_type == 'streaming':
            await self.client.change_presence(activity=Streaming(name=choice(statuses.get('streaming')), url='https://www.youtube.com/watch?v=Tt7bzxurJ1I'))

        elif status_type == 'playing':
            await self.client.change_presence(status=Status.idle, activity=Game(name=choice(statuses.get('playing'))))

        elif status_type == 'watching':
            await self.client.change_presence(status=Status.idle, activity=Activity(type=ActivityType.watching, name=choice(statuses.get('watching'))))

        elif status_type == 'listening':
            await self.client.change_presence(status=Status.idle, activity=Activity(type=ActivityType.listening, name=choice(statuses.get('listening'))))
    
    def users(self):
        count = 0
        for guild in self.client.guilds:
            for member in guild.members:
                count += 1
        return count

def setup(client):
    client.add_cog(AutoStatus(client))