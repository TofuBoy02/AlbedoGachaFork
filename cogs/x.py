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

rarity_3_index = len(database.child("cards").child("rarity-3").get().val())
rarity_4_index = len(database.child("cards").child("rarity-4").get().val())
rarity_5_index = len(database.child("cards").child("rarity-5").get().val())

status_claimed = {"status": "claimed",
                  "timestamp": f"{int(time.time()) + 1800}"}
status_can_claim = {"status": "can_claim"}


# class CooldownManager:

#     def __init__(self, executions_allowed: int, cooldown_time: float):
#         self.state = {}
#         self.executions_allowed = executions_allowed
#         self.cooldown_time = cooldown_time

#     def time_left(self, key) -> float:
#         """Attempt to execute. Return 0 if ready, or the number of seconds until you're allowed to execute again."""
#         if key not in self.state.keys():
#             self.state[key] = []
#         if len(self.state[key]) > 0:
#             # Clean up executions that have aged away
#             # self.state[key] is sorted with the newest first
#             for i in range(len(self.state[key])-1, -1, -1):
#                 if self.state[key][i] + self.cooldown_time < time.time():
#                     del self.state[key][i]
#             if len(self.state[key]) < self.executions_allowed:
#                 self.state[key].append(time.time())
#                 return 0
#             next_available_execution = self.state[key][len(
#                 self.state)-1] + self.cooldown_time
#             return next_available_execution - time.time()
#         else:
#             self.state[key].append(time.time())
#             return 0

#     def assert_cooldown(self, data):
#         """Run this at the beginning of the command."""
#         time_left = self.time_left(data)
#         if time_left > 0:
#             raise commands.CommandOnCooldown('', retry_after=time_left)

# cm1 = CooldownManager(1, 2.0)  # execute once every 3 seconds
# cm2 = CooldownManager(5, 1800.0)  # execute up to 5x every 10 minutes


class chat(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('gacha cog is online')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            remaining_seconds = int(round(error.retry_after, 2))
            
            if remaining_seconds < 60:
              remaining_time = format_timespan(remaining_seconds)
              await ctx.reply(f"Try again in {remaining_time}")
            elif remaining_seconds > 10:
              # remaining_time = time.strftime("%Mm%Ss", time.gmtime(remaining_seconds))
              remaining_time = format_timespan(remaining_seconds)
              await ctx.reply(f"You've used up all your pulls! Try again in {remaining_time}")
            
        else:
            print(error)

    @commands.cooldown(5, 1800, commands.BucketType.user)
    @commands.command()
    async def g(self, ctx, uid=None):
        # cm1.assert_cooldown(ctx.author.id)  # This is basically the bucket type. You can use things like ctx.author.id, ctx.guild.id, etc
        # cm2.assert_cooldown(ctx.author.id)

        rarities = ["rarity-3", "rarity-4", "rarity-5"]
        chance = [50, 44, 6]

        # DEFINES FINAL ROLLED RARITY
        result = random.choices(rarities, chance, k=1)
        counter_res = (Counter(result))

        # SENDS A MESSAGE
        # message = await ctx.reply("Rolling! <a:rollingfast:1036896585155624990>")

        final_rarity = list(counter_res.keys())[
            list(counter_res.values()).index(1)]

        if final_rarity == "rarity-3":
            card_index = rarity_3_index - 1
            rarity_stars = "⭐⭐⭐"
        elif final_rarity == "rarity-4":
            card_index = rarity_4_index - 1
            rarity_stars = "⭐⭐⭐⭐"
        elif final_rarity == "rarity-5":
            card_index = rarity_5_index - 1
            rarity_stars = "⭐⭐⭐⭐⭐"

        # DEFINES THE FINAL CARD
        random_card_index = random.randint(1, card_index)
        # random_card_index = 1

        # FETCH THE CARD DATA
        card_data = database.child("cards").child(
            f"{final_rarity}").child(random_card_index).get().val()

        # DEFINE DATA OF STORED CARDS OF USER WHEN CLAIMED
        claimed_card_data = {"Card_name": f"{card_data['card_name']}",
                             "Card_ID": f"{final_rarity}-{random_card_index}",
                             "Card_rarity": f"{card_data['rarity']}"}

        # DEFINE UNIX TIMES
        current_unix = int(time.time())
        current_unix_added = current_unix + 10800
        current_unix_added_cecilia = current_unix + 600

        # CHECK IF CARD IS CLAIMED
        if card_data['claimed'] == "true" or card_data['claimed'] == True:
            card_is_claimed = True
        else:
            card_is_claimed = False

        if card_data['description'] == "None":
            description = ""
        else:
            description = f"{card_data['description']}\n"

        # DEFINE THE CARD EMBED
        embed = discord.Embed(title=f"Art by {card_data['artist']}", color=discord.Color.random(
        ), description=f"**{card_data['card_name']}**\n{rarity_stars}\n{description}[Link]({card_data['post_link']})")
        embed.set_image(url=card_data['image'])

        # ADD FOOTER IF CARD IS CLAIMED BY SOMEONE ELSE ALREADY
        if card_is_claimed:
            owner = database.child("cards").child(f"{final_rarity}").child(
                random_card_index).child("owned_by").get().val()
            try:
              uid_to_user = self.client.get_user(owner).name
            except:
              uid_to_user = "Error"
            embed.set_footer(
                text=f"Owned by {uid_to_user}. Claim to get 50 cecilia.")

        # SENDS THE EMBED
        # await message.edit(content="", embed=embed)
        message = await ctx.reply(embed=embed)

        while True:
            try:
                reaction, user = await self.client.wait_for(
                    "reaction_add",
                    check=lambda reaction, user: reaction.message == message,
                    timeout=15
                )

                # CLAIM EVENT

                if not database.child("users").child(user.id).shallow().get().val():

                    if not card_is_claimed:
                        await message.edit(content="", embed=embed.set_footer(text=f"Claimed by {user.name}"))
                        database.child("users").child(
                            user.id).update({"currency": 0})
                        database.child("users").child(user.id).child("owned_cards").child(
                            card_data['card_name']).set(claimed_card_data)
                        database.child("users").child(user.id).update(
                            {"claim_time": current_unix_added})
                        database.child("cards").child(f"{final_rarity}").child(
                            random_card_index).update({"claimed": "true"})
                        database.child("cards").child(f"{final_rarity}").child(
                            random_card_index).update({"owned_by": user.id})
                        return

                    if card_is_claimed:

                        await message.edit(content="", embed=embed.set_footer(text=f"Added 50 Cecilia for {user.name}"))
                        database.child("users").child(
                            user.id).update({"currency": 50})
                        database.child("users").child(user.id).update(
                            {"claim_time": current_unix_added_cecilia})
                        return

                elif database.child("users").child(user.id).shallow().get().val():
                    saved_unix = database.child("users").child(
                        user.id).child("claim_time").get().val()

                    if current_unix > saved_unix:

                        if not card_is_claimed:
                            await message.edit(content="", embed=embed.set_footer(text=f"Claimed by {user.name}"))
                            database.child("users").child(user.id).child("owned_cards").child(
                                card_data['card_name']).set(claimed_card_data)
                            database.child("users").child(user.id).update(
                                {"claim_time": current_unix_added})
                            database.child("cards").child(f"{final_rarity}").child(
                                random_card_index).update({"claimed": "true"})
                            database.child("cards").child(f"{final_rarity}").child(
                                random_card_index).update({"owned_by": user.id})
                            return

                        elif card_is_claimed:
                            await message.edit(content="", embed=embed.set_footer(text=f"Added 50 Cecilia for {user.name}"))
                            current_balance = database.child("users").child(
                                user.id).child("currency").get().val()
                            database.child("users").child(user.id).update(
                                {"currency": current_balance + 50})
                            database.child("users").child(user.id).update(
                                {"claim_time": current_unix_added_cecilia})
                            return

                    if current_unix < saved_unix:
                        unix_difference = saved_unix - current_unix
                        converted = time.strftime(
                            "%Mm%Ss", time.gmtime(unix_difference))
                        await ctx.reply(f"You have alread claimed a card. Try again in {converted}")

            except asyncio.TimeoutError:
                return
                # await message.edit(content="", embed=embed.set_footer(text="expired"))


def setup(client):
    client.add_cog(chat(client))
