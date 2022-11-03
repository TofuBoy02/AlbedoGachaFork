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



class chat(commands.Cog):

  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_ready(self):
    print('bal cog is online')
    
  @commands.command()
  async def bal(self,ctx):
    try:
      balance = (database.child("users").child(ctx.author.id).child("currency").get().val())["currency"]
      await ctx.reply(f"You have {balance} cecilias!")
    except:
      await ctx.reply("You have no cecilias! You can earn cecilias by claiming cecilia cards or selling your claimed cards!")

  
        
def setup(client):
  client.add_cog(chat(client))