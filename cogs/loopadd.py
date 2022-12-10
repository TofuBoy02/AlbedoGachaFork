import os
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
load_dotenv()
import pyrebase
TOKEN = os.getenv('TOKEN')
import time

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



class pulladd(commands.Cog):

  def __init__(self, client):
    self.client = client
    self.loopadd.start()


  @commands.Cog.listener()
  async def on_ready(self):
    print('loop cog is online')

  def cog_unload(self):
    self.loopadd.cancel()

      
  @tasks.loop(minutes=10)
  async def loopadd(self):
    print("looping")
    database.child("pull_refresh").child("unix").set(int(time.time()) + 600)
    all_users = database.child("users").shallow().get().val()
    for user in all_users:
      if database.child("users").child(user).child("pulls").get().val():
        user_data = database.child("users").child(user).child("pulls").get().val()
        # print(user_data)
        max_pulls = user_data['max']
        current_pulls = user_data['amount']
        speed = user_data['speed']

        
        remaining_slots = max_pulls - current_pulls
        # print(f"Remaining Slots: {remaining_slots}")
        if remaining_slots >= speed:
          print("adding new amount")
          database.child("users").child(user).child("pulls").update({"amount": current_pulls + speed})
          print("added new amount")
        elif current_pulls > max_pulls:
          print("User has more pulls than max, can't give more.")
        elif remaining_slots == 0:
          print("User has max pulls. Can't add more.")
        elif remaining_slots < max_pulls:
          database.child("users").child(user).child("pulls").update({"amount": max_pulls})
      elif not database.child("users").child(user).child("pulls").get().val():
        print("Not in data")
      time.sleep(0.5)
      

  @loopadd.before_loop
  async def before_printer(self):
      print('waiting...')
      await self.client.wait_until_ready()

  @commands.command()
  async def startloop(self,ctx):
    self.loopadd.start()
        
def setup(client):
  client.add_cog(pulladd(client))