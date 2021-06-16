#!/usr/bin/python3
import requests
from PIL import Image
from io import BytesIO

matches = {
    (237, 28, 36, 255) : "apple",
    (253, 215, 0, 255) : "banana",
    (47, 21, 62, 255) : "epic coin",
    (255, 204, 0, 255) : "golden fish",
    (255, 242, 0, 255) : "golden coin",
    (217, 17, 27, 255) : "life potion",
    (0, 198, 255, 255) : "normie fish",
    (255, 21, 21, 255) : "ruby",
    (255, 130, 170, 255) : "unicorn horn",
    (46, 46, 52, 255) : "wolf skin",
    (77, 98, 11, 255) : "zombie eye"
}

def handle_guard(message):

    r = requests.get(message.attachments[0].url)
    img = Image.open(BytesIO(r.content))
    pixel_data = set(img.getdata())
    for k, v in matches.items():
        if k in pixel_data:
            return matches[k]
    
    return "none found"