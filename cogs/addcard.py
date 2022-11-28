import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import pyrebase
import random
from collections import Counter
import asyncio
import time
import datetime
from humanfriendly import format_timespan

load_dotenv()

TOKEN = os.getenv('TOKEN')

config = {
    'apiKey': os.getenv('apiKey'),
    'authDomain': os.getenv('authDomain'),
    'projectId': os.getenv('projectId'),
    'storageBucket': os.getenv('storageBucket'),
    'messagingSenderId': os.getenv('messagingSenderId'),
    'appId': os.getenv('appId'),
    'measurementId': os.getenv('measurementId'),
    'databaseURL': os.getenv('databaseURL')
      
}

firebase = pyrebase.initialize_app(config)
database = firebase.database()

# Rarity Index Fetcher





class chat(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('gacha cog is online')

    @commands.command()
    async def add(self, ctx, rarity, artist, name, image, link):

        rarity_index = len(database.child("cards").child(f"rarity-{rarity}").get().val())
        
        data = {"artist": f"{artist}",
                             "card_name": f"{name}",
                             "claimed": "false",
                             "description": "None",
                             "image": f"{image}",
                             "owned_by": "None",
                             "post_link": f"{link}",
                             "rarity": rarity}
            
        database.child("cards").child(f"rarity-{rarity}").child(f"{rarity_index}").set(data)
        # print(rarity_index)
def setup(client):
    client.add_cog(chat(client))
