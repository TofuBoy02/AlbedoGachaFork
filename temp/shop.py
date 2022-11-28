import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()
import pyrebase
TOKEN = os.getenv('TOKEN')


class buy(commands.Cog):

  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_ready(self):
    print('shop cog is online')
    
  @commands.command()
  async def shop(self,ctx):
    
    embed = discord.Embed(title="Albedo Shop", color=12748863)
    embed.add_field(name="Pull Count Reset", value="`.buy pull`: 100 <:cecilia:1038333000905134141>\n*Resets pulls to 5. Use up all pulls before buying.*", inline=False)
    embed.add_field(name="Claim Reset", value="`.buy  claim`: 500 <:cecilia:1038333000905134141>\n*Resets claim status and skips 30 minute cooldown.*", inline=False)
    await ctx.reply(embed=embed)

        
def setup(client):
  client.add_cog(buy(client))