#!/usr/bin/python3
import asyncio
import random

async def handle_duels(msg_queue):
    if not msg_queue.empty():
        await msg_queue.put((0, random.choice([
            "Hold up one sec",
            "wait one sec then try again",
            "one sec, then try"
        ])))
    else:
        await msg_queue.put((0, "yes"))
        await msg_queue.put((1, random.choice(['A', 'B', 'C'])))