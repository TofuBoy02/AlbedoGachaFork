import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()
import pyrebase
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



class bal(commands.Cog):

  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_ready(self):
    print('bal cog is online')
    
  @commands.command()
  async def bal(self,ctx, user=None):
    if user == None:
      try:
        balance = database.child("users").child(ctx.author.id).child("currency").get().val()
        await ctx.reply(f"You have {balance} <:cecilia:1038333000905134141>")
      except:
        await ctx.reply("You have no cecilias! You can earn cecilias by claiming cecilia cards or selling your claimed cards!")
    elif user != None:
      try:
        if user.startswith("<@"):
          user = int(user[2:-1])
          print(user)
          uid_to_user = self.client.get_user(user).name
        else:
          uid_to_user = self.client.get_user(int(user)).name
        balance = database.child("users").child(user).child("currency").get().val()
        await ctx.reply(f"{uid_to_user} have {balance} <:cecilia:1038333000905134141>")
      except:
        await ctx.reply("Could find {uid_to_user}'s account.")

  
        
def setup(client):
  client.add_cog(bal(client))