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

#### Rarity Index Fetcher ####

rarity_3_index = len(database.child("cards").child("rarity-3").get().val())
rarity_4_index = len(database.child("cards").child("rarity-4").get().val())
rarity_5_index = len(database.child("cards").child("rarity-5").get().val())

status_claimed = {"status": "claimed",
                  "timestamp": f"{int(time.time()) + 1800}"}
status_can_claim = {"status": "can_claim"}

class chat(commands.Cog):

  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_ready(self):
    print('chat cog is online')

  # @commands.Cog.listener()
  # async def on_command_error(self, ctx, error):
  #   if isinstance(error, commands.CommandOnCooldown):
  #     remaining_seconds = int(round(error.retry_after, 2))
  #     remaining_time = time.strftime("%Mm%Ss", time.gmtime(remaining_seconds))
  #     await ctx.send(f"You've used up all your pulls! Your pulls will reset in {remaining_time}")
    
  @commands.cooldown(5, 600, commands.BucketType.user)
  @commands.command()
  async def xxx(self,ctx,uid=None):
    message = await ctx.reply("Rolling! <a:rollingfast:1036896585155624990>")

    rarities = ["rarity-3", "rarity-4", "rarity-5"]
    chance = [50, 46, 4]
    # chance = [100, 0, 0]

    result = random.choices(rarities, chance, k=1)
    counter_res = (Counter(result))
    final_rarity = list(counter_res.keys())[list(counter_res.values()).index(1)]


    if final_rarity == "rarity-3":
        card_index = rarity_3_index - 1
        # card_index = 2
        rarity_stars = "⭐⭐⭐"
    elif final_rarity == "rarity-4":
        card_index = rarity_4_index - 1
        rarity_stars = "⭐⭐⭐⭐"
    elif final_rarity == "rarity-5":
        card_index = rarity_5_index - 1
        rarity_stars = "⭐⭐⭐⭐⭐"

    random_card_index = random.randint(1, card_index)

    ###FETCH RARITY FROM CARD RESULT

    card_data = database.child("cards").child(f"{final_rarity}").child(random_card_index).get().val()
    claimed_card = {"Card_name": f"{card_data['card_name']}",
                "Card_ID":f"{final_rarity}-{random_card_index}",
                "Card_rarity": f"{card_data['rarity']}"}


    ##### CHECK IF CARD IS OWNED ALREADY #####
    if card_data['claimed'] == True:
      card_is_claimed = True
    else:
      card_is_claimed = False

    #### CECILIA CARD ####
    if random_card_index == 1 and final_rarity == "rarity-3":
      cecilia = True
      embed = discord.Embed(title="Cecilia 50x", description="React to claim 50x cecilia")
      embed.set_image(url="https://media.discordapp.net/attachments/1036843967402229780/1037247645086924820/Item_Cecilia_1.png")
    else:
      cecilia = False
      if card_data['description'] == "None":
          description = ""
      else:
          description = f"{card_data['description']}\n"

      embed=discord.Embed(title=f"Art by {card_data['artist']}", color = discord.Color.random(), description = f"**{card_data['card_name']}**\n{rarity_stars}\n{description}[Link]({card_data['post_link']})")
      embed.set_image(url=card_data['image'])

      if card_is_claimed:
        embed.set_footer(text=f"Owned by {card_data['owned_by']}")

    await message.edit(content="", embed=embed)

    while True:
      try:
        reaction, user = await self.client.wait_for(
          "reaction_add",
          check=lambda reaction, user: reaction.message == message,
          timeout=20
        )


        ##### IF USER ID IS NOT IN DATABASE #####
        if not database.child("users").child(user.id).shallow().get().val():
        
          if not card_is_claimed:
            await message.edit(content="", embed=embed.set_footer(text=f"claimed by {user.name}"))
            if cecilia == True:

              await ctx.send(f"{user.name} claimed **{card_data['card_name']}**")
              cecilia_data = {"currency": 50}

            else:
              cecilia_data = {"currency": 0}

              await ctx.send(f"{user.name} claimed **{card_data['card_name']}**")
              database.child("users").child(user.id).child("owned_cards").child(card_data['card_name']).set(claimed_card)
              database.child("users").child(user.id).child("currency").set(cecilia_data)
              database.child("users").child(user.id).child("status").set(status_claimed)
              database.child("cards").child(f"{final_rarity}").child(random_card_index).update({"claimed": "True"})
              database.child("cards").child(f"{final_rarity}").child(random_card_index).update({"owned_by": f"{user.name}"})
              return
          elif card_is_claimed:
            await message.edit(content="", embed=embed.set_footer(text=f"50 cecilias claimed by {user.name}"))
            current_currency = (database.child("users").child(user.id).child("currency").get().val())["currency"]
            database.child("users").child(user.id).child("currency").update({"currency":current_currency + 50})
            return

        
        #### IF USER ID ALREADY EXISTS
        elif database.child("users").child(user.id).shallow().get().val():
          current_status = database.child("users").child(user.id).child("status").get().val()

          if current_status['status'] == "can_claim":
            await message.edit(content="", embed=embed.set_footer(text=f"claimed by {user.name}"))
            await ctx.send(f"{user.name} claimed **{card_data['card_name']}**")
            database.child("users").child(user.id).child("status").set(status_claimed)

            if cecilia == True:
              current_currency = (database.child("users").child(user.id).child("currency").get().val())['currency']
              currency_sum = {"currency": current_currency + 50}
              database.child("users").child(user.id).child("currency").set(currency_sum)
              return

            elif cecilia == False:
              database.child("users").child(user.id).child("owned_cards").child(card_data['card_name']).set(claimed_card)
              return

              
          elif current_status['status'] == "claimed":
            current_unix = int(time.time())
            unix_added = int((database.child("users").child(user.id).child("status").get().val())['timestamp'])
            if current_unix > unix_added:
              current_status = database.child("users").child(user.id).child("status").get().val()
              await message.edit(content="", embed=embed.set_footer(text=f"claimed by {user.name}"))
              await ctx.send(f"{user.name} claimed **{card_data['card_name']}**")
              database.child("users").child(user.id).child("status").set(status_claimed)

              if cecilia == True:
                current_currency = (database.child("users").child(user.id).child("currency").get().val())['currency']
                currency_sum = {"currency": current_currency + 50}
                database.child("users").child(user.id).child("currency").set(currency_sum)
                return

            elif cecilia == False:
              database.child("users").child(user.id).child("owned_cards").child(card_data['card_name']).set(claimed_card)
              return

            elif current_unix < unix_added:
              unix_difference = unix_added - current_unix

              #### CONVERTS REMAINING SECONDS TO Minutes Seconds #####
              converted = time.strftime("%Mm%Ss", time.gmtime(unix_difference))

              await ctx.reply(f"You have already claimed a card. You can claim again in {converted}")
        
        

      except asyncio.TimeoutError:
        await message.edit(content="", embed=embed.set_footer(text="expired"))
        return

  
        
def setup(client):
  client.add_cog(chat(client))