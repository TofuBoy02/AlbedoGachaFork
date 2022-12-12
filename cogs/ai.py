import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()
import pyrebase
# import openai
import json
import requests

TOKEN = os.getenv('TOKEN')


service = {
    
  "type": "service_account",
  "project_id": os.getenv('project_id'),
  "private_key_id": os.getenv('private_key_id'),
  "private_key": os.getenv('private_key'),
  "client_email": os.getenv('client_email'),
  "client_id": os.getenv('client_id'),
  "auth_uri": os.getenv('auth_uri'),
  "token_uri": os.getenv('token_uri'),
  "auth_provider_x509_cert_url": os.getenv('auth_provider_x509_cert_url'),
  "client_x509_cert_url": os.getenv('client_x509_cert_url')
}

config = {
    'apiKey': os.getenv('apiKey'),
    'authDomain': os.getenv('authDomain'),
    'projectId': os.getenv('projectId'),
    'storageBucket': os.getenv('storageBucket'),
    'messagingSenderId': os.getenv('messagingSenderId'),
    'appId': os.getenv('appId'),
    'measurementId': os.getenv('measurementId'),
    'databaseURL': os.getenv('databaseURL'),
    "serviceAccount": service

} 

firebase = pyrebase.initialize_app(config)
database = firebase.database()



class ai(commands.Cog):

  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_ready(self):
    print('ai cog is online')
    
  @commands.Cog.listener()
  async def on_message(self,ctx):
    # print("test")
    if ctx.author.id == self.client.user.id:
            return
    if ctx.content.startswith('b.'):
      prompt_msg = str(ctx.content)[3:]
      print(prompt_msg)
      if prompt_msg ==None:
        await ctx.reply("Please send a message~")
      elif prompt_msg != None:
        message = await ctx.reply("Thinking...")
        response = requests.get(f"https://tofuboy.pythonanywhere.com/albedo?query={prompt_msg}", verify=False)
        response = response.json()['text']
        await message.edit(content=response)

    reference = ctx.reference
    if reference is None:
      return
    else:
      if ctx.reference.resolved.author.id == 1007934486815723520:
        message = await ctx.reply("Thinking...")
        prompt_msg = str(ctx.content)[3:]
        response = requests.get(f"https://tofuboy.pythonanywhere.com/albedo?query={prompt_msg}", verify=False)
        response = response.json()['text']
        await message.edit(content=response)

        

        # await ctx.reply(response['choices'][0]['text'])




  
        
def setup(client):
  client.add_cog(ai(client))