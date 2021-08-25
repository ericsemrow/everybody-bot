import discord
import os
import keepalive
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
    content = message.content[2:]
    editable = await getExistingMessage(message)
    if editable is not None:
      await editable.edit(content=content)
    else:
      newMsg = await message.channel.send(content)
      db[str(message.channel.id)] = newMsg.id

    # if there's an everybody-bot-log channel then
    # plop the message in there for posterity
    logChannel = getLogChannel(message)
    if logChannel is not None:
      await logChannel.send(f"```{content}``` by {message.author} in <#{message.channel.id}>")

    # the user's message has to be cleaned up
    await message.delete()


async def getExistingMessage(message):
  channelId = str(message.channel.id)
  if channelId in db:
    existingMessageId = db[channelId]
    try:
      return await message.channel.fetch_message(existingMessageId)
    except discord.errors.NotFound:
      pass
  return None

def getLogChannel(message):
  return discord.utils.get(message.guild.channels, name="everybody-bot-log")

keepalive.keep_alive()
token = os.environ.get("DISCORD_TOKEN") 
client.run(token)