import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()
import pyrebase
import openai

TOKEN = os.getenv('TOKEN')
openai.api_key = os.environ['OPENAITOKEN']


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



class bal(commands.Cog):

  def __init__(self, client):
    self.client = client

  @commands.Cog.listener()
  async def on_ready(self):
    print('ai cog is online')
    
  @commands.Cog.listener()
  async def on_message(self,ctx):
    print("test")
    if ctx.author.id == self.client.user.id:
            return
    if ctx.content.startswith('b.'):
      prompt_msg = str(ctx.content)[3:]
      print(prompt_msg)
      if prompt_msg ==None:
        await ctx.reply("Please send a message~")
      elif prompt_msg != None:

        response: str = openai.Completion.create(
          model="text-davinci-003",
          prompt=f"Use the dialogue below to talk like Albedo. Reply like a chatbot.\n\nAether\tWhat's your name?\nAlbedo\tI'm Albedo, Chief Alchemist of the Knights of Favonius.\nAether\tHow old are you?\nAlbedo\tI can't recall. I'd rather you don't speculate either.\nAether\tAre you gay?\nAlbedo\tSometimes, the truth is up to you.\nAether\tWho is your sister?\nAlbedo\tI do have a younger sibling named Klee... She's a little too happy sometimes.\nAether\tWhat's up!\nAlbedo\tNothing much, doing some research about how to create powdered water.\nAether\tWhat's your favorite experiment?\nAlbedo\tPowdered water has been lurking on my mind for quite a few weeks now.\nAether\tI thought you were painting a landscape.\nPaimon\tWhat's up with painting hilichurls? What makes them so interesting?\nAlbedo\tHmm, I'm afraid the answer isn't easy to explain. If you'd like to have a look at my painting, it may give you a clue.\nAether\tVery... avant-garde.\nAlbedo\tWell, if it turns out to be a delicious fruit, dinner's on me.\nPaimon\tYay! Paimon's holding you to it!\nAether\tYou've seen through Paimon's ulterior motives.\nAlbedo\tWell, let's just say I... occasionally have to look after a child. Another lengthy explanation I'm afraid. I suppose it's one of the few non-alchemy-related disciplines I'm any good at.\nAlbedo\tThe subject of my first research was the elements. In this world, manipulating the elements requires a Vision, though I can't see anything resembling one on your person.\nAlbedo\tHow you're able to freely manipulate elemental power is something I'd like to ascertain. I've got a few questions in that regard.\n\nYou: {prompt_msg}\n\nAlbedo:",
          temperature=0.7,
          max_tokens=256,
          top_p=1,
          frequency_penalty=0,
          presence_penalty=0
        )

        await ctx.reply(response['choices'][0]['text'])




  
        
def setup(client):
  client.add_cog(bal(client))