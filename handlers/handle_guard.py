#!/usr/bin/python3

captchas = {
    "https://cdn.discordapp.com/attachments/703333986042380411/709454247351025744/epic_guard.png": "wolf skin",
    "https://cdn.discordapp.com/attachments/703333986042380411/709443647388516432/epic_guard.png": "apple",
    "https://cdn.discordapp.com/attachments/703333986042380411/709441377666203658/epic_guard.png": "golden fish",
    "https://cdn.discordapp.com/attachments/703333986042380411/709427399787282512/epic_guard.png": "banana",
    "https://cdn.discordapp.com/attachments/703333986042380411/709256572777267250/epic_guard.png": "zombie eye",
    "https://cdn.discordapp.com/attachments/703333986042380411/709522524261842964/epic_guard.png": "zombie eye",
    "https://cdn.discordapp.com/attachments/703333986042380411/709231236471717908/epic_guard.png": "epic coin",
    "https://cdn.discordapp.com/attachments/703333986042380411/709219030434709604/epic_guard.png": "normie fish",
    "https://cdn.discordapp.com/attachments/703333986042380411/709053020180054016/epic_guard.png": "life potion",
    "https://cdn.discordapp.com/attachments/703333986042380411/709031733504245840/epic_guard.png": "golden coin"
}

def handle_guard(message):
    print(f"{message.guild} | {message.channel} | {message.author} | {message.content}")
    print(message.attachments)

    if message.attachments[0].url in captchas:
        return captchas[message.attachments[0].url]

    else:
        return "not found"