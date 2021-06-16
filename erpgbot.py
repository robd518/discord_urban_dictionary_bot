#!/usr/bin/python3
import logging
import random
import os
import re
import discord
from discord.ext import commands
import asyncio
from dotenv import load_dotenv
load_dotenv()

from handlers import *
from helpers import *


class ERPGBot(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Read env vars
        self.bot_stuff_channel = int(os.getenv("EPIC_RPG_BOT_CHANNEL"))
        self.work_command = os.getenv("WORK_COMMAND")
        self.hp_threshold = int(os.getenv("HP_THRESHOLD"))

        # Set up logging
        self.logger = logging.getLogger("discord")
        self.logger.setLevel(logging.DEBUG)
        self.handler = logging.FileHandler(filename="log/erpgbot.log", encoding="utf-8", mode="w")
        self.handler.setFormatter(logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))
        self.logger.addHandler(self.handler)

        # Set up our queue
        self.msg_queue = asyncio.PriorityQueue()
        
        # Initialize an empty variable to hold the channel ID.  We set this at 0
        # to start so that we can wait for the channels to be populated.  Normally
        # these would get populated after waiting for ready, but this doesn't
        # work when bot=False is set in the client at runtime
        self.channel = 0

        # Set up our handler classes (if they're classes)
        self.training_handler = HandleTraining()

        # Keep a list of various actions to perform with our queue handler
        self.ready_actions_todo = []
        self.inventory_actions_todo = []

        # Keep an up-to-date dictionary of our player's inventory
        self.player_inventory = {}

        # create our background tasks
        self.loop.create_task(self.perform_action_handler())
        self.loop.create_task(self.perform_ready_check_handler())
        self.loop.create_task(self.perform_inventory_handler())


    async def on_ready(self):
        print("We're ready!")

    async def on_message(self, message):

        # Ignore messages from "EPIC RPG Support Server" explicitly
        if str(message.guild) == "EPIC RPG Support Server":
            return

        # Ignore messages that aren't in the bot channel
        elif message.channel.id != self.bot_stuff_channel:
            return

        # Detect the EPIC GUARD captcha and shut 'er down until we can reliably solve captcha
        elif message.content.startswith(f':police_car: **EPIC GUARD**: stop there, <@{client.user.id}>'):
            guard_answer = handle_guard(message)
            print(f"GUARD ANSWER: {guard_answer}")
            if guard_answer == "none found":
                await self.close()
            else:
                await self.msg_queue.put((0, guard_answer))

        # Handle "IN THE JAIL" events:
        elif f"{client.user.name} is now in the jail!" in message.content:
            await self.close()

        # Handle healing ones self
        elif message.content.startswith(f'**{client.user.name}** found'):
            if (handle_life_check(message.content, self.hp_threshold) == True) or (r'**Your horse** saved you') in message.content:
                await self.msg_queue.put((1, "rpg heal"))

        # Handle receiving a lootbox
        elif re.search(r'.+got (a|an)\s(.+lootbox)\s', message.content):
            match = re.search(r'.+got (a|an)\s(.+lootbox)\s', message.content).group(2).lower()
            await self.msg_queue.put((2, f"rpg open {match}"))

        # Handle "GOD DROPPED" events
        elif (message.author == "EPIC RPG#4117") and ("OOPS! God accidentally dropped" in message.embeds[0].fields[0].name):
            god_made_me_say = re.search(r'\*{2}(.+?)\*{2}', message.embeds[0].fields[0].value).group(1)
            print(f"GOD MADE ME SAY IT: {god_made_me_say}")
            await self.msg_queue.put((0, god_made_me_say))


        # "RPG DUEL" - Handle duel requests
        elif f'rpg duel <@{client.user.id}>' in message.content.lower():
            await asyncio.sleep(1)
            await handle_duels(self.msg_queue)

        # "RPG TRAINING" - Handle training messages
        elif message.content.startswith(f'**{client.user.name}** is training in the'):
            training_answer = self.training_handler.handle_training(message.content, self.player_inventory)
            await self.msg_queue.put((0, training_answer))

        # "RPG RD" - Parse 'rpg rd' responses and place ready actions into self.ready_actions_todo
        elif (message.embeds) and (message.embeds[0].author.name == f"{client.user.name}'s ready"):
            self.ready_actions_todo = await parse_cooldown(message.embeds[0])
            while self.ready_actions_todo:
                action = self.ready_actions_todo.pop(0)
                if action == "chop | fish | pickup | mine":
                    action = self.work_command
                if action == "adventure":
                    await self.msg_queue.put((1, "rpg heal"))

                await self.msg_queue.put((2, f'rpg {action}'))

        # "RPG INVENTORY" - Parse 'rpg inventory' responses and put into self.player_inventory,
        # then put inventory actions onto the queue
        elif (message.embeds) and (message.embeds[0].author.name == f"{client.user.name}'s inventory"):
            self.player_inventory = await parse_inventory(message.embeds[0])
            self.inventory_actions_todo = await handle_inventory(self.player_inventory)
            while self.inventory_actions_todo:
                action = self.inventory_actions_todo.pop(0)
                await self.msg_queue.put((action[0], f'rpg {action[1]}'))

        
        # Print everything
        print(f"{message.guild} | {message.channel} | {message.author} | {message.content} | {message.attachments}")
        self.print_embeds(message.embeds)

    async def perform_action_handler(self):
        ''' This is the FIFO queue that will accept action commands
            that will be sent to the channel to be read/handled by
            the Epic RPG Bot.  It uses the following priorities.
            0 : must be done immediately because of blocking by the bot
            1 : things like healing or buying potions when empty
            2 : last priority / do whenever
        '''

        await asyncio.sleep(5)
        self.channel = self.get_channel(self.bot_stuff_channel)

        while True:
            msg = await self.msg_queue.get()
            await self.channel.send(msg[1])
            self.msg_queue.task_done()
            await asyncio.sleep(5)

    async def perform_ready_check_handler(self):
        ''' Perform a ready check every (n) seconds'''

        while True:
            # If the queue is empty and there's no items in self.ready_actions_todo, 
            # put a ready check into the queue
            if (self.msg_queue.empty()) and not (self.ready_actions_todo):
                await self.msg_queue.put((2, 'rpg rd'))
        
            await asyncio.sleep(65)

    async def perform_inventory_handler(self):
        ''' Every (n) seconds, perform an 'rpg inventory' '''

        while True:
            await self.msg_queue.put((2, 'rpg inventory'))
            await asyncio.sleep(300)


    # Pretty print message embeds (for testing)
    def print_embeds(self, embeds):
        for embed in embeds:
            print("=====================\n" \
            f"Author: {embed.author.name}\n" \
            f"Title: {embed.title}\n" \
            f"Description: {embed.description}\n" \
            f"URL: {embed.url}\n" \
            "---------------\n")

            for field in embed.fields:
                print("%s" % field.name)
                print("------------------")

                for each in field.value.split("\n"):
                    print("%s" % each)
            print("=====================")


client = ERPGBot()
client.run(os.getenv("DISCORD_TOKEN"), bot=False)