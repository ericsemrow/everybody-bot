import discord
import os
from replit import db

client = discord.Client()

@client.event 
async def on_message(message):     
    if message.author != client.user:         
        await message.channel.send(message.content[::-1])

token = os.environ.get("DISCORD_TOKEN") 
client.run(token)