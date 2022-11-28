# import os
# import discord
# from discord.ext import commands
# from dotenv import load_dotenv
# import pyrebase
# import random
# from collections import Counter
# import asyncio
# import time
# import datetime

# load_dotenv()

# TOKEN = os.getenv('TOKEN')

# config = {
#     'apiKey': os.getenv('apiKey'),
#     'authDomain': os.getenv('authDomain'),
#     'projectId': os.getenv('projectId'),
#     'storageBucket': os.getenv('storageBucket'),
#     'messagingSenderId': os.getenv('messagingSenderId'),
#     'appId': os.getenv('appId'),
#     'measurementId': os.getenv('measurementId'),
#      'databaseURL': os.getenv('databaseURL')
# }

# firebase = pyrebase.initialize_app(config)
# database = firebase.database()


# class p(commands.Cog):

#   def __init__(self, client):
#     self.client = client

#   @commands.Cog.listener()
#   async def on_ready(self):
#     print('push cog is online')


  
#   @commands.command()
#   @commands.has_role("Owner")
#   async def p(self,ctx,uid=None):

#     await ctx.message.delete()

#     rarity = "rarity-4"

#     artist = "юнхоня"
#     card_name = "easy albedo’s booty tutorial"
#     image = "https://cdn.discordapp.com/attachments/1036843967402229780/1038675733763076156/f6074b03ac52594b9cbd2bda74e684c2_7194763914734976419.jpg"
#     link = "https://www.hoyolab.com/article/13217307"

#     data = {"artist": artist,
#             "card_name": card_name,
#             "claimed": "false",
#             "description": "None",
#             "image": image,
#             "owned_by": "None",
#             "post_link": link,
#             "rarity": rarity[7:]}

    

#     index = len(database.child("cards").child(rarity).get().val())
#     database.child("cards").child(rarity).child(index).set(data)
#     print(index)
        
# def setup(client):
#   client.add_cog(p(client))