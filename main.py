import discord
from discord.ext import commands
import os
from os import system
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('TOKEN')


intents = discord.Intents.default()
intents.members = True

client = commands.Bot(
    command_prefix=['.'], help_command=None, intents = intents, case_insensitive=True)

@client.event 
async def on_ready():
  
  print('We have logged in as {0.user}'.format(client))

@client.command()
@commands.has_any_role(1008304083213488229)
async def l(ctx, extension):
  client.load_extension(f'cogs.{extension}')

@client.command()
@commands.has_any_role(1008304083213488229)
async def ul(ctx, extension):
  client.unload_extension(f'cogs.{extension}')

@client.command()
@commands.has_any_role(1008304083213488229)
async def reload(ctx, extension):
  client.load_extension(f'cogs.{extension}')
  client.unload_extension(f'cogs.{extension}')

for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    client.load_extension(f'cogs.{filename[:-3]}')


@client.event
async def on_member_join(member):
    welcome = 1007935143383670847
    channel = client.get_channel(int(welcome))
    embed=discord.Embed(title=f"Welcome {member.name}", description="Welcome to the server! If you joined to talk to Albedo AI, you can go to <#1008319961179115531>.", color=16041501) # F-Strings!
    embed.set_thumbnail(url=member.avatar_url) # Set the embed's thumbnail to the member's avatar image!

    await channel.send(f"<@{member.id}>", embed=embed)



client.run(TOKEN)

