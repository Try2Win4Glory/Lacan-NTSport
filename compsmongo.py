import pymongo
import os
import json
import time
import queue
import threading
import motor

client = motor.motor_tornado.MotorClient(f"mongodb+srv://adl212:{os.getenv('DB_KEY')}@cluster0.q3r5v.mongodb.net/test?retryWrites=true&w=majority")
class DBClient:
    def __init__(self):
        self.client = client
        self.db = self.client.comps
    async def get_array(self, collection, dict):
        return collection.find(dict)
    async def update_array(self, collection, old, new):
        return await collection.replace_one(old, new)
    async def create_doc(self, collection, data):
        await collection.insert_one(data)
