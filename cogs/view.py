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



class view(commands.Cog):

  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_ready(self):
    print('view cog is online')
    
  @commands.command()
  async def view(self,ctx, *, card=None):
    # try:
      if card == None:
        await ctx.reply("Specify a card!")
      else:
      
        parse_index = card[2:]
        if int(parse_index) >= 10:
          parse_rarity = card[:-3]
        elif int(parse_index) < 10:
          parse_rarity = card[:-2]
 

        card = database.child("cards").child(f"rarity-{parse_rarity}").child(parse_index).get().val()
        if card['rarity'] == 3 or card['rarity'] == "3":
      
          rarity = '⭐⭐⭐'
        elif card['rarity'] == 4 or card['rarity'] == "4":
     
          rarity = '⭐⭐⭐⭐'
        elif card['rarity'] == 5 or card['rarity'] == "5":
     
          rarity = '⭐⭐⭐⭐⭐'

      
        embed = discord.Embed(title=f"Art By {card['artist']}", description=rarity, color=discord.Color.random())
        embed.set_image(url=card['image'])

        if card['claimed'] == "true" or card['claimed'] == True:
          uid_to_user = self.client.get_user(card['owned_by']).name
          embed.set_footer(text=f"Owned by {uid_to_user}")

        await ctx.reply(embed=embed)
    # except:
    #   await ctx.reply("Card not found.")

    
    

  
        
def setup(client):
  client.add_cog(view(client))