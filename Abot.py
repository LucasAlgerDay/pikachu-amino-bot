from keep_alive import keep_alive
keep_alive()
from BotAmino import BotAmino
from alice import chatbot
import sys
import threading
from threading import Thread, Lock
import os
from os import system, urandom, path
import ast
import re
import urllib
import urllib.request
from typing import List
import string
import hmac
import hashlib
from hashlib import sha1
import pytz
import time
import datetime
from datetime import datetime
from dateutil import parser
from time import sleep
import base64
from uuid import uuid4
from io import BytesIO
import requests
import ujson as json
from gtts import gTTS, lang
from contextlib import suppress
from pathlib import Path
from functools import wraps
from pymongo import MongoClient
from PIL import Image, ImageFont, ImageDraw
from easy_pil import Editor, Canvas, load_image, Font
import io
from zipfile import ZipFile
import unicodedata
from unicodedata import normalize
from string import punctuation
from random import uniform, choice, randint
from youtube_search import YoutubeSearch
from yt_dlp import YoutubeDL
from google_trans_new import google_translator
from constant import LANGUAGES,DEFAULT_SERVICE_URLS
from amino.lib.util.helpers import decode_sid, sid_to_uid
from sid import sid_e
from json import dumps, load
import random

path_utilities = "utilities"
path_download = "audio"
path_lock = f"{path_utilities}/locked"

client = BotAmino(secret="31 BLluWzPZ 3c6308c5-e5ec-4d60-b7d6-1730382c6703 42.110.171.52 cdc1ac5d08ac01ad9ff9c9fe7b56030c20a760fc 1 1673002475 OWCrmEZAYzlyN_0Y6hMsM0fbQ-o")
client.prefix = "/"
client.activity = "True"
clie = MongoClient("mongodb+srv://vedansh121:vedansh121@cluster0.h3erwet.mongodb.net/?retryWrites=true&w=majority")

def print_exception(exc):
    print(repr(exc))


def nope(data):
    return False

def is_it_me(data):
    return data.authorId in ('4bdde85c-7d9b-4258-8473-84af3186a7f9')

def is_staff(data):
    return data.authorId in ('4bdde85c-7d9b-4258-8473-84af3186a7f9') or data.subClient.is_in_staff(data.authorId)

Message =  None
Messages = None
stored_messages: List[Message] = []
deleted_messages: List[Messages] = []

def all_data(data):
    stored_messages.append(data.json)

@client.on_delete()
def remove(data):
    for message in stored_messages:
        id = message['messageId']
        if id == data.messageId:
            tipo = message['mediaType']
            if tipo == 0:
                contentt =  message['content']
            else:
                contentt =  message['mediaValue']
            chat = message['threadId']
            author = data.author
            message  = {'chatId': chat, 'content': contentt, 'author': author}
            deleted_messages.append(message)
            chatlink = f"ndc://x{data.comId}/chat-thread/{data.chatId}"
            val = data.subClient.get_chat_thread(data.chatId).title
            ctz = pytz.timezone('Asia/Kolkata')
            chats = data.subClient.favorite_chats
            if val ==None:
                val="Private Chat"
            for id, in zip(chats):
                data.subClient.send_message(chatId=id, message=
f"""[c]Deleted Message

[c]𐄁𐄙𐄁𐄙𐄁𐄙𐄁𐄙𐄁𐄙𐄁𐄙𐄁𐄙𐄁

{contentt}

[c]𐄁𐄙𐄁𐄙𐄁𐄙𐄁𐄙𐄁𐄙𐄁𐄙𐄁𐄙𐄁

Chat : {chatlink}
Time : {datetime.now(ctz).strftime("%H:%M:%S")}""",embedTitle=f"{data.author}",embedLink=f"ndc://x{data.comId}/user-profile/{data.authorId}",embedContent=f"Chat: {val}")
            break

@client.command()
def snipe(data):
    snipe = []
    for message in deleted_messages:
        chatId = message['chatId']
        if data.chatId ==  chatId:
            snipe.append(message)
    if len(snipe) !=0:
        if data.message and not((int(data.message))> len(snipe)):
            amount = int(data.message)
        else:
            amount = 1
        
        message  = f"""[c]Deleted Message
[c]----------------------------------------
Message : {snipe[-amount]['content']}
Deleted By : {snipe[-amount]['author']}
[c]----------------------------------------"""
    else:
        message = "You have 0 deleted messages"
    data.subClient.send_message(data.chatId, message)

def welcome_log(data):
    try:
        op=client.get_from_id(objectId=data.chatId,objectType="12",comId=data.comId).json
        chatlink=op["extensions"]["linkInfo"]["shareURLShortCode"]
    except:
        chatlink="Private Chat"
    val=data.subClient.get_chat_thread(data.chatId).title
    ctz = pytz.timezone('Asia/Kolkata')
    chats=data.subClient.favorite_chats
    if val ==None:
        val="Private Chat"
    for id in chats:
        try:
            data.subClient.send_message(chatId=id,message=f"""{data.author} joined {val}

Chat: {chatlink}

Time : {datetime.now(ctz).strftime("%H:%M:%S")}""",embedTitle=f"{data.author}",embedLink=f"ndc://x{data.comId}/user-profile/{data.authorId}",embedContent=f"Chat: {val}")
        except:
            pass

@client.command(condition=is_staff)
def setbotlog(data):
		if data.chatId not in data.subClient.favorite_chats:
			data.subClient.add_favorite_chats(data.chatId)
			owner_user = data.subClient.get_all_users(type="leaders", start=0, size=25).profile.userId
			another_user = data.subClient.get_all_users(type="curators", start=0, size=25).profile.userId
			category_users = [*owner_user, *another_user]
			for userId in category_users:
			 	data.subClient.invite_to_chat(chatId=data.chatId, userId=userId)
			data.subClient.send_message(data.chatId,message="Botlog GC set")
		else:
			data.subClient.send_message(data.chatId,message="Already Set",replyTo=data.messageId)

@client.command(condition=is_staff)
def usetbotlog(data):
		if data.chatId  in data.subClient.favorite_chats:
			data.subClient.remove_favorite_chats(data.chatId)
			data.subClient.send_message(data.chatId,message="Botlog GC Removed")
		else:
			data.subClient.send_message(data.chatId,message="Already removed",replyTo=data.messageId)

@client.command(condition=is_it_me)
def joinamino(data):
    url = data.message
    code = client.get_from_code(url)
    community_id = code.path[1:code.path.index('/')]
    if 'extensions' in code.json and 'invitationId' in code.json['extensions']:
        invitation_id = code.json['extensions']['invitationId']
        client.join_community(community_id, invitation_id)
    else:
        client.join_community(community_id)
    Thread(target=client.threadLaunch, data=[community_id, True]).start()
    data.subClient.send_message(data.chatId, message="Joined the community")

@client.command()
def cb(data):
    chatbot_ai=chatbot()
    message=f"{data.message}"
    response=chatbot_ai.text(message)
    data.subClient.send_message(data.chatId, message=f"{response}", replyTo=data.messageId)

@client.command()
def tb(data):
    chatbot_ai=chatbot()
    message=f"{data.message}"
    res=chatbot_ai.text(message)
    audio_bytes = BytesIO()
    gTTS(text=res, lang='hi', slow=False).write_to_fp(audio_bytes)
    audio_bytes.seek(0)
    data.subClient.send_message(data.chatId, file=audio_bytes, fileType="audio")

@client.command(condition=is_staff)
def frame(data):
	z=data.subClient.get_user_info(data.authorId).avatarFrameId
	data.subClient.apply_avatar_frame(avatarId=z,applyToAll=False)
	data.subClient.send_message(message="Frame Applied",chatId=data.chatId,replyTo=data.messageId)

@client.command(condition=is_staff)
def bubble(data):
	z=data.subClient.get_user_info(data.authorId).json['extensions']['defaultBubbleId']
	data.subClient.apply_bubble(bubbleId=z,chatId=data.chatId,applyToAll=True)
	data.subClient.send_message(message="Chatbubble Applied",chatId=data.chatId,replyTo=data.messageId)

@client.command()
def startvc(data):
    try:
      data.subClient.delete_message(data.chatId, data.messageId, asStaff=True)
    except:
      data.subClient.delete_message(data.chatId, data.messageId)
    client.start_vc(comId=data.subClient.community_id,chatId=data.chatId,joinType=1)
    data.subClient.send_message(data.chatId, "Started Vc!")

@client.command()
def endvc(data):
      data.subClient.delete_message(data.chatId, data.messageId) 
      client.end_vc(comId=data.subClient.community_id,chatId=data.chatId,joinType=2) 
      data.subClient.send_message(data.chatId, "Ended Vc!")

@client.command()
def startvid(data):
    try:
      data.subClient.delete_message(data.chatId, data.messageId, asStaff=True)
    except:
      data.subClient.delete_message(data.chatId, data.messageId)
    client.start_video_chat(comId=data.subClient.community_id,chatId=data.chatId,joinType=1)
    data.subClient.send_message(data.chatId, "Started Video chat!")

live_vc = False
@client.command()
def startsc(data):
    try:
      data.subClient.delete_message(data.chatId, data.messageId, asStaff=True)
    except:
      data.subClient.delete_message(data.chatId, data.messageId)
    global live_vc
    data.subClient.send_message(data.chatId, "Started Screening!")
    live_vc = True
    while live_vc:
        try:
            client.reps(comId=data.subClient.community_id,chatId=data.chatId,joinType=1)
            time.sleep(10)
            if live_vc == False:
                break
        except Exception:
            return

@client.command()
def endsc(data):
    global live_vc
    live_vc = False
    try:
        client.end_vc(comId=data.subClient.community_id,chatId=data.chatId,joinType=2)
    except Exception:
        pass
    data.subClient.send_message(data.chatId, "Ended Screening!")

@client.command()
def repinfo(data):
	x = data.subClient.get_vc_reputation_info(chatId=data.chatId).availableReputation
	data.subClient.send_message(data.chatId, message=f"AvailableReputation : {x}")

@client.command(condition=is_staff)
def claimrep(data):
    duplicates=[]
    data.subClient.send_message(data.chatId, "Claim started")
    while True:
        x = data.subClient.get_vc_reputation_info(data.chatId)
        time.sleep(5)
        rep=x.availableReputation
        duplicates.append(int(rep))
        if rep >=10:
            x = data.subClient.claim_vc_reputation(data.chatId)
            duplicates.clear()
        g=duplicates.count(rep)
        if g >=6:
          data.subClient.claim_vc_reputation(data.chatId)
          duplicates.clear()

def iucn(d,udd):
	try:
		d.subClient.live_notify(userId=udd,chatId=d.chatId)
	except:
		pass

@client.command()
def notifyall(data):
	h=data.subClient.get_online_users(start=0,size=100).profile.userId
	j=data.subClient.get_online_users(start=0,size=100).profile.nickname
	u=len(j)
	for ud in h:
		Thread(target=iucn,args=(data,ud,)).start()
	data.subClient.send_message(chatId=data.chatId,message=f"Notified {u} members")

def icn(d,udd):
	try:
		d.subClient.invite_to_chat(userId=udd,chatId=d.chatId)
	except:
		pass

@client.command()
def inviteall(data):
	h=data.subClient.get_online_users(start=0,size=100).profile.userId
	j=data.subClient.get_online_users(start=0,size=100).profile.nickname
	u=len(j)
	for ud in h:
		Thread(target=icn,args=(data,ud,)).start()
	data.subClient.send_message(chatId=data.chatId,message=f"Invited {u} members in Chatroom")

@client.command()
def inv(data):
    if "aminoapps.com" in data.message:
    	user=(client.get_from_code(data.message.split(' ')[0]).objectId)
    	data.subClient.invite_to_chat(chatId=data.chatId,userId=user)
    	data.subClient.send_message(chatId=data.chatId, message="Invited")

@client.command()
def inviteglobal(data):
	x=random.randint(40,100)
	a=client.get_all_users(size=100)
	try:
		for userid in a.profile.userId:
			data.subClient.invite_to_chat(data.chatId,userId=userid)
	except Exception:
		pass
	data.subClient.send_message(data.chatId,message=f"Invited {x} members")

@client.command(condition=is_staff)
def vc(data):
    id=data.subClient.get_user_info(userId=data.authorId).userId
    data.subClient.invite_to_vc(userId=id,chatId=data.chatId)

@client.command()
def pvp(data):
    import time
    msg = data.message + " null null "
    msg = msg.split(" ")
    try:
        rounds = int(msg[0])
    except (TypeError, ValueError):
        rounds = 5
        msg[2] = msg[1]
        msg[1] = msg[0]
        msg[0] = 5

    if msg[1] == '' or msg[1] == ' ' or msg[1] == 'null':
        msg[1] = data.author
    if msg[2] == '' or msg[1] == ' ' or msg[2] == 'null':
        msg[2] = data.author
    if msg[1] == msg[2]:
        msg[2] = f'Reverse_{msg[1]}'

    while True:
        try:
            data.subClient.send_message(chatId=data.chatId, message=f"[icu]{data.author} started a PvP."
                                                                    f"\n[ci]{msg[1]} ⚔ {msg[2]}"
                                                                    f'\n[ci]May the best win!')
            break
        except:
            print(f"Error... Retrying in 5 seconds.")
            time.sleep(5)
    win1 = 0
    win2 = 0
    round = 0
    for tpvp in range(0, rounds):
        round = round + 1
        punch = randint(0, 1)
        if punch == 0:
            win1 = win1 + 1
            agress = msg[1]
            defens = msg[2]
        else:
            win2 = win2 + 1
            agress = msg[2]
            defens = msg[1]
        time.sleep(4)
        while True:
            try:
                data.subClient.send_message(chatId=data.chatId, message=f"[cu]Round {round}"
                                                                        f"\n[ci]{msg[1]} ⚔ {msg[2]}"
                                                                        f"\n[ic] {agress} destroyed {defens}!")
                break
            except:
                print(f"Error... Retrying in 5 seconds")
                time.sleep(5)
    while True:
        try:
            if win1 > win2:
                data.subClient.send_message(chatId=data.chatId, message=f"[bcu]{msg[1]} has won!"
                                                                        f"\n[ciu][{win1} x {win2}]")
            elif win1 < win2:
                data.subClient.send_message(chatId=data.chatId, message=f"[bcu]{msg[2]} has won!"
                                                                        f"\n[cic][{win1}x{win2}]")
            elif win1 == win2:
                data.subClient.send_message(chatId=data.chatId, message=f"[iC]Tie.")
            break
        except:
            print(f"Error... Retrying in 5 seconds.")
            time.sleep(5)

@client.command(condition=is_it_me)
def leaveamino(args):
    args.subClient.send_message(args.chatId, "Leaving the amino!")
    args.subClient.stop_instance()
    args.subClient.leave_amino()

@client.command("title")
def title(args):
    if client.check(args, 'staff', id_=client.botId):
        try:
            title, color = args.message.split("color=")
            color = color if color.startswith("#") else f'#{color}'
        except Exception:
            title = args.message
            color = None

        if args.subClient.add_title(args.authorId, title, color):
            args.subClient.send_message(args.chatId, f"The titles of {args.author} has changed")

@client.command(condition=is_staff)
def post(data,):
    data.subClient.post_blog(title="I am Kunal",content="This is just a random post maybe for coins")
    data.subClient.send_message(chatId=data.chatId, message="Made post")

@client.command(condition=is_staff)
def bgicon(data):
	info = data.subClient.get_message_info(chatId = data.chatId, messageId = data.messageId)
	reply_message = info.json['extensions']
	if reply_message:
		image = info.json['extensions']['replyMessage']['mediaValue']
		filename = image.split("/")[-1]
		filetype = image.split(".")[-1]
		urllib.request.urlretrieve(image, filename)
		with open(filename, 'rb') as fp:
			im=[fp]
			for i in range(1,5):
				try:
					data.subClient.edit_profile(imageList=im)
				except Exception:
				    pass
	data.subClient.send_message(data.chatId, message="Profile bg pic changed")
	os.remove(filename)

@client.command(condition=is_staff)
def bgcolor(data):
	data.subClient.edit_profile(backgroundColor=data.message)
	data.subClient.send_message(chatId=data.chatId,message=f"Profile bg color changed")

@client.command(condition=is_staff)
def icon(data):
	info = data.subClient.get_message_info(chatId = data.chatId, messageId = data.messageId)
	reply_message = info.json['extensions']
	if reply_message:
		image = info.json['extensions']['replyMessage']['mediaValue']
		filename = image.split("/")[-1]
		ftype = image.split(".")[-1]
		if ftype=="gif":
		    filetype="gif"
		else:
		    filetype="image"
		urllib.request.urlretrieve(image, filename)
		with open(filename, 'rb') as fp:
			for i in range(1,5):
				try:
					data.subClient.edit_profile(icon=fp, fileType=filetype)
				except Exception:
				    pass
	data.subClient.send_message(data.chatId, message="Profile pic changed")
	os.remove(filename)

@client.command("ship")
def ship(data):
    couple = data.message + " null null "
    people = couple.split(" ")
    percentage = uniform(0, 100)
    quote = ' '
    if percentage <= 10:
        quote = 'No way.'
    elif 10 <= percentage <= 25:
        quote = 'Eh...'
    elif 25 <= percentage <= 50:
        quote = 'Maybe one day?'
    elif 50 <= percentage <= 75:
        quote = 'My couple ❤'
    elif 75 <= percentage <= 100:
        quote = 'Top couple'
    data.subClient.send_message(chatId=data.chatId, message=f"{people[0]} x {people[1]} has {percentage:.2f}% "
                                                            f"of chance to work.")
    data.subClient.send_message(chatId=data.chatId, message=quote)
    value = int(''.join(open("value", 'r').readlines()))
    value = value + 1
    print(value)

@client.command(condition=is_staff)
def prefix(args):
    if args.message:
        args.subClient.set_prefix(args.message)
        args.subClient.send_message(args.chatId, f"prefix set as {args.message}")

db = clie["lvl"]
levels={"1":4, "2":5, "3":10, "4":24, "5":50, "6":100, "7":200, "8":500, "9":1000, "10":2000, "11":3000, "12":5000, "13":7000, "14":10000, "15":20000, "16":40000, "17":60000, "18":100000, "19":250000,"20":500000}

def convert(im):
    with io.BytesIO() as f:
        im.save(f, format='PNG')
        return f.getvalue()

def update(com,user,level):
    put_level = db[com]
    old=put_level.find_one({com:user})
    lev=old["level"]
    lol={com:user,"level":lev}
    newvalues = { "$set": {com:user,"level":level}}
    put_level.update_one(lol, newvalues)

def zipurl(url):
	resp = urllib.request.urlopen(url)
	zipf = ZipFile(io.BytesIO(resp.read()))
	inflist = zipf.infolist()
	for f in inflist:
	    if "frame" in str(f):
		    ifile = zipf.open(f)
		    img = Image.open(ifile)
		    return img

def calPercent(x, y, integer = False):
   percent = x / y * 100
   
   if integer:
       return int(percent)
   return percent

def dec(text):
    return unicodedata.normalize('NFKD',text)
def ff(name,size):
	return ImageFont.truetype(name,size)
def circle(av):
    circle_image = Image.new('L', (av,av))
    circle_draw = ImageDraw.Draw(circle_image)
    circle_draw.ellipse((0, 0,av,av), fill=255)
    return circle_image

@client.command()
def rank(data):
    level = data.level
    level_colors = {
        1: "#46E6C2",
        2: "#46E6C2",
        3: "#46E6C2",
        4: "#46E6C2",
        5: "#54D206",
        6: "#FFD657",
        7: "#FFD657",
        8: "#FFD657",
        9: "#FFD657",
        10: "#C4DBFA",
        11: "#A339E7",
        12: "#A339E7",
        13: "#A339E7",
        14: "#A339E7",
        15: "#3FA002",
        16: "#28A4FF",
        17: "#28A4FF",
        18: "#28A4FF",
        19: "#28A4FF",
        20: "#E61338",
    }
    color = level_colors.get(level, "#000000")
    final = levels[str(level + 1)]
    rep = int(data.reputation)
    x = rep - int(levels[str(level)])
    y = int(levels[str(level + 1)]) - int(levels[str(level)])
    percentage = calPercent(x, y)
    profile1 = Image.open("backgrounds/bt.png")
    background = Editor(profile1)
    profile = load_image(str(data.authorIcon))
    profile = Editor(profile).resize((190, 190)).circle_image()
    poppins = ImageFont.truetype("fonts/calibril.ttf", 50)
    poppins_small = Font(path="fonts/calibril.ttf").poppins(size=30)
    square = Canvas((500, 500), "#06FFBF")
    square = Editor(square)
    square.rotate(30, expand=True)
    background.paste(square.image, (600, -250))
    background.paste(profile.image, (26, 47))
    try:
        url = data.json["author"]["avatarFrame"]["resourceUrl"]
        img1 = zipurl(url)
        if img1 is not None:
            av2 = Editor(img1).resize((223, 223)).circle_image()
            background.paste(av2, (11, 32))
    except:
        pass
    background.rectangle((210, 220), width=575, height=40, fill="white", radius=20)
    background.bar(
        (210, 220),
        max_width=575,
        height=40,
        percentage=percentage,
        fill=color,
        radius=20,
    )
    status = data.json["author"]["accountMembershipStatus"]
    plus = Editor("on.png" if status == 1 else "off.png").resize((40, 40))
    background.paste(plus, (240, 115))
    sus = f"lvl/{level}.png"
    ll = Editor(sus).resize((70, 70))
    background.text((287, 115), str(dec(data.author)), font=poppins, color="white")
    background.paste(ll, (699, 23))
    background.rectangle((280, 160), width=480, height=2, fill=color)
    background.text(
            (236, 187),
            f"Level :{level}",
            font=poppins_small,
            color="white",
    )
    background.text(
            (498, 185),
            f" Reputation :{rep}",
            font=poppins_small,
            color="white",
    )
    data.subClient.send_message(message=f"{data.author}",chatId=data.chatId,linkSnippetImage=background.image_bytes,linkSnippet=f"ndc://user-profile/{data.authorId}")

def cranks(data):
        user=str(data.authorId)
        com=str(data.comId)
        put_level = db[com]
        check=put_level.find_one({com:user})
        if check ==None: put_level.insert_one({com:user,"level":data.level})
        else:
            lvl=check["level"]
            if lvl < data.level:
                level=data.level
                if level==1:
                    color="#46E6C2"
                elif level==2:
                    color="#46E6C2"
                elif level==3:
                    color="#46E6C2"
                elif level==4:
                    color="#46E6C2"
                elif level==5:
                    color="#54D206"
                elif level==6:
                    color="#FFD657"
                elif level==7:
                    color="#FFD657"
                elif level==8:
                    color="#FFD657"
                elif level==9:
                    color="#FFD657"
                elif level==10:
                    color="#C4DBFA"
                elif level==11:
                    color="#A339E7"
                elif level==12:
                    color="#A339E7"
                elif level==13:
                    color="#A339E7"
                elif level==14:
                    color="#A339E7"
                elif level==15:
                    color="#3FA002"
                elif level==16:
                    color="#28A4FF"
                elif level==17:
                    color="#28A4FF"
                elif level==18:
                    color="#28A4FF"
                elif level==19:
                    color="#28A4FF"
                elif level==20:
                    color="#E61338"
                background = Editor("backgrounds/bt.png")
                profile=load_image(data.authorIcon)
                profile = Editor(profile).resize((200, 200)).circle_image()
                square = Canvas((500, 500), "#06FFBF")
                square = Editor(square)
                square.rotate(30, expand=True)
                sus=str(f"lvl/{level}.png")
                ll = Editor(sus).resize((70,70))
                background.paste(ll,(455,220))
                background.paste(square.image,(600, -250))
                background.paste(profile.image, (37,50))
                status=data.json["author"]["accountMembershipStatus"]
                if status == 1:
                    plus = Editor("on.png").resize((40,40))
                    background.paste(plus,(294,30))
                else:
                    plus = Editor("off.png").resize((40,40))
                    background.paste(plus,(294,30))
                try:
                    img1=zipurl(data.json["author"]["avatarFrame"]["resourceUrl"])
                    if img1 !=None:
                        av2 = Editor(img1).resize((250, 250)).circle_image()
                        background.paste(av2, (12,25))
                except: pass

                background.text((294,90), "Congratulations", font=ff("fonts/ss.ttf",60), color=color)
                background.text((301,162),f"You just reached level {level}", font=ff("fonts/ss.ttf",44), color=color)
                background.text((345,35),str(dec(data.author)), font=ff("fonts/calibril.ttf",50), color="#FFFFFF")
                data.subClient.send_message(message=f"{data.author}",chatId=data.chatId,linkSnippetImage=background.image_bytes,linkSnippet=f"ndc://user-profile/{data.authorId}")
                update(com,user,level)

@client.command()
def rainbow(data):
    url = f"https://some-random-api.ml/canvas/gay/?avatar={data.info.message.author.icon}"
    filename = url.split("/")[-1]
    filetype = url.split(".")[-1]
    urllib.request.urlretrieve(url, filename)
    im = Image.open(filename)
    rgb_im = im.convert('RGB')
    rgb_im.save(filename)
    Image.open(filename).resize((800, 800)).save(filename)
    img = Image.open(filename).convert("RGB")
    img.save("output.png", "png")
    snippetImage = "output.png"
    with open(snippetImage, "rb") as f:
        data.subClient.send_message(chatId=data.chatId, linkSnippetImage=f, linkSnippet=f"ndc://user-profile/{data.authorId}", message="Rainbow overley")
        os.remove(filename)
        os.remove('output.png')

@client.command("follow")
def follow(args):
    args.subClient.follow_user(args.authorId)
    args.subClient.send_message(args.chatId, "Now following you!")

@client.command("unfollow")
def unfollow(args):
    args.subClient.unfollow_user(args.authorId)
    args.subClient.send_message(args.chatId, "Unfollow!")

@client.command(condition=is_it_me)
def stopamino(args):
    args.subClient.stop_instance()
    del client[args.subClient.community_id]

def coo(data):
    info = data.subClient.get_chat_thread(data.chatId).json
    cohosts = info['extensions']['coHost']
    host = info["uid"]
    if data.authorId in cohosts or data.authorId == host or data.authorId == '4bdde85c-7d9b-4258-8473-84af3186a7f9':
        return True

def play_music(comid: str, chatid: str):
    comid = str(comid)
    data = '{"o":{"ndcId":'+comid+',"threadId":"'+chatid+'","joinRole":1,"id":"2249844"},"t":112}'
    client.send(data)

    data = '{"o":{"ndcId":'+comid+',"threadId":"'+chatid+'","channelType":1,"id":"2250161"},"t":108}'
    client.send(data)

    sleep(3)
    data = '{"o":{"ndcId":'+comid+',"threadId":'+chatid+',"id":"337496"},"t":200}'
    client.send(data)

    global is_playing
    is_playing = True
    while is_playing:
        try:
            data = '{"o":{"ndcId":'+comid+',"threadId":"'+chatid+'","joinRole":1,"id":"2249844"},"t":112}'
            client.send(data)
            sleep(2)
        except Exception:
            pass

urls = ["https://Voicebot.vedtwo2six6.repl.co", "https://Voicebot-2.vedtwo2six6.repl.co", "https://Voicebot-3.vedtwo2six6.repl.co", "https://Voicebot-4.vedtwo2six6.repl.co", "https://Voicebot-5.vedtwo2six6.repl.co", "https://Voicebot-6.vedtwo2six6.repl.co", "https://Voicebot-7.vedtwo2six6.repl.co", "https://Voicebot-8.vedtwo2six6.repl.co", "https://Voicebot-9.vedtwo2six6.repl.co", "https://Voicebot-10.vedtwo2six6.repl.co"]
last_used_urls = {}
last_used_urls_lock = Lock()

@client.command()
def music(data):
    if coo(data):
        play_music(data.comId, data.chatId)
    else:
        data.subClient.send_message(chatId=data.chatId, message="You are not co-host", replyTo=data.messageId)

@client.event("on_fetch_channel")
def on_tee(data):
    t = data.json
    chat_id = t["threadId"]
    send_joinn(data.json, chat_id)

@client.command()
def end(data):
    if coo(data):
        global is_playing
        is_playing = False
        chatId = str(data.chatId)
        client.end_voice_room(data.comId, data.chatId)
        data.subClient.send_message(chatId=data.chatId, message="Ended Music!")
        type_request_url = last_used_urls.pop(chatId)
        if type_request_url:
            leave = "leave"
            send_type(leave, type_request_url)
    else:
        data.subClient.send_message(chatId=data.chatId, message="You are not co-host", replyTo=data.messageId)

def send_joinn(token, chat_id):
    dat = {"data": json.dumps(token)}
    with last_used_urls_lock:
        last_used_url = last_used_urls.get(chat_id)
        if last_used_url is None:
            last_used_url = random.choice(urls)
        if chat_id not in last_used_urls:
            available_urls = [url for url in urls if url != last_used_url]
            last_used_url = random.choice(available_urls)
            print(f'Sending request to {last_used_url}')
        last_used_urls[chat_id] = last_used_url
    requests.post(last_used_url + "/join", data=dat)

@client.command()
def pause(data):
    if coo(data):
        type_request_url = last_used_urls.get(data.chatId)
        if type_request_url:
            pause = "pause"
            send_type(pause, type_request_url)
        data.subClient.send_message(chatId=data.chatId,message="Music paused")
    else:
        data.subClient.send_message(chatId=data.chatId, message="You are not co-host", replyTo=data.messageId)

@client.command()
def resume(data):
    if coo(data):
        type_request_url = last_used_urls.get(data.chatId)
        if type_request_url:
            resume = "resume"
            send_type(resume, type_request_url)
        data.subClient.send_message(chatId=data.chatId,message="Music resumed")
    else:
        data.subClient.send_message(chatId=data.chatId, message="You are not co-host", replyTo=data.messageId)

@client.command()
def mute(data):
    if coo(data):
        type_request_url = last_used_urls.get(data.chatId)
        if type_request_url:
            mute = "mute"
            send_type(mute, type_request_url)
        data.subClient.send_message(chatId=data.chatId,message="Music muted")
    else:
        data.subClient.send_message(chatId=data.chatId, message="You are not co-host", replyTo=data.messageId)

@client.command()
def unmute(data):
    if coo(data):
        type_request_url = last_used_urls.get(data.chatId)
        if type_request_url:
            unmute = "unmute"
            send_type(unmute, type_request_url)
        data.subClient.send_message(chatId=data.chatId,message="Music unmuted")
    else:
        data.subClient.send_message(chatId=data.chatId, message="You are not co-host", replyTo=data.messageId)

def send_type(types, url):
    requests.post(f"{url}/type", data={"type": types})

@client.command()
def volume(data):
    if coo(data):
        vol = int(data.message)
        if not 1 <= vol <= 10:
            data.subClient.send_message(chatId=data.chatId, message="Volume level should be between 1 and 10.")
        lvl = vol * 10
        volume_icons = [
            "🔊 ─⚪─────────",
            "🔊 ──⚪────────",
            "🔊 ───⚪───────",
            "🔊 ────⚪──────",
            "🔊 ─────⚪─────",
            "🔊 ──────⚪────",
            "🔊 ───────⚪───",
            "🔊 ────────⚪──",
            "🔊 ─────────⚪─",
            "🔊 ──────────⚪",
        ]
        message = f"Volume {volume_icons[vol - 1]} {vol}"
        type_request_url = last_used_urls.get(data.chatId)
        if type_request_url:
            requests.post(type_request_url + "/volume", data={"volume": lvl})
        data.subClient.send_message(chatId=data.chatId, message=message)
    else:
        data.subClient.send_message(chatId=data.chatId, message="You are not co-host", replyTo=data.messageId)

@client.command()
def queue(data):
    if coo(data):
        url = data.message
        type_request_url = last_used_urls.get(data.chatId)
        if type_request_url:
            requests.post(type_request_url + "/queue", data={"url": url}).text
        data.subClient.send_message(chatId=data.chatId, message=res)
    else:
        data.subClient.send_message(chatId=data.chatId, message="You are not co-host", replyTo=data.messageId)

@client.command()
def playlist(data):
    if coo(data):
        type_request_url = last_used_urls.get(data.chatId)
        if type_request_url:
            res = requests.post(type_request_url + "/playlist").text
            songs = ast.literal_eval(res)
            playlist = "Playlists:\n" + "\n".join(songs)
        data.subClient.send_message(chatId=data.chatId, message=playlist)
    else:
        data.subClient.send_message(chatId=data.chatId, message="You are not co-host", replyTo=data.messageId)

@client.command()
def next(data):
    if coo(data):
        type_request_url = last_used_urls.get(data.chatId)
        if type_request_url:
            requests.post(type_request_url + "/play_next")
    else:
        data.subClient.send_message(chatId=data.chatId, message="You are not co-host", replyTo=data.messageId)

@client.command()
def previous(data):
    if coo(data):
        type_request_url = last_used_urls.get(data.chatId)
        if type_request_url:
            requests.post(type_request_url + "/play_previous")
    else:
        data.subClient.send_message(chatId=data.chatId, message="You are not co-host", replyTo=data.messageId)

@client.command()
def song(data):
    if coo(data):
        url = data.message
        type_request_url = last_used_urls.get(data.chatId)
        if type_request_url:
            res = requests.post(type_request_url + "/play", data={"url": url}).text
            message = res
        try:
            size = int(message.strip().split().pop())
            msg = " ".join(message.strip().split()[:-1])
            search = msg
        except ValueError:
            size = 1
            search = message
        if size > 5:
            size = 5
        results = YoutubeSearch(search, max_results=size).to_json()
        results = YoutubeSearch(search, max_results=size).to_dict()
        yt_reply = ""
        for result in results:
            title = result['title']
            thumbnails = result['thumbnails'][0]
            yt_url = 'https://youtu.be' + result['url_suffix']
            url = f"{thumbnails}"
            file = upload(url)
            dr = result['duration']
            views = result['views']
            yt_reply = yt_reply + str(title) + "\nVistas: " + str(views) + "\nDuracion: " + str(dr) + "\n" + str(yt_url) + "\n\n"
        with suppress(Exception):
            data.subClient.send_message(chatId=data.chatId,message=f"{title}",embedTitle="Now playing",embedImage=file, embedLink=f"{yt_url}",fileType="image")
    else:
        data.subClient.send_message(chatId=data.chatId, message="You are not co-host", replyTo=data.messageId)

def deviceaoss(identifier):
    mac = hmac.new(bytes.fromhex('AE49550458D8E7C51D566916B04888BFB8B3CA7D'), b"\x52" + identifier, hashlib.sha1)
    return (f"52{identifier.hex()}{mac.hexdigest()}").upper()

@client.command()
def deviceid(data):
     genids = deviceaoss(identifier=urandom(20))
     data.subClient.send_message(data.chatId, message=genids)

@client.command(condition=is_staff)
def wallet(data):
    coins = client.get_wallet_info().totalCoins
    data.subClient.send_message(message=f"Total coins {coins}",chatId=data.chatId)

@client.command(condition=is_staff)
def promote(data):
    if "aminoapps.com" in data.message:
    	user=(client.get_from_code(data.message.split(' ')[0]).objectId)
    	link=data.message.split(' ')[1]
    	data.subClient.promote(userId=user, rank=link)
    	data.subClient.send_message(data.chatId, message=f"{link} request sent")
    else:
        data.subClient.send_message(chatId=data.chatId, message="Check the link")

@client.command(condition=is_staff)
def lban(data):
    x = data.subClient.get_all_users(start = 0,size = 5000)
    for nickname, uid in zip(x.profile.nickname,x.profile.userId):
        if nickname == data.message:
            try:
                data.subClient.ban(userId=uid, reason="spam joining here",banType=2)
            except Exception:
                data.subClient.send_message(message=f"Banned {data.message} users",chatId=data.chatId)

@client.command(condition=is_staff)
def ban(data):
    mention = data.subClient.get_message_info(chatId=data.chatId, messageId=data.messageId).mentionUserIds
    if "aminoapps.com" in data.message:
    	uid=(client.get_from_code(data.message.split(' ')[0]).objectId)
    elif mention!=None:
    	for x in mention:
    		uid=x
    reason=None
    try:
        reason= ' '.join(data.message.split(' ')[1:])
        if len(reason.split(' '))<3:
            data.subClient.send_message(data.chatId,'Specify atleast 3 words for reason',replyTo=data.messageId)
        else:
            data.subClient.ban(uid,reason)
            name=data.subClient.get_user_info(uid).nickname
            data.subClient.send_message(data.chatId,f'Banned {name}',replyTo=data.messageId)
    except:
            data.subClient.send_message(data.chatId,'Specify reason for ban',replyTo=data.messageId)

@client.command(condition=is_staff)
def unban(data):
    uid=(client.get_from_code(data.message.split(' ')[0]).objectId)
    reason=None
    try:
        reason= ' '.join(data.message.split(' ')[1:])
        if len(reason.split(' '))<3:
            data.subClient.send_message(data.chatId,'Specify atleast 3 words for reason',replyTo=data.messageId)
        else:
            data.subClient.unban(uid,reason)
            name=data.subClient.get_user_info(uid).nickname
            data.subClient.send_message(data.chatId,f'Unbanned {name}',replyTo=data.messageId)
    except:
        data.subClient.send_message(data.chatId,'Specify reason for unban',replyTo=data.messageId)

@client.command(condition=is_staff)
def warn(data):
    mention = data.subClient.get_message_info(chatId=data.chatId, messageId=data.messageId).mentionUserIds
    if "aminoapps.com" in data.message:
    	uid=(client.get_from_code(data.message.split(' ')[0]).objectId)
    elif mention!=None:
    	for x in mention:
    		uid=x
    reason=None
    try:
        reason= ' '.join(data.message.split(' ')[1:])
        if len(reason.split(' '))<3:
            data.subClient.send_message(data.chatId,'Specify atleast 3 words for reason',replyTo=data.messageId)
        else:
            data.subClient.warn(uid,reason)
            name=data.subClient.get_user_info(uid).nickname
            data.subClient.send_message(data.chatId,f'Warned {name}',replyTo=data.messageId)
    except:
        data.subClient.send_message(data.chatId,'Specify reason for Warn',replyTo=data.messageId)

@client.command(condition=is_staff)
def feature(data):
    link=data.message.split(' ')[1]
    try:
        time=int(data.message.split(' ')[0])
        info=client.get_from_code(link.split('/')[4])
        objId=info.objectId
        objtype=info.objectType
        if objtype==0 and time in [1,2]:
            data.subClient.feature(time,userId=objId)
            data.subClient.send_message(data.chatId,f'Featured User for {time} days',replyTo=data.messageId)
        elif objtype==1 and time in [1,2,3]:
            data.subClient.feature(time,blogId=objId)
            data.subClient.send_message(data.chatId,f'Featured Blog for {time} days',replyTo=data.messageId)
        elif objtype==2 and time in [1,2,3]:
            data.subClient.feature(time,wikiId=objId)
            data.subClient.send_message(data.chatId,f'Featured Wiki for {time} days',replyTo=data.messageId)
        elif objtype==12 and time in [1,2,3]:
            data.subClient.feature(time,chatId=objId)
            data.subClient.send_message(data.chatId,f'Featured Chatroom for {time} hours',replyTo=data.messageId)
        elif objtype not in [0,1,2,12]:
            data.subClient.send_message(data.chatId,'Given link cannot be featured',replyTo=data.messageId)
        else:
            data.subClient.send_message(data.chatId,'Invalid time specified',replyTo=data.messageId)
    except:
        data.subClient.send_message(data.chatId,'Please specify time after the command. If you did specify a time already...then you tried featuring a post thats already featured.',replyTo=data.messageId)

@client.command(condition=is_staff)
def unfeature(data):
    link=data.message
    try:
        info=client.get_from_code(link.split(' ')[0])
        objId=info.objectId
        objtype=info.objectType
        if objtype==0:
            data.subClient.unfeature(userId=objId)
            data.subClient.send_message(data.chatId,f'UnFeatured User',replyTo=data.messageId)
        elif objtype==1:
            data.subClient.unfeature(blogId=objId)
            data.subClient.send_message(data.chatId,f'UnFeatured Blog',replyTo=data.messageId)
        elif objtype==2:
            data.subClient.unfeature(wikiId=objId)
            data.subClient.send_message(data.chatId,f'UnFeatured Wiki',replyTo=data.messageId)
        elif objtype==12:
            data.subClient.unfeature(chatId=objId)
            data.subClient.send_message(data.chatId,f'UnFeatured Chatroom',replyTo=data.messageId)
        elif objtype not in [0,1,2,12]:
            data.subClient.send_message(data.chatId,'Given link cannot be Unfeatured',replyTo=data.messageId)
    except:
        data.subClient.send_message(data.chatId,'You probably tried to unfeature a post that wasnt featured.',replyTo=data.messageId)

@client.command(condition=is_staff)
def strike(data):
    mention = data.subClient.get_message_info(chatId=data.chatId, messageId=data.messageId).mentionUserIds
    if "aminoapps.com" in data.message:
    	uid=(client.get_from_code(data.message.split(' ')[0]).objectId)
    elif mention!=None:
    	for x in mention:
    		uid=x
    reason=None
    try:
        time=int(values.message.split(' ')[0])
        reason= ' '.join(values.message.split(' ')[2:])
        if len(reason.split(' '))<3:
            data.subClient.send_message(values.chatId,'Specify atleast 3 words for reason',replyTo=values.messageId)
        elif time not in [1,3,6,12,24]:
            data.subClient.send_message(values.chatId,'Specify Valid hours for strike',replyTo=values.messageId)
        else:
            tdict={1:1,3:2,6:3,12:4,24:5}
            timd=tdict[time]
            values.subClient.strike(uid,timd,'Custom',reason)
            name=values.subClient.get_user_info(uid).nickname
            data.subClient.send_message(values.chatId,f'Striked {name} for {time} hours',replyTo=values.messageId)
    except:
        data.subClient.send_message(values.chatId,'Specify reason and time for Strike',replyTo=values.messageId)

@client.command(condition=is_staff)
def name(data):
	data.subClient.edit_profile(nickname=data.message)
	data.subClient.send_message(chatId=data.chatId,message=f"name changed to {data.message}")

@client.command(condition=is_staff)
def bio(data):
	data.subClient.edit_profile(content=data.message)
	data.subClient.send_message(chatId=data.chatId,message=f"Bio changed")

@client.command(condition=is_staff)
def giveco(data):
    mention = data.subClient.get_message_info(chatId=data.chatId, messageId=data.messageId).mentionUserIds
    if "@" in data.message:
    	for x in mention:
    		user=x
    else:
    	user=data.authorId
    with suppress(Exception):
        data.subClient.edit_chat(chatId=data.chatId,coHosts=[user])

@client.command(condition=is_staff)
def vm(data):
    id = data.subClient.get_chat_threads(start=0, size=40).chatId
    for chat in id:
        with suppress(Exception):
            data.subClient.edit_chat(chatId=chat, viewOnly=True)

@client.command(condition=is_staff)
def unvm(data):
    id = data.subClient.get_chat_threads(start=0, size=40).chatId
    for chat in id:
        with suppress(Exception):
            data.subClient.edit_chat(chatId=chat, viewOnly=False)

def telecharger(url):
    music = None
    if ("=" in url and "/" in url and " " not in url) or ("/" in url and " " not in url):
        if "=" in url and "/" in url:
            music = url.rsplit("=", 1)[-1]
        elif "/" in url:
            music = url.rsplit("/")[-1]

        if music in os.listdir(path_download):
            return music

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
                }],
            'extract-audio': True,
            'outtmpl': f"{path_download}/{music}",
            }

        with YoutubeDL(ydl_opts) as ydl:
            video_length = ydl.extract_info(url, download=True).get('duration')
            ydl.cache.remove()

        music = music+".mp3"

        return music, video_length
    return url, False


def search_internet_music(music_name):
    query_string = urllib.parse.urlencode({"search_query": music_name})
    formatUrl = urllib.request.urlopen("https://www.youtube.com/results?" + query_string)

    search_results = re.findall(r"watch\?v=(\S{11})", formatUrl.read().decode())
    clip2 = "https://www.youtube.com/watch?v=" + "{}".format(search_results[0])
    return telecharger(clip2)


def decoupe(musical, temps):
    size = 180
    with open(musical, "rb") as fichier:
        nombre_ligne = len(fichier.readlines())

    if temps < 181 or temps > 540:
        return False

    decoupage = int(size*nombre_ligne / temps)

    t = 0
    file_list = []
    for a in range(0, nombre_ligne, decoupage):
        b = a + decoupage
        if b >= nombre_ligne:
            b = nombre_ligne

        with open(musical, "rb") as fichier:
            lignes = fichier.readlines()[a:b]

        with open(musical.replace(".mp3", "PART"+str(t)+".mp3"),  "wb") as mus:
            for ligne in lignes:
                mus.write(ligne)

        file_list.append(musical.replace(".mp3", "PART"+str(t)+".mp3"))
        t += 1
    return file_list


@client.command()
def play(args):
    music, size = telecharger(args.message)

    if not size:
        music, size = search_internet_music(music)

    if size:
        music = f"{path_download}/{music}"
        val = decoupe(music, size)

        if not val:
            try:
                with open(music, 'rb') as fp:
                    args.subClient.send_message(args.chatId, file=fp, fileType="audio")
            except Exception:
                args.subClient.send_message(args.chatId, "Error! File too heavy (5 min max)")
            os.remove(music)
            return

        os.remove(music)
        for elem in val:
            try:
                with open(elem, 'rb') as fp:
                    args.subClient.send_message(args.chatId, file=fp, fileType="audio")
            except Exception as e:
                print(type(e), e)

            os.remove(elem)

        return
    args.subClient.send_message(args.chatId, "Error! Wrong link")

@client.command(condition=is_staff)
def join(args):
    val = args.subClient.join_chatroom(args.message, args.chatId)
    if val or val == "":
        args.subClient.send_message(args.chatId, f"Chat {val} joined".strip())
    else:
        args.subClient.send_message(args.chatId, "No chat joined")
        
@client.command(condition=is_staff)
def leave(args):
    if args.message:
        chat_ide = args.subClient.get_chat_id(args.message)
        if chat_ide:
            args.chatId = chat_ide
    args.subClient.leave_chat(args.chatId)

@client.command("block", False)
def block(args):
    val = args.subClient.get_user_id(args.message)
    if val:
        args.subClient.client.block(val[1])
        args.subClient.send_message(args.chatId, f"User {val[0]} blocked!")

@client.command("unblock", False)
def unblock(args):
    val = args.subClient.client.get_blocked_users()
    for aminoId, userId in zip(val.aminoId, val.userId):
        if args.message in aminoId:
            args.subClient.client.unblock(userId)
            args.subClient.send_message(args.chatId, f"User {aminoId} unblocked!")

@client.command(condition=is_staff)
def takehost(data):
	if "aminoapps.com" in data.message:
	    ids=(client.get_from_code(data.message.split(' ')[0]).objectId)
	else:
	    ids=data.chatId
	data.subClient.transfer_host(chatId=ids,userIds=[client.userId])
	info=data.subClient.get_chat_thread(ids)
	x=info.json['extensions']['organizerTransferRequest']['requestId']
	data.subClient.accept_organizer(chatId=ids,requestId=x)
	data.subClient.send_message(data.chatId,message="Accepted Host")

@client.command(condition=is_staff)
def givehost(data):
    mention = data.subClient.get_message_info(chatId=data.chatId, messageId=data.messageId).mentionUserIds
    if "aminoapps.com" in data.message:
    	user=(client.get_from_code(data.message.split(' ')[0]).objectId)
    elif mention!=None:
    	for x in mention:
    		user=x
    else:
    	user=data.authorId
    data.subClient.transfer_host(data.chatId,userIds=[user])
    data.subClient.send_message(data.chatId,message="Host request send")

@client.command()
def accept(args):
    if args.subClient.accept_role(args.chatId):
        args.subClient.send_message(args.chatId, "Accepted!")
        return
    val = args.subClient.get_notices(start=0, size=25)
    for elem in val:
        print(elem["title"])

    res = None

    for elem in val:
        if 'become' in elem['title'] or "host" in elem['title']:
            res = elem['noticeId']

        if res and args.subClient.accept_role(res):
            args.subClient.send_message(args.chatId, "Accepted!")
            return
    else:
        args.subClient.send_message(args.chatId, "Error!")

@client.command(condition=is_staff)
def announce(args):
    #if client.check(args,'staff'):
    	try:
    		val = args.subClient.get_chat_threads(start=0,size=100).chatId
    		print(val)
    		for g in val:
            			args.subClient.send_message(chatId=g,message=f"""

{args.message}""")

    	except Exception:
    		  	args.subClient.send_message(args.chatId,message=f"""
Finished Announcement
""")

@client.command(condition=is_it_me)
def ask(args):
    lvl = ""
    boolean = 1
    if "lvl=" in args.message:
        lvl = args.message.rsplit("lvl=", 1)[1].strip().split(" ", 1)[0]
        args.message = args.message.replace("lvl="+lvl, "").strip()
    elif "lvl<" in args.message:
        lvl = args.message.rsplit("lvl<", 1)[1].strip().split(" ", 1)[0]
        args.message = args.message.replace("lvl<"+lvl, "").strip()
        boolean = 2
    elif "lvl>" in args.message:
        lvl = args.message.rsplit("lvl>", 1)[1].strip().split(" ", 1)[0]
        args.message = args.message.replace("lvl>"+lvl, "").strip()
        boolean = 3
    try:
        lvl = int(lvl)
    except ValueError:
        lvl = 20

    args.subClient.ask_all_members(args.message+f"\n[CUI]This message was sent by {args.author}\n[CUI]I am a bot and have a nice day^^", lvl, boolean)
    args.subClient.send_message(args.chatId, "Asking...")

@client.command("askstaff", False)
def ask_staff(args):
    amino_list = client.client.sub_clients()
    for commu in amino_list.comId:
        client[commu].ask_amino_staff(message=args.message)
    args.subClient.send_message(args.chatId, "Asking...")

@client.command("lock", is_staff)
def lock_command(args):
    if not args.message or args.message in args.subClient.locked_command or args.message not in client.commands_list() or args.message in ("lock", "unlock"):
        return
    try:
        args.message = args.message.lower().strip().split()
    except Exception:
        args.message = [args.message.lower().strip()]
    args.subClient.add_locked_command(args.message)
    args.subClient.send_message(args.chatId, "Locked command list updated")

@client.command("unlock", is_staff)
def unlock_command(args):
    if args.message:
        try:
            args.message = args.message.lower().strip().split()
        except Exception:
            args.message = [args.message.lower().strip()]
        args.subClient.remove_locked_command(args.message)
        args.subClient.send_message(args.chatId, "Locked command list updated")

@client.command("llock")
def locked_command_list(args):
    val = ""
    if args.subClient.locked_command:
        for elem in args.subClient.locked_command:
            val += elem+"\n"
    else:
        val = "No locked command"
    args.subClient.send_message(args.chatId, val)

@client.command("alock")
def admin_lock_command(args):
    if client.check(args, 'me', 'admin'):
        if not args.message or args.message not in client.get_commands_names() or args.message == "alock":
            return

        command = args.subClient.admin_locked_command
        args.message = [args.message]

        if args.message[0] in command:
            args.subClient.remove_admin_locked_command(args.message)
        else:
            args.subClient.add_admin_locked_command(args.message)

        args.subClient.send_message(args.chatId, "Locked command list updated")

@client.command("allock")
def locked_admin_command_list(args):
    if client.check(args, 'me', 'admin'):
        val = ""
        if args.subClient.admin_locked_command:
            for elem in args.subClient.admin_locked_command:
                val += elem+"\n"
        else:
            val = "No locked command"
        args.subClient.send_message(args.chatId, val)

@client.command("mention")
def mention(args):
    try:
        size = int(args.message.strip().split().pop())
        args.message = " ".join(args.message.strip().split()[:-1])
    except ValueError:
        size = 1

    val = args.subClient.get_user_id(args.message)
    if not val:
        args.subClient.send_message(chatId=args.chatId, message="Username not found")
        return

    if size > 5:
        size = 5

    if val:
        for _ in range(size):
            with suppress(Exception):
                args.subClient.send_message(chatId=args.chatId, message=f"‎‏‎‏@{val[0]}‬‭", mentionUserIds=[val[1]])
                
@client.command(condition=is_staff)
def msg(args):
    value = 0
    size = 1
    ment = None
    with suppress(Exception):
        args.subClient.delete_message(args.chatId, args.messageId, asStaff=True, reason="Clear")

    if "chat=" in args.message:
        chat_name = args.message.rsplit("chat=", 1).pop()
        chat_ide = args.subClient.get_chat_id(chat_name)
        if chat_ide:
            args.chatId = chat_ide
        args.message = " ".join(args.message.strip().split()[:-1])

    try:
        size = int(args.message.split().pop())
        args.message = " ".join(args.message.strip().split()[:-1])
    except ValueError:
        size = 0

    try:
        value = int(args.message.split().pop())
        args.message = " ".join(args.message.strip().split()[:-1])
    except ValueError:
        value = size
        size = 1

    if not args.message and value == 1:
        args.message = f"‎‏‎‏@{args.author}‬‭"
        ment = args.authorId

    if size > 10:
        size = 10

    for _ in range(size):
        with suppress(Exception):
            args.subClient.send_message(chatId=args.chatId, message=f"{args.message}", messageType=value, mentionUserIds=ment)

@client.command()
def check(args):
	args.subClient.send_message(args.chatId, f"--Bot is Online--")

@client.command()
def ghost(data):
	rol=data.subClient.get_user_info(userId=client.userId).json["role"]
	if (rol==100,rol==101):
		data.subClient.delete_message(chatId=data.chatId,messageId=data.messageId,asStaff=True,reason="Clear")
		data.subClient.send_message(data.chatId,data.message,messageType=114)

@client.command()
def gspam(args):
    try:
      args.subClient.delete_message(args.chatId, args.messageId, asStaff=True)
    except:
      args.subClient.delete_message(args.chatId, args.messageId)
    qte = args.message.rsplit(" ", 1)
    msg, quantity= qte[0], qte[1]
    quantity = 1 if not quantity.isdigit() else int(quantity)
    quantity = 100 if quantity > 100 else quantity

    for _ in range(quantity):
        args.subClient.send_message(args.chatId, msg, messageType=114)

@client.command("mentionco")
def mentionco(data):
    hostlist = data.subClient.get_chat_thread(data.chatId).coHosts
    msg = 'Co-Hosts:\n'
    for item in hostlist:
        n = data.subClient.get_user_info(str(item)).nickname
        msg += f'<$@{n}$>\n'
    data.subClient.send_message(chatId=data.chatId, message=msg, mentionUserIds=hostlist)
                        
@client.command()
def joke(data):
    link = f"https://some-random-api.ml/joke"
    response = requests.get(link)
    json_data = json.loads(response.text)
    msg = json_data['joke']
    data.subClient.send_message(chatId=data.chatId, message=f"{msg}")
    
@client.command("8ball")
def height_ball(data):
    ball= choice(["Yes", "No", "Maybe", "of course", "never", "i think so"])
    data.subClient.send_message(data.chatId, ball, replyTo = data.messageId)

@client.command("say")
def say_something(data):
    audio_bytes = BytesIO()
    gTTS(text=data.message, lang='hi', slow=False).write_to_fp(audio_bytes)
    audio_bytes.seek(0)
    data.subClient.send_message(data.chatId, file=audio_bytes, fileType="audio")

@client.command()
def prank(args, amt : int , nt = 1):
    with suppress(Exception):
        args.subClient.delete_message(args.chatId, args.messageId, asStaff=True)

    tId = "3c6308c5-e5ec-4d60-b7d6-1730382c6703"
    if args.message:
    	chat_ide = args.subClient.get_chat_id(args.message)
    	if chat_ide:
    		args.chatId = chat_ide
    	amt , nt = int(amt) , int(nt)
    	for _ in range(nt):
    		args.subClient.send_coins(coins=amt, chatId=args.chatId, transactionId=tId)

@client.command()
def bg(data):
    image = data.subClient.get_chat_thread(chatId=data.chatId).backgroundImage
    if image:
        profile =load_image(str(image))
        background = Editor(profile)
        data.subClient.send_message(data.chatId, file=background.image_bytes, fileType="image")

@client.command()
def bgi(data):
    image = data.subClient.get_chat_thread(chatId=data.chatId).icon
    if image:
        profile =load_image(str(image))
        background = Editor(profile)
        data.subClient.send_message(data.chatId, file=background.image_bytes, fileType="image")

@client.command()
def joinvc(data):
	client.join_voice_chat(comId=data.subClient.community_id,chatId=data.chatId,joinType=1)

@client.command()
def joinsc(data):
	client.join_screen_room(comId=data.subClient.community_id,chatId=data.chatId,joinType=1)

@client.command()
def summon(data):
    with open("sid.txt") as f:
        lines = [line.strip() for line in f.readlines()]
    payload = {"list": lines, "comId": data.comId, "chatId": data.chatId}
    param = {"data": json.dumps(payload)}
    requests.post("https://summon.vedtwo2six6.repl.co/vc", data=param)

@client.command()
def jsummon(data):
    with open('sid.txt') as f:
        lines = [line.strip() for line in f.readlines()]
    users = [sid_to_uid(sid) for sid in lines]
    for user in users:
        data.subClient.invite_to_chat(chatId=data.chatId,userId=user)

@client.command(condition=is_it_me)
def sidex(data):
    data.subClient.send_message(data.chatId,"extracting sids")
    file_path = "sid.txt"
    with open(file_path, 'w') as f:
        f.truncate(0)
    sid_e()
    data.subClient.send_message(data.chatId,"sid_extracted")

@client.command()
def spam(args):
    try:
      args.subClient.delete_message(args.chatId, args.messageId, asStaff=True)
    except:
      args.subClient.delete_message(args.chatId, args.messageId)
    qte = args.message.rsplit(" ", 1)
    msg, quantity= qte[0], qte[1]
    quantity = 1 if not quantity.isdigit() else int(quantity)
    quantity = 100 if quantity > 100 else quantity

    for _ in range(quantity):
        args.subClient.send_message(args.chatId, msg)
        
@client.command(condition=is_staff)
def clear(args):
    #if client.check(args, 'staff', client.botId):
        try:
            size = int(args.message)
        except Exception:
            size = 1
        args.subClient.delete_message(args.chatId, args.messageId, asStaff=True, reason="Clear")

        if size > 99:
            size = 99

        messages = args.subClient.get_chat_messages(chatId=args.chatId, size=size).messageId

        for message in messages:
            args.subClient.delete_message(args.chatId, messageId=message, asStaff=True, reason="Clear")

@client.command("all")
def everyone(args):
    try:
      args.subClient.delete_message(args.chatId, args.messageId, asStaff=True)
    except:
      args.subClient.delete_message(args.chatId, args.messageId)
    mention = [userId for userId in args.subClient.get_chat_users(chatId=args.chatId).userId]
    # test = "".join(["‎‏‎‏‬‭" for user in args.subClient.get_chat_users(chatId=args.chatId).userId])
    args.subClient.send_message(chatId=args.chatId, message=f"[iu]@everyone‎‏‎‏‬‭‎‏‎‏‬‭ {args.message}", mentionUserIds=mention)

@client.command()
def lurk(data):
    members = data.subClient.get_chat_lurkers()['userInfoInThread'][data.chatId]
    names = [name['nickname'] for name in members['userProfileList']]
    count = members['userProfileCount']
    mes= f'[bc]Lurkers : {count}\n\n'
    for i in names:
        mes += f'• {i}\n'
    data.subClient.send_message(data.chatId,mes)

@client.command()
def tr(args):
  data = args.subClient.get_message_info(chatId = args.chatId, messageId = args.messageId)
  reply_message = data.json['extensions']
  if reply_message:
    reply_message = data.json['extensions']['replyMessage']['content']
    reply_messageId = data.json['extensions']['replyMessage']['messageId']
    translator = google_translator() 
    # detect_result = translator.detect(reply_message)[1]
    translate_text = translator.translate(reply_message)
    reply = "[IC]"+str(translate_text)
    print(reply)
    args.subClient.send_message(chatId=data.chatId,message=reply,replyTo=reply_messageId)

@client.command()
def gif(args):
  search = (args.message)
  with suppress(Exception):
    try:
      args.subClient.delete_message(args.chatId, args.messageId, asStaff=True)
    except:
      args.subClient.delete_message(args.chatId, args.messageId)
  response = requests.get('http://api.giphy.com/v1/gifs/search?q=' + search + '&api_key=7G8jLZHM52O5YLJ0fPcBOawMvew5a1e1')
  # print(response.text)
  data = json.loads(response.text)
  gif_choice = randint(0, 9)
  image = data['data'][gif_choice]['images']['original']['url']
  print("URL",image)
  if image is not None:
    profile =load_image(str(image))
    background = Editor(profile)
    args.subClient.send_message(args.chatId, file=background.image_bytes, fileType="gif")

@client.command("chatlist", condition=is_staff)
def get_chats(args):
    val = args.subClient.get_chats()
    for title, _ in zip(val.title, val.chatId):
        args.subClient.send_message(args.chatId, title)

afk_users = {}

def afk_message(data):
    if data.authorId in afk_users:
        user = afk_users.pop(data.authorId)
        time_away = (datetime.now() - user["time"]).seconds
        minutes_away = time_away // 60
        data.subClient.send_message(message=f"""Welcome back {user["name"]}! 
You have been away for {minutes_away} minutes and {time_away % 60} seconds
Reason {user["msg"]}""", chatId=data.chatId)

@client.command()
def afk(data):
    afk_users[data.authorId] = {"name": data.author, "time": datetime.now(), "msg": data.message}
    data.subClient.send_message(message=f'{data.author} is now AFK for {data.message}',chatId=data.chatId)

@client.command("chatid")
def chat_id(args):
    val = args.subClient.get_chats()
    for title, chat_id in zip(val.title, val.chatId):
        if args.message.lower() in title.lower():
            args.subClient.send_message(args.chatId, f"{title} | {chat_id}")

@client.command(condition=is_staff)
def joinall(args):
        args.subClient.join_all_chat()
        args.subClient.send_message(args.chatId, "All chat joined")

@client.command(condition=is_staff)
def leaveall(args):
    args.subClient.send_message(args.chatId, "Leaving all chat...")
    args.subClient.leave_all_chats()

@client.command(condition=is_staff)
def sw(args):
    data = args.subClient.get_message_info(chatId=args.chatId, messageId=args.messageId)
    reply_message = data.json['extensions']
    if reply_message:
        reply_message = data.json['extensions']['replyMessage']['content']
        args.subClient.set_welcome_message(reply_message)
    args.subClient.send_message(args.chatId, "Welcome wall message changed")

@client.command(condition=is_staff)
def unsw(args):
    val=""
    args.subClient.set_welcome_message(val)
    args.subClient.send_message(args.chatId, "wall welcome off")

@client.command()
def help(data):
    data.subClient.send_message(chatId=data.chatId, message="""[BC]BoT Menu

➼ help           ➼ fun
➼ check        ➼ modonly
➼ chat           ➼ musicmod

[CI]By Vedansh~""")

@client.command()
def fun(data):
    data.subClient.send_message(chatId=data.chatId, message="""[BC]Fun Menu
➼say 
➼prank
➼gif
➼msg
➼dice
➼cb
➼tb
➼quote
➼joke
➼play
➼truth
➼dare
➼rainbow
➼ss
➼afk
➼dictionary
➼global2
➼hug
➼pie
➼trash
➼kill
➼slap
➼ship
➼rank""")

@client.command()
def modonly(data):
    data.subClient.send_message(chatId=data.chatId, message="""[BC]Modonly Menu
➼name
➼icon
➼bgicon
➼bgcolor
➼bubble
➼frame
➼bio
➼block
➼unblock
➼ask
➼wallet
➼accept
➼leaveall
➼announce
➼gcon
➼gcoff
➼post
➼abw
➼rbw
➼spam
➼vm
➼unvm
➼ban
➼unban
➼feature
➼unfeature
➼strike
➼warn
➼lban
➼id
➼setbotlog
➼usetbotlog
➼antiraidon
➼antiraidoff
➼givetco
➼takehost
➼givehost
➼promote""")

@client.command()
def chat(data):
    data.subClient.send_message(chatId=data.chatId, message="""[BC]Chat Menu
➼startvc    ➼bgi
➼endvc      ➼restart
➼joinvc      ➼profile
➼startsc    ➼llock
➼endsc      ➼mention
➼startvid   ➼mentionco
➼joinsc      ➼deviceid
➼inviteall   ➼pvp
➼notifyall   ➼follow
➼ghost       ➼unfollow
➼tr              ➼bg
➼chatlist    ➼global
➼all             ➼joinall
➼google    ➼join
➼summon  ➼purge
➼lurk          ➼snipe
➼findid     ➼inviteglobal""")

@client.command()
def musicmod(data):
    data.subClient.send_message(chatId=data.chatId, message="""[BC]Music Menu
➼music(will start musicmode)
➼song(play song)
➼pause
➼resume
➼mute
➼unmute
➼volume
➼end""")

@client.command()
def findid(data, user_id, com_id):
    n=user_id
    link=com_id
    gg=client.get_from_code(link).comId
    id=client.get_from_code(n).objectId
    try:
        link = client.get_from_id(objectId=id, objectType=0, comId=gg).json['extensions']['linkInfo']['shareURLShortCode']
        data.subClient.send_message(chatId=data.chatId,message=f"User Found -- {link}")
    except:
        data.subClient.send_message(chatId=data.chatId,message="User not found")

@client.command()
def dictionary(data):
    link = f"https://some-random-api.ml/dictionary?word={data.message}"
    response = requests.get(link)
    json_data = json.loads(response.text)
    msg = json_data['definition']
    data.subClient.send_message(chatId=data.chatId, message=f"{msg}")

@client.command()
def hug(data):
	mention = data.subClient.get_message_info(chatId=data.chatId, messageId=data.messageId).mentionUserIds
	for user in mention:
		h=data.subClient.get_user_info(userId=str(user)).nickname
		url = f"https://some-random-api.ml/animu/hug"
		response = requests.get(url)
		json_data = json.loads(response.text)
		url = json_data['link']
		file = upload(url)
		
		data.subClient.send_message(chatId=data.chatId,file=file, fileType="gif")
		data.subClient.send_message(chatId=data.chatId, message=f"""{data.author} hugged {h} {randint(1, 20)} times""")

@client.command()
def quote(data):
    link = f"https://some-random-api.ml/animu/quote"
    response = requests.get(link)
    json_data = json.loads(response.text)
    msg = json_data['sentence']
    data.subClient.send_message(chatId=data.chatId, message=f"{msg}")
            
@client.command()
def google(data):
    msg = data.message.split(" ")
    msg = '+'.join(msg)
    while True:
        try:
            data.subClient.send_message(chatId=data.chatId, message=f"https://www.google.com/search?q={msg}")
            break
        except:
            print(f"Error... Retrying in 5 seconds.")
            time.sleep(5)
            
@client.command("global")
def globall(data):
	mention = data.subClient.get_message_info(chatId=data.chatId, messageId=data.messageId).mentionUserIds
	for user in mention:
	   AID=client.get_user_info(userId=str(user)).aminoId
	   data.subClient.send_message(data.chatId,message="https://aminoapps.com/u/"+str(AID))
	   	 	   
@client.command("global2")
def globall(data):
	   id=client.get_from_code(data.message).objectId
	   AID=client.get_user_info(id).aminoId
	   data.subClient.send_message(data.chatId,message="https://aminoapps.com/u/"+str(AID))

@client.command()
def truth(data):
    rating = 'pg'
    link = f"https://api.truthordarebot.xyz/api/truth?rating={rating}"
    response = requests.get(link)
    json_data = json.loads(response.text)
    msg = json_data['question']
    data.subClient.send_message(chatId=data.chatId, message=f"""[U]Truth for {data.author}
{msg}""")

@client.command()
def dare(data):
    rating = 'pg'
    link = f"https://api.truthordarebot.xyz/api/dare?rating={rating}"
    response = requests.get(link)
    json_data = json.loads(response.text)
    msg = json_data['question']
    data.subClient.send_message(chatId=data.chatId, message=f"""[U]Dare for {data.author}
{msg}""")

@client.command()
def ss(data):
    url = f"https://shot.screenshotapi.net/screenshot?&url={data.message}&output=image&file_type=jpeg&wait_for_event=load"
    file = upload(url)
    
    data.subClient.send_message(chatId=data.chatId,file=file, fileType="image")

@client.command(condition=is_staff)
def purge(data):
    levels_to_purge = [int(data.message)]
    chat_users = data.subClient.get_chat_users(data.chatId, start=0, size=100).userId
    data.subClient.send_message(chatId=data.chatId, message="The bot is about to purge")
    for user_id in chat_users:
        user_level = data.subClient.get_user_info(user_id).level
        if user_level in levels_to_purge:
            data.subClient.kick(chatId=data.chatId, userId=user_id, allowRejoin=True)
    data.subClient.send_message(chatId=data.chatId, message="Purge complete")

@client.command("dice")
def dice(args):
    if not args.message:
        args.subClient.send_message(args.chatId, f"🎲 -{randint(1, 20)},(1-20)- 🎲")
    else:
        try:
            n1, n2 = map(int, args.message.split('d'))
            times = n1 if n1 < 20 else 20
            max_num = n2 if n2 < 1_000_000 else 1_000_000
            numbers = [randint(1, (max_num)) for _ in range(times)]

            args.subClient.send_message(args.chatId, f'🎲 -{sum(numbers)},[ {" ".join(map(str, numbers))}](1-{max_num})- 🎲')
        except Exception as e:
            print_exception(e)

@client.command()
def kill(data):
    sword_img = Image.open("sword.png")
    mention_users = data.subClient.get_message_info(chatId=data.chatId, messageId=data.messageId).mentionUserIds
    for user in mention_users:
        user_info = data.subClient.get_user_info(userId=str(user))
        user_avatar = user_info.icon
        user_nickname = user_info.nickname
        response = requests.get(user_avatar)
        with open(".aiyijhale.png", "wb") as file:
            file.write(response.content)
        avatar_img = Image.open(".aiyijhale.png").resize((175, 175))
        sword_img.paste(avatar_img, (295, 670))
        sword_img.save(".yihh3.png")
        with open(".yihh3.png", "rb") as final_img:
            try:
                data.subClient.send_message(
                    chatId=data.chatId, 
                    linkSnippetImage=final_img, 
                    linkSnippet=f"ndc://user-profile/{data.authorId}", 
                    message=f"{user_nickname} got {randint(1, 20)} killed from {data.author}"
                )
            except:
                pass
        os.remove(".aiyijhale.png")
        os.remove(".yihh3.png")
					
@client.command()
def slap(data):
    with open("slap.png", "rb") as slap_img:
        mention_ids = data.subClient.get_message_info(chatId=data.chatId, messageId=data.messageId).mentionUserIds
        for user_id in mention_ids:
            user = data.subClient.get_user_info(str(user_id))
            user_nickname = user.nickname
            user_icon_url = user.icon
            author = data.subClient.get_user_info(data.authorId)
            author_icon_url = author.icon
            with open(".haas.png", "wb") as haas_img:
                haas_img.write(requests.get(user_icon_url).content)
            with open(".aie.png", "wb") as aie_img:
                aie_img.write(requests.get(author_icon_url).content)
            Image.open("slap.png").resize((837, 736)).save("slape.png")
            slap_img = Image.open("slape.png")
            haas_img = Image.open(".haas.png").resize((190, 190)) 
            aie_img = Image.open(".aie.png").resize((180, 180))
            slap_img.paste(haas_img, (500, 400))
            slap_img.paste(aie_img, (290, 100))
            with open(".ijs.png", "wb") as ijs_img:
                slap_img.save(ijs_img)
            with open(".ijs.png", "rb") as ijs_img:
                try:
                    message = f"{user_nickname} got {randint(1, 20)} slap from {data.author}"
                    data.subClient.send_message(
                        linkSnippet=f"ndc://user-profile/{data.authorId}", 
                        linkSnippetImage=ijs_img, 
                        message=message, 
                        chatId=data.chatId
                    )
                except:
                    pass
            os.remove(".haas.png")
            os.remove(".aie.png")
            os.remove(".ijs.png")

@client.command()
def kiss(data):
	mention = data.subClient.get_message_info(chatId=data.chatId, messageId=data.messageId).mentionUserIds
	for user in mention:
		nkn=data.subClient.get_user_info(str(user)).nickname
		endpoint="kiss"
		r = requests.get("https://neko-love.xyz/api/v1/" + endpoint)
		filename="kiss1.png"
		image=r.json()["url"]
		reqs=requests.get(image)
		file=open(filename,"wb")
		file.write(reqs.content)
		file.close()
		Image.open("kiss1.png").resize((800,500)).save("kiss2.png")
		imgg=open("kiss2.png","rb")
		msg=f"""{data.author} kissed {nkn} {randint(1, 20)} times 😘"""
		data.subClient.send_message(linkSnippet=f"ndc://user-profile/{data.authorId}", linkSnippetImage=imgg, message=msg, chatId=data.chatId)
		os.remove("kiss2.png")
		os.remove("kiss1.png")

@client.command()
def trash(data):
    with open("trash.png", "rb") as img_file:
        mention = data.subClient.get_message_info(chatId=data.chatId, messageId=data.messageId).mentionUserIds
        for user in mention:
            user_info = data.subClient.get_user_info(str(user))
            nickname = user_info.nickname
            icon_url = user_info.icon

            response = requests.get(icon_url)
            with open(".a77ale.png", "wb") as icon_file:
                icon_file.write(response.content)

            pie_img = Image.open("trash.png") 
            user_icon = Image.open(".a77ale.png").resize((483,483))
            pie_img.paste(user_icon, (480, 0))
            pie_img.save(".iw83.png")
            with open(".iw83.png", "rb") as final_img:
                message = f"{nickname} got {randint(1, 20)} trash from {data.author}"
                data.subClient.send_message(chatId=data.chatId, linkSnippetImage=final_img, 
                                            linkSnippet=f"ndc://user-profile/{data.authorId}", message=message)
                
            os.remove(".a77ale.png")
            os.remove(".iw83.png")

@client.command()
def pie(data):
    with open("pie.png", "rb") as img_file:
        mention = data.subClient.get_message_info(chatId=data.chatId, messageId=data.messageId).mentionUserIds
        for user in mention:
            user_info = data.subClient.get_user_info(str(user))
            nickname = user_info.nickname
            icon_url = user_info.icon

            response = requests.get(icon_url)
            with open(".a44ale.png", "wb") as icon_file:
                icon_file.write(response.content)

            pie_img = Image.open("pie.png") 
            user_icon = Image.open(".a44ale.png").resize((328, 328))
            pie_img.paste(user_icon, (445, 406))
            pie_img.save(".iw82.png")
            with open(".iw82.png", "rb") as final_img:
                message = f"{nickname} got pie {randint(1, 20)}"
                data.subClient.send_message(chatId=data.chatId, linkSnippetImage=final_img, 
                                            linkSnippet=f"ndc://user-profile/{user}", message=message)
                
            os.remove(".a44ale.png")
            os.remove(".iw82.png")

@client.command(condition=is_staff)
def abw(args):
    if not args.message or args.message in args.subClient.banned_words:
        return
    try:
        args.message = args.message.lower().strip().split()
    except Exception:
        args.message = [args.message.lower().strip()]
    args.subClient.add_banned_words(args.message)
    args.subClient.send_message(args.chatId, "Banned word list updated")

@client.command(condition=is_staff)
def rbw(args):
    if not args.message:
        return
    try:
        args.message = args.message.lower().strip().split()
    except Exception:
        args.message = [args.message.lower().strip()]
    args.subClient.remove_banned_words(args.message)
    args.subClient.send_message(args.chatId, "Banned word list updated")
        
@client.command("bwl")
def banned_word_list(args):
    val = ""
    if args.subClient.banned_words:
        for elem in args.subClient.banned_words:
            val += elem + "\n"
    else:
        val = "No words in the list"
    args.subClient.send_message(args.chatId, val)

@client.command("welcome", condition=is_staff)
def welcome_channel(args):
    args.subClient.set_welcome_chat(args.chatId)
    args.subClient.send_message(args.chatId, "Welcome channel set!")

@client.command("unwelcome", condition=is_staff)
def unwelcome_channel(args):
    args.subClient.unset_welcome_chat()
    args.subClient.send_message(args.chatId, "Welcome channel unset!")

@client.command(condition=is_staff)
def id(data):
    if data.message=="":
        data.subClient.send_message(chatId=data.chatId,message=f"{data.comId}")
        data.subClient.send_message(chatId=data.chatId,message=data.chatId)
    else:
        bb=client.get_from_code(data.message)
        cid=bb.path[1:bb.path.index("/")]
        data.subClient.send_message(chatId=data.chatId,message=f"{cid}")
        try:
            chatId=bb.objectId
            data.subClient.send_message(chatId=data.chatId,message=f"{chatId}")
        except:
            pass

@client.command(condition=is_it_me)
def restart(self):
  sys.argv
  sys.executable
  self.subClient.send_message(chatId=self.chatId,message=f"Restarting")
  os.execv(sys.executable, ['python'] + sys.argv)

@client.command(condition=is_it_me)
def stop(args):
    args.subClient.send_message(args.chatId, "Stopping Bot")
    os.execv(sys.executable, ["None", "None"])

@client.command("profile")
def profileinfo(data):
    mention = data.subClient.get_message_info(chatId=data.chatId, messageId=data.messageId).mentionUserIds
    if "aminoapps.com" in data.message:
    	user=(client.get_from_code(data.message.split(' ')[0]).objectId)
    elif mention!=None:
    	for x in mention:
    		user=x
    else:
    	user=data.authorId
    x=data.subClient.get_user_info(userId=client.userId).json["role"]
    repa = data.subClient.get_user_info(userId=str(user)).reputation
    lvl = data.subClient.get_user_info(userId=str(user)).level
    crttime = client.get_user_info(userId=str(user)).createdTime[:-1].split('T')
    followers = data.subClient.get_user_achievements(userId=str(user)).numberOfFollowersCount
    profilchange = data.subClient.get_user_info(userId=str(user)).modifiedTime[:-1].split('T')
    commentz = data.subClient.get_user_info(userId=str(user)).commentsCount
    ic=data.subClient.get_user_info(str(user)).icon
    bg=data.subClient.get_user_info(userId=str(user)).mediaList
    if bg ==None:
        bgs="No Image"
    else:
	    bgs=bg[0][1]
    posts = data.subClient.get_user_achievements(userId=str(user)).numberOfPostsCreated
    if x==100:
        gstrk=data.subClient.get_user_info(userId=str(user)).globalStrikeCount
    else:
        gstrk="0"
    followed = data.subClient.get_user_info(userId=str(user)).followingCount
    if x==100:
        wrn=data.subClient.get_user_info(userId=str(user)).warningCount
        strk=data.subClient.get_user_info(userId=str(user)).strikeCount
    else:
        wrn= "0"
        strk= "0"
    sysrole = data.subClient.get_user_info(userId=str(user)).role
    h=data.subClient.get_user_info(userId=str(user)).nickname
    id=data.subClient.get_user_info(userId=str(user)).userId
    user_role = data.subClient.get_user_info(userId=str(user)).role
    if user_role == 0:
        user_role = 'Member'
    elif user_role == 100:
        user_role = 'Leader'
    elif user_role == 101:
        user_role = 'Curator'
    elif user_role == 102:
        user_role = 'Agent'
    data.subClient.send_message(data.chatId, message=f"""
[CB]Profile Info
[C]┅┅┅┅┅┅┅༻❁༺┅┅┅┅┅┅┅
❖Nickname: {h}
❖Role: {user_role}
❖UserId: {id}
❖Account created time: {crttime}
❖Last time the profile was changed: {profilchange}
❖Reputation points: {repa}
❖Account level: {lvl}
❖Number of posts created in the profile: {posts}
❖Number of comments on the profile wall: {commentz}
❖The number of people you follow: {followed}
❖Account followers: {followers}
❖Account number in system: {sysrole}
❖Strike: {strk}
❖Global strike: {gstrk}
❖Warning: {wrn}
❖Icon: {ic}
❖Background: {bgs}
	""")

disabled_welcome_messages = set()
with open('disabled_welcome_messages.txt', 'r') as file:
    for line in file:
        disabled_welcome_messages.add(int(line.rstrip('\n')))

@client.command(condition=is_staff)
def gcon(data):
    disabled_welcome_messages_file = 'disabled_welcome_messages.txt'

    if data.comId not in disabled_welcome_messages:
        data.subClient.send_message(data.chatId, "Chat welcome already on")
    else:
        with open(disabled_welcome_messages_file, 'r') as file:
            cids = [cid for cid in file if cid != f'{data.comId}\n']
        with open(disabled_welcome_messages_file, 'w') as file:
            file.write('\n'.join(cids))
        disabled_welcome_messages.remove(int(data.comId))
        data.subClient.send_message(data.chatId, "Chat welcome on")

@client.command(condition=is_staff)
def gcoff(data):
    com_id = int(data.comId)
    if com_id in disabled_welcome_messages:
        data.subClient.send_message(data.chatId, "Chat welcome is already off")
        return

    with open('disabled_welcome_messages.txt', 'a') as file:
        file.write(f'{data.comId}\n')

    disabled_welcome_messages.add(com_id)
    data.subClient.send_message(data.chatId, "Chat welcome off")

def welcome(data):
    if data.comId in disabled_welcome_messages:
        return
    info=data.subClient.get_chat_thread(chatId=data.chatId)
    data.subClient.send_message(data.chatId, f'''[BC]━━━━┅━━━┅━━━━
Welcome to the {info.title}
[C]Thanks for joining us ! ꒰🍻꒱
[C]Follow the rules and guidelines of the group chat.
[C]Respect the Host and Cohost and the members.
[C]Most of all enjoy chatting.🤗
[BC]━━━━┅━━━┅━━━━
''', embedTitle=data.author,embedLink=f"ndc://user-profile/{data.authorId}", embedImage=upload(data.info.message.author.icon))
def upload(url):
    link = requests.get(url)
    result = BytesIO(link.content)
    return result

def on_mage(data):
    mt=[114,109,108,100, 107,115,116,110,111,112,113,114,117,124,125,126,128,1,50,51,57,58,59]
    mtype = data.info.message.type
    if mtype in mt and data.message != None:
        user_id=data.authorId
        if user_id !=client.userId:
            try:
                data.subClient.kick(chatId=data.chatId, userId=data.authorId, allowRejoin=False)
            except:
                pass

@client.on_member_join_chat()
def join_catch(data):
    welcome_log(data)
    welcome(data)

@client.on_all()
def join_catch2(data):
    all_data(data)
    on_mage(data)

@client.on_message()
def join_catch3(data):
    afk_message(data)
    cranks(data)

client.launch(True)
print("ready")

def Root():
    j = 0
    while True:
        if j >= 120:
            client.close()
            print("socket close")
            client.run_amino_socket()
            print("socket start")
            j = 0
        j += 1
        time.sleep(1)
Root()