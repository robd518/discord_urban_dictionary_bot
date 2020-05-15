#!/usr/bin/python3
import random
import os
import re
import discord
from discord.ext import commands
import asyncio
from dotenv import load_dotenv
load_dotenv()

user_token = os.getenv("DISCORD_TOKEN")
bot_stuff_channel = int(os.getenv("EPIC_RPG_BOT_CHANNEL"))
client = discord.Client()

@client.event
async def on_ready():
    print("Ready!")

@client.event
async def on_message(message):

    # if message.author == client.user and message.channel.id == bot_stuff_channel and message.content == sleeper_cmd:
    #     await client.close()

    if str(message.guild) == "EPIC RPG Support Server":
        return

    elif message.channel.id != bot_stuff_channel:
        return

    # Detect the EPIC GUARD captcha and shut 'er down
    elif message.content.startswith(r':police_car: **EPIC GUARD**: stop there'):
        print("%s | %s | %s | %s" % (message.guild, message.channel, message.author, message.content))
        await client.close()

    # Handle healing ones self
    elif message.content.startswith(r'**mudda** found'):
        if (check_life(message.content) == True) or ("Your horse saved you") in message.content:
            channel = client.get_channel(bot_stuff_channel)
            await asyncio.sleep(5)
            await channel.send("rpg heal")
        
        print("%s | %s | %s | %s" % (message.guild, message.channel, message.author, message.content))

    else:
        print("%s | %s | %s | %s" % (message.guild, message.channel, message.author, message.content))

# Function for doing work tasks (i.e. axe, net, pickup)
async def work_task():
    await asyncio.sleep(30)
    channel = client.get_channel(bot_stuff_channel)
    while not client.is_closed():
        await channel.send("rpg axe")
        await asyncio.sleep(random.randint(300,310))

# Function for hunting
async def hunt_task():
    await asyncio.sleep(5)
    channel = client.get_channel(bot_stuff_channel)
    while not client.is_closed():
        await channel.send("rpg hunt")
        await asyncio.sleep(random.randint(60.70))

# Check life
def check_life(message):
    try:
        # Check if life is below 120
        if int(re.search('\d{1,3}\/\d{3}', message).group(0).split('/')[0]) <= 120:
            return True
        else:
            return False
    
    except AttributeError:
        return

client.loop.create_task(work_task())
client.loop.create_task(hunt_task())

client.run(user_token, bot=False)