#Making it easy....
#thanks to @ranger_op


import shlex
import os
from os import getcwd
from os.path import basename, join
from textwrap import wrap
from typing import Optional, Tuple

import numpy as np

try:
    from colour import Color as asciiColor
except:
    os.system("pip install colour")
from PIL import Image, ImageDraw, ImageFont
from telethon.errors.rpcerrorlist import YouBlockedUserError
from wand.color import Color
from wand.drawing import Drawing
from wand.image import Image as hellimage
import re
import time
import urllib.request
import zipfile
from random import choice
import asyncio
import PIL.ImageOps
import requests
from telethon.tl.types import Channel, PollAnswer
from validators.url import url
from bs4 import BeautifulSoup
from asyncio import sleep
from emoji import get_emoji_regexp

MARGINS = [50, 150, 250, 350, 450]


async def runcmd(cmd: str) -> Tuple[str, str, int, int]:
    args = shlex.split(cmd)
    process = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return (
        stdout.decode("utf-8", "replace").strip(),
        stderr.decode("utf-8", "replace").strip(),
        process.returncode,
        process.pid,
    )


# For using gif , animated stickers and videos in some parts , this
# function takes  take a screenshot and stores ported from userge


async def take_screen_shot(
    video_file: str, duration: int, path: str = ""
) -> Optional[str]:
    print(
        "[[[Extracting a frame from %s ||| Video duration => %s]]]",
        video_file,
        duration,
    )
    ttl = duration // 2
    thumb_image_path = path or os.path.join("./temp/", f"{basename(video_file)}.jpg")
    command = f"ffmpeg -ss {ttl} -i '{video_file}' -vframes 1 '{thumb_image_path}'"
    err = (await runcmd(command))[1]
    if err:
        print(err)
    return thumb_image_path if os.path.exists(thumb_image_path) else None


async def make_gif(event, file):
    chat = "@tgstogifbot"
    async with event.client.conversation(chat) as conv:
        try:
            await silently_send_message(conv, "/start")
            await event.client.send_file(chat, file)
            response = await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
            if response.text.startswith("Send me an animated sticker!"):
                return "`This file is not supported`"
            response = response if response.media else await conv.get_response()
            hellresponse = response if response.media else await conv.get_response()
            await event.client.send_read_acknowledge(conv.chat_id)
            hellfile = await event.client.download_media(hellresponse, "./temp")
            return await unzip(hellfile)
        except YouBlockedUserError:
            return "Unblock @tgstogifbot"


async def silently_send_message(conv, text):
    await conv.send_message(text)
    response = await conv.get_response()
    await conv.mark_read(message=response)
    return response


async def thumb_from_audio(audio_path, output):
    await runcmd(f"ffmpeg -i {audio_path} -filter:v scale=500:500 -an {output}")

async def covidindia(state):
    hburl = "https://www.mohfw.gov.in/data/datanew.json"
    req = requests.get(hburl).json()
    for i in states:
        if i == state:
            return req[states.index(i)]
    return None

async def simpmusic(simp , QUALITY):
  search = simp
  headers = {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}
  html = requests.get('https://www.youtube.com/results?search_query='+search, headers=headers).text
  soup = BeautifulSoup(html, 'html.parser')
  for link in soup.find_all('a'):
    if '/watch?v=' in link.get('href'):
        # May change when Youtube Website may get updated in the future.
        video_link = link.get('href') 
        break
  video_link =  'http://www.youtube.com/'+video_link
  command = ('youtube-dl --extract-audio --audio-format mp3 --audio-quality ' + QUALITY + ' ' + video_link)	
  os.system(command)

song_dl = "youtube-dl --force-ipv4 --write-thumbnail -o './temp/%(title)s.%(ext)s' --extract-audio --audio-format mp3 --audio-quality {QUALITY} {video_link}"
thumb_dl = "youtube-dl --force-ipv4 -o './temp/%(title)s.%(ext)s' --write-thumbnail --skip-download {video_link}"
video_dl = "youtube-dl --force-ipv4 --write-thumbnail  -o './temp/%(title)s.%(ext)s' -f '[filesize<20M]' {video_link}"
name_dl = (
    "youtube-dl --force-ipv4 --get-filename -o './temp/%(title)s.%(ext)s' {video_link}"
)

async def simpmusicvideo(simp):
    search = simp
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}
    html = requests.get('https://www.youtube.com/results?search_query='+search, headers=headers).text
    soup = BeautifulSoup(html, 'html.parser')
    for link in soup.find_all('a'):
        if '/watch?v=' in link.get('href'):
            # May change when Youtube Website may get updated in the future.
            video_link = link.get('href') 
            break    
    video_link =  'http://www.youtube.com/'+video_link
    command = ('youtube-dl -f "[filesize<20M]" ' +video_link)  
    os.system(command)

#convertion..

def convert_toimage(image):
    img = Image.open(image)
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save("./temp/temp.jpg", "jpeg")
    os.remove(image)
    return "./temp/temp.jpg"


async def convert_tosticker(image):
    img = Image.open(image)
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save("./temp/temp.webp", "webp")
    os.remove(image)
    return "./temp/temp.webp"
    
async def invert_colors(imagefile, endname):
    image = Image.open(imagefile)
    inverted_image = PIL.ImageOps.invert(image)
    inverted_image.save(endname)


async def flip_image(imagefile, endname):
    image = Image.open(imagefile)
    inverted_image = PIL.ImageOps.flip(image)
    inverted_image.save(endname)


async def grayscale(imagefile, endname):
    image = Image.open(imagefile)
    inverted_image = PIL.ImageOps.grayscale(image)
    inverted_image.save(endname)


async def mirror_file(imagefile, endname):
    image = Image.open(imagefile)
    inverted_image = PIL.ImageOps.mirror(image)
    inverted_image.save(endname)


async def solarize(imagefile, endname):
    image = Image.open(imagefile)
    inverted_image = PIL.ImageOps.solarize(image, threshold=128)
    inverted_image.save(endname)
    
    
#pranks....
#source - https://nekobot.xyz/api

    
async def iphonex(text):
    r = requests.get(f"https://nekobot.xyz/api/imagegen?type=iphonex&url={text}").json()
    kraken = r.get("message")
    hellurl = url(kraken)
    if not hellurl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(kraken).content)
    img = Image.open("temp.png").convert("RGB")
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"


async def baguette(text):
    r = requests.get(
        f"https://nekobot.xyz/api/imagegen?type=baguette&url={text}"
    ).json()
    kraken = r.get("message")
    hellurl = url(kraken)
    if not hellurl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(kraken).content)
    img = Image.open("temp.png").convert("RGB")
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"
    
    
async def threats(text):
    r = requests.get(f"https://nekobot.xyz/api/imagegen?type=threats&url={text}").json()
    kraken = r.get("message")
    hellurl = url(kraken)
    if not hellurl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(kraken).content)
    img = Image.open("temp.png")
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"


async def lolice(text):
    r = requests.get(f"https://nekobot.xyz/api/imagegen?type=lolice&url={text}").json()
    kraken = r.get("message")
    hellurl = url(kraken)
    if not hellurl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(kraken).content)
    img = Image.open("temp.png")
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"


async def trash(text):
    r = requests.get(f"https://nekobot.xyz/api/imagegen?type=trash&url={text}").json()
    kraken = r.get("message")
    hellurl = url(kraken)
    if not hellurl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(kraken).content)
    img = Image.open("temp.png")
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"


async def awooify(text):
    r = requests.get(f"https://nekobot.xyz/api/imagegen?type=awooify&url={text}").json()
    kraken = r.get("message")
    hellurl = url(kraken)
    if not hellurl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(kraken).content)
    img = Image.open("temp.png")
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"


async def trap(text1, text2, text3):
    r = requests.get(
        f"https://nekobot.xyz/api/imagegen?type=trap&name={text1}&author={text2}&image={text3}"
    ).json()
    kraken = r.get("message")
    hellurl = url(kraken)
    if not hellurl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(kraken).content)
    img = Image.open("temp.png")
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"


async def phcomment(text1, text2, text3):
    r = requests.get(
        f"https://nekobot.xyz/api/imagegen?type=phcomment&image={text1}&text={text2}&username={text3}"
    ).json()
    kraken = r.get("message")
    hellurl = url(kraken)
    if not hellurl:
        return "check syntax once more"
    with open("temp.png", "wb") as f:
        f.write(requests.get(kraken).content)
    img = Image.open("temp.png")
    if img.mode != "RGB":
        img = img.convert("RGB")
    img.save("temp.jpg", "jpeg")
    return "temp.jpg"

#tweets...
#source - https://nekobot.xyz/api

async def trumptweet(text):
        r = requests.get(
            f"https://nekobot.xyz/api/imagegen?type=trumptweet&text={text}").json()
        wew = r.get("message")
        hburl = url(wew)
        if not hburl:
            return  "check syntax once more"
        with open("temp.png", "wb") as f:
            f.write(requests.get(wew).content)
        img = Image.open("temp.png").convert("RGB")
        img.save("temp.jpg", "jpeg")    
        return "temp.jpg"

async def changemymind(text):
        r = requests.get(
            f"https://nekobot.xyz/api/imagegen?type=changemymind&text={text}").json()
        wew = r.get("message")
        hburl = url(wew)
        if not hburl:
            return  "check syntax once more"
        with open("temp.png", "wb") as f:
            f.write(requests.get(wew).content)
        img = Image.open("temp.png").convert("RGB")
        img.save("temp.jpg", "jpeg")    
        return "temp.jpg"
    
async def kannagen(text):
        r = requests.get(
            f"https://nekobot.xyz/api/imagegen?type=kannagen&text={text}").json()
        wew = r.get("message")
        hburl = url(wew)
        if not hburl:
            return  "check syntax once more"
        with open("temp.png", "wb") as f:
            f.write(requests.get(wew).content)
        img = Image.open("temp.png").convert("RGB")
        img.save("temp.webp", "webp")    
        return "temp.webp"    
    
async def moditweet(text):
        r = requests.get(
            f"https://nekobot.xyz/api/imagegen?type=tweet&text={text}&username=narendramodi").json()
        wew = r.get("message")
        hburl = url(wew)
        if not hburl:
            return  "check syntax once more"
        with open("temp.png", "wb") as f:
            f.write(requests.get(wew).content)
        img = Image.open("temp.png").convert("RGB")
        img.save("temp.jpg", "jpeg")    
        return "temp.jpg"    
        
        
async def miatweet(text):
        r = requests.get(
            f"https://nekobot.xyz/api/imagegen?type=tweet&text={text}&username=miakhalifa").json()
        wew = r.get("message")
        hburl = url(wew)
        if not hburl:
            return  "check syntax once more"
        with open("temp.png", "wb") as f:
            f.write(requests.get(wew).content)
        img = Image.open("temp.png").convert("RGB")
        img.save("temp.jpg", "jpeg")    
        return "temp.jpg"    


async def papputweet(text):
        r = requests.get(
            f"https://nekobot.xyz/api/imagegen?type=tweet&text={text}&username=rahulgandhi").json()
        wew = r.get("message")
        hburl = url(wew)
        if not hburl:
            return  "check syntax once more"
        with open("temp.png", "wb") as f:
            f.write(requests.get(wew).content)
        img = Image.open("temp.png").convert("RGB")
        img.save("temp.jpg", "jpeg")    
        return "temp.jpg"

async def sunnytweet(text):
        r = requests.get(
            f"https://nekobot.xyz/api/imagegen?type=tweet&text={text}&username=sunnyleone").json()
        wew = r.get("message")
        hburl = url(wew)
        if not hburl:
            return  "check syntax once more"
        with open("temp.png", "wb") as f:
            f.write(requests.get(wew).content)
        img = Image.open("temp.png").convert("RGB")
        img.save("temp.jpg", "jpeg")    
        return "temp.jpg"    

async def sinstweet(text):
        r = requests.get(
            f"https://nekobot.xyz/api/imagegen?type=tweet&text={text}&username=johnnysins").json()
        wew = r.get("message")
        hburl = url(wew)
        if not hburl:
            return  "check syntax once more"
        with open("temp.png", "wb") as f:
            f.write(requests.get(wew).content)
        img = Image.open("temp.png").convert("RGB")
        img.save("temp.jpg", "jpeg")    
        return "temp.jpg" 
    
async def tweets(text1,text2):
        r = requests.get(
            f"https://nekobot.xyz/api/imagegen?type=tweet&text={text1}&username={text2}").json()
        wew = r.get("message")
        hburl = url(wew)
        if not hburl:
            return  "check syntax once more"
        with open("temp.png", "wb") as f:
            f.write(requests.get(wew).content)
        img = Image.open("temp.png").convert("RGB")
        img.save("temp.jpg", "jpeg")    
        return "temp.jpg"    

#sticker text

EMOJI_PATTERN = re.compile(
    "["
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F700-\U0001F77F"  # alchemical symbols
    "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
    "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
    "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
    "\U0001FA00-\U0001FA6F"  # Chess Symbols
    "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
    "\U00002702-\U000027B0"  # Dingbats
    "]+"
)


def deEmojify(inputString: str) -> str:
    """Remove emojis and other non-safe characters from string"""
    return re.sub(EMOJI_PATTERN, "", inputString)

async def waifutxt(text, chat_id, reply_to_id, bot, borg):
    animus = [
        0,
        1,
        2,
        3,
        4,
        9,
        15,
        20,
        22,
        27,
        29,
        32,
        33,
        34,
        37,
        38,
        41,
        42,
        44,
        45,
        47,
        48,
        51,
        52,
        53,
        55,
        56,
        57,
        58,
        61,
        62,
        63,
    ]
    sticcers = await bot.inline_query("stickerizerbot", f"#{choice(animus)}{text}")
    hell = await sticcers[0].click("me", hide_via=True)
    if hell:
        await bot.send_file(int(chat_id), hell, reply_to=reply_to_id)
        await hell.delete()
