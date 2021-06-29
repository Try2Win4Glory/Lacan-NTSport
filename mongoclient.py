import os
import json
import time
import queue
import threading
import motor
import asyncio
import warnings
from dotenv import load_dotenv

load_dotenv()
client = motor.motor_tornado.MotorClient(f"mongodb+srv://adl212:{os.getenv('DB_KEY')}@cluster0.q3r5v.mongodb.net/test?retryWrites=true&w=majority")
class DBClient:
    def __init__(self):
        self.client = client
        self.db = self.client.nitrotype
    async def get_array(self, collection, dict):
        return collection.find(dict)
    async def update_array(self, collection, old, new):
        return await collection.replace_one(old, new)
    async def create_doc(self, collection, data):
        await collection.insert_one(data)
    async def get_big_array(self, collection, array_name):
        warnings.warn(
            "DBClient.get_big_array is deprecated; instead use get_array",
            DeprecationWarning,
            stacklevel=2,
        )
        async for obj in collection.find({}, {array_name: 1}):
            return obj
    async def update_big_array(self, collection, array_name, data):
        await collection.replace_one({}, data)
        if collection.name == 'NT_to_discord':
            with open('NT_to_discord.json', 'w') as f:
                json.dump(data[array_name], f, indent=4)

