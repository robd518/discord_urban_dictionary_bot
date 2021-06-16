#!/usr/bin/python3

import asyncio
import re

async def parse_inventory(embed):
    ''' Parse out the player's inventory into a dictionary of
        { "Item" : Count }

        Returns: player_inventory
    '''

    player_inventory = {}

    for field in embed.fields:
        for value in field.value.split("\n"):
            match = re.search(r"(.+\*{2}(.+?)\*{2}\:\s)?(?(1)(\d{1,})|.+\*{2}(.+?)\*{2})", value)
            if match.group(2) and match.group(3):
                player_inventory[match.group(2).lower()] = int(match.group(3))
            elif match.group(4):
                player_inventory[match.group(4)] = 1
            else:
                pass
                
    return player_inventory