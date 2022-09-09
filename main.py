import discord
import os
import requests
import json
from random import randint
from replit import db
from keep_alive import keep_alive



intents = discord.Intents.all()
intents.typing = False

client = discord.Client(intents=intents)


def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + '\n      -' + json_data[0]['a']
  return (quote)


quote_lst = ["haha", "hehe", "lol"]
index = 0


def update_jokes(msg):
  if "jokes" in db.keys():
      jokes = db["jokes"]
      jokes.append(msg)
      db['jokes'] = jokes
  else:
      db['jokes'] = [msg]
  pass


def delete_joke(num):
  jokes = db['jokes']
  if len(jokes) > num:
      del jokes[num]
  db['jokes'] = jokes
  pass


def randomizer():
    index = randint(0, len(quote_lst))
    return index


@client.event
async def on_ready():
    print("meow im awake")


@client.event
async def on_message(message):
  if message.author == client.user:
      return

  msg = message.content

  if msg.startswith('$meow'):
      await message.channel.send('meow!')

  if msg.startswith('$quote'):
      quote = get_quote()
      await message.channel.send(quote)
  


  if msg.startswith('$help'):
      await message.channel.send(
          "ฅ^•ﻌ•^ฅ meow! Here's a list of the commands. \nStart every command with $:\nhelp\nmeow\nquote\njoke"
      )

  if 'jokes' in db.keys():
      options = db['jokes']
      for joke in db['jokes']:
          if joke not in options:
              options.append(joke)
      for joke in quote_lst:
          if joke not in options:
              options.append(joke)

  if msg.endswith('$joke'):
      new = randomizer()
      print(options)
      await message.channel.send(options[new])

  if msg.startswith("$new"):
      new_joke = msg.split("$new ", 1)[1]
      update_jokes(new_joke)
      await message.channel.send("new joke added. meow!")

  if msg.startswith("$del"):
      jokes = []
      if "jokes" in db.keys():
          new_index = int(msg.split("$del", 1)[1])
          delete_joke(new_index)
      await message.channel.send('i have successfully deleted the joke. 😿')

  if msg.startswith('$jokes'):
      jokes = [joke for joke in db['jokes']]
      await message.channel.send(jokes)

keep_alive()
client.run(os.environ['TOKEN1'])
