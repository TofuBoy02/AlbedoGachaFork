import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('TOKEN')



class claimReminder(commands.Cog):

  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_ready(self):
    print('claimReminder cog is online')
    
  @commands.command()
  async def claim(self,ctx):
   
    await ctx.reply("React to the card with any emoji to claim a card.")

def setup(client):
  client.add_cog(claimReminder(client))