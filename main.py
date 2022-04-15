import os, discord
from tinydb import TinyDB, Query

db = TinyDB('/opt/storage/db.json')
client = discord.Client()

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
    try:
      if editable is not None:
        await editable.edit(content=content)
      else:
        newMsg = await message.channel.send(content)
        q = Query()
        db.upsert({'messageId': newMsg.id, 'id': message.channel.id}, q.id == message.channel.id)
    except Exception as e:
      print (f'Permission error when sending update or fresh message: {e}')

    # if there's an everybody-bot-log channel then
    # plop the message in there for posterity
    logChannel = getLogChannel(message)
    try:
      if logChannel is not None:
        await logChannel.send(f'```{content}``` by {message.author} in <#{message.channel.id}>')
    except Exception as e:
      print(f'Permission issue sending log message: {e}')
    # the user's message has to be cleaned up

    try:
      await message.delete()
    except Exception as e:
      print(f'Permission issue deleting old message: {e}')


async def getExistingMessage(message):
  channelId = str(message.channel.id)
  q = Query()
  # get first element off array or else None
  prev = next(iter(db.search(q.id == message.channel.id)), None)
  if prev and 'messageId' in prev:
    existingMessageId = prev["messageId"]
    try:
      return await message.channel.fetch_message(existingMessageId)
    except discord.errors.NotFound:
      pass
  return None

def getLogChannel(message):
  return discord.utils.get(message.guild.channels, name="everybody-bot-log")

token = os.environ.get("DISCORD_TOKEN")
client.run(token)