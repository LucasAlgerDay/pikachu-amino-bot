import json
from os import path
import json
import random
import os
from time import time as timestamp
import names
from hashlib import sha1
from functools import reduce
from base64 import b85decode, b64decode
import random
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from requests import Session
import hmac
import platform,socket,re,uuid
import base64
from uuid import uuid4
sesion = Session()
THIS_FOLDER = path.dirname(path.abspath(__file__))
emailfile=path.join(THIS_FOLDER,"vc.json") # accounts.json file path

dictlist=[] # Empty list initialisation which will hold dictionaries from accounts.json

with open(emailfile) as f: # Opening the accounts.json file
    dictlist = json.load(f)

def sigg(data):
        key='EAB4F1B9E3340CD1631EDE3B587CC3EBEDF1AFA9'
        mac = hmac.new(bytes.fromhex(key), data.encode("utf-8"), sha1)
        digest = bytes.fromhex("52") + mac.digest()
        return base64.b64encode(digest).decode("utf-8")

def dev():
    hw=(names.get_full_name()+str(random.randint(0,10000000))+platform.version()+platform.machine()+names.get_first_name()+socket.gethostbyname(socket.gethostname())+':'.join(re.findall('..', '%012x' % uuid.getnode()))+platform.processor())
    identifier=sha1(hw.encode('utf-8')).digest()
    key='AE49550458D8E7C51D566916B04888BFB8B3CA7D'
    mac = hmac.new(bytes.fromhex(key), b"\x52" + identifier, sha1)
    return (f"52{identifier.hex()}{mac.hexdigest()}").upper()
def SID(email: str, password: str,device, proxies: dict = None):
        headers = {
            "NDCDEVICEID": dev(),
            #"NDC-MSG-SIG": dev.device_id_sig,
            "Accept-Language": "en-US",
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 5.1.1; SM-G973N Build/beyond1qlteue-user 5; com.narvii.amino.master/3.4.33562)",
            "Host": "service.narvii.com",
            "Accept-Encoding": "gzip",
            "Connection": "Keep-Alive"
        }
        
        data = json.dumps({
            "email": email,
            "v": 2,
            "secret": f"0 {password}",
            "deviceID": device,
            "clientType": 100,
            "action": "normal",
            "timestamp": int(timestamp() * 1000)
        })
        headers["NDC-MSG-SIG"]=sigg(data)
        sid=None
        proxy= {'http': 'socks5://pro1:1214@chile.zaicadiahost.xyz:5279', 'https':'socks5://pro1:1214@chile.zaicadiahost.xyz:5279'}

        response = sesion.post(f"https://service.narvii.com/api/v1/g/s/auth/login", headers=headers, data=data, proxies=proxy)
        if response.json()["api:message"]=="OK":
        	sid=response.json()["sid"]
        
        	
        return sid


def threadit(acc : dict): # Defining the main threading function which will run in a threaded loop
    #global totalcoin # Using the global variable totalcoin inside the block
    email=acc["email"] # Assigns the value of "email" key inside email variable
    device=acc["device"] # Assigns the value of "device" key inside device variable
    password=acc["password"] # Assigns the value of "password" key inside password variable
    try:
            sid=SID(email,password,device)
            with open("sid.txt","a") as d:
                 d.write(f"{sid}\n")
            #print("saved")
    except Exception as f:
            print(f)
            pass

def sid_e():
    #print(f"{len(dictlist)} accounts loaded")
    for amp in dictlist:
        threadit(amp)
    #print("sid")