import os
import discord
import requests
import json
import random
from replit import db
import keep_alive

client= discord.Client()

sad_words=["sad","depressed","heartbroken","unhappy","miserable","depressing","angry","regretful","lonely","tragedy","joyless","low spirited","regret","depressing"]

encouragement=["Cheer up!","Hang in there!","You are a great person!","Don't give up","Keep fighting!","Come on! You can do it!","Never give up"]

if 'responding' not in db.keys():
  db["responding"]=True

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data=json.loads(response.text)
  quote = json_data[0]['q'] + " - " + json_data[0]['a']
  return(quote)

@client.event
async def on_ready():
  print("we have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
  if message.author==client.user:
    return
  #send quotes
  msg= message.content
  if message.content.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)
  #encouragement
  if db['responding']:
    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(encouragement))
  #turn on and off
  if msg.startswith("$respond"):
    value = msg.split("$respond ",1)[1]
    if value.lower()=="on":
      db["responding"]=True
      await message.channel.send("Hurray! I'm back")
    if value.lower()=="off":
      db["responding"]=False
      await message.channel.send("I'll keep quite")

keep_alive.keep_alive()
client.run(os.environ['Token'])