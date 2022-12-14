import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()
import pyrebase
import time
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



class buy(commands.Cog):

  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_ready(self):
    print('buy cog is online')
    
  @commands.command()
  async def buy(self,ctx, *, item=None):

    user_bal = database.child("users").child(ctx.author.id).child("currency").get().val()

    if item == None:
      await ctx.reply("Please specify the item.")

    elif item.lower() == "pulls" or item.lower() == "pull":
      try:
        if user_bal >= 100:
          self.client.get_command("g").reset_cooldown(ctx)
          await ctx.reply("Finished resetting your pulls to 5.")
          database.child("users").child(ctx.author.id).update({"currency":user_bal-100})

        if user_bal < 100:
          await ctx.reply("You don't have enough <:cecilia:1038333000905134141> to buy \"pull\"")
      except TypeError:
        await ctx.reply("You don't have enough <:cecilia:1038333000905134141> to buy \"pull\"")


    elif item.lower() == "claims" or item.lower() == "claim":
      current_unix = int(time.time())
      user_unix = database.child("users").child(ctx.author.id).child("claim_time").get().val()

      if current_unix > user_unix:
        await ctx.reply("You can claim right now. Buying this is useless.")

      elif current_unix < user_unix:

        if user_bal > 500 or user_bal == 500:
          new_bal = user_bal - 500
          await ctx.reply(f"Bought Claim Reset. You can now claim a card. Your new balance is {new_bal}")
          database.child("users").child(ctx.author.id).update({"claim_time": 0})
          database.child("users").child(ctx.author.id).update({"currency": new_bal})

        if user_bal < 500:
          await ctx.reply("You don't have enough <:cecilia:1038333000905134141> to buy \"claim\"")
          print(user_bal)
      


        
def setup(client):
  client.add_cog(buy(client))