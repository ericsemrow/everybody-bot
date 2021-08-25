import discord
import os
from replit import db

client = discord.Client()
print( "Starting" )

@client.event
async def on_ready():
    print("Online")

@client.event 
async def on_message(message):
  #messages must begin with $$   
  if message.author != client.user and message.content.startswith("$$"):
    # stringify the channel id and strip off the $$
    channelId = str(message.channel.id)
    content = message.content[2:]
    if channelId in db:
      # If there's already an everybot message in this
      # channel then grab its ID and lets reuse it
      existingMessageId = db[channelId]
      try:
        editable = await message.channel.fetch_message(existingMessageId)
        await editable.edit(content=content)
      # make sure you catch the error if the message 
      # you thought was there got deleted somehow
      except discord.errors.NotFound:
        # send the new message and log its id to reuse next time
        newMsg = await message.channel.send(content)
        db[channelId] = newMsg.id

    else:
      newMsg = await message.channel.send(content)
      db[channelId] = newMsg.id

    # the user's message has to be cleaned up
    await message.delete()


token = os.environ.get("DISCORD_TOKEN") 
client.run(token)