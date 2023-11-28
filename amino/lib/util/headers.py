import base64
import hmac
from hashlib import sha1
from uuid import uuid4

from . import device, signature
sid = None

class Headers:
    def __init__(self, data = None, type = None, deviceId: str = None, sig: str = None):
        if deviceId:
            dev = device.DeviceGenerator(deviceId=deviceId)
        else:
            dev = device.DeviceGenerator()

        headers = {
            "NDCDEVICEID": dev.device_id,
            "Accept-Language": "en-US",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Apple iPhone13,4 iOS v15.6.1 Main/3.12.9",
            "Host": "service.aminoapps.com",
            "Accept-Encoding": "gzip",
            "Connection": "Keep-Alive"
        }

        if data:
            headers["Content-Length"] = str(len(data))
            headers["NDC-MSG-SIG"] = signature(data)
        if sid: headers["NDCAUTH"] = f"sid={sid}"
        if type: headers["Content-Type"] = type
        if sig: headers["NDC-MSG-SIG"] = sig

        self.headers = headers
