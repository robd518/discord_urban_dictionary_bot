#!/usr/bin/python3
import re
import asyncio

async def parse_cooldown(embed):
    ''' We want to check our "ready" cooldown, parse it,
        and shove it into a list.  If it's in the list,
        that means it's ready and we can run that action 
        in the box (aka: it's not on cooldown)

        Returns: []
    '''

    events_to_ignore = [
        "lootbox",
        "duel",
        "quest | epic quest",
        "horse breeding | horse race",
        "arena",
        "dungeon | miniboss"
    ]

    ready_events = []

    if embed.fields:
        for field in embed.fields:
            for value in field.value.split("\n"):
                parsed_value = re.search(r'^.+`(.+?)`', value).group(1).lower()
                if parsed_value not in events_to_ignore:
                    ready_events.append(parsed_value)

    return ready_events