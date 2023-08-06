import json
import os

import requests
from datetime import datetime
import socket

# from config import CONFIG

API_KEY = 'http://192.168.29.195:12000/trainer'
ALL_LOG = f"{API_KEY}/all_logs"
create_log = f"{API_KEY}/create_log"
LOGS_DATERANGE = f"{API_KEY}//logs_daterange"
TODAY_LOG = f"{API_KEY}//gettodaylog"
LOG_BY_LEVELDATE = f"{API_KEY}/get_log_by_leveldaterange"
SOURCE = "Trainer"
collection = "trainer_log"

hostname = socket.gethostname()
host_ip = socket.gethostbyname(hostname)


def date_serializer(o):
    if isinstance(o, datetime):
        return o.__str__()


def call_log(loglevel: str, data: str):
    json_data = {
        "source": SOURCE,
        "time": datetime.now().isoformat(),
        "log_data": data,
        "module_name": "tinyurl",
        "domain": API_KEY,
        "loglevel": loglevel,
        "logtype": "Warning",
        "loginID": 0,
        "ip_address": host_ip,
        "loggedby": os.getlogin(),
        "hostname": hostname,
        "messageID": "",
        "context_id": "",
        "created_on": datetime.now().isoformat()

    }
    return json_data


async def INFO(message):
    res = call_log(loglevel="Info", data=message)
    result = requests.post(url=create_log, data=json.dumps(res, default=date_serializer),
                           params={"modulename": collection})
    return result


async def FATAL(message):
    res = call_log(loglevel="Fatal", data=message)
    result = requests.post(url=create_log, data=json.dumps(res, default=date_serializer),
                           params={"modulename": collection})
    return result


async def ERROR(message):
    res = call_log(loglevel="Error", data=message)
    result = requests.post(url=create_log, data=json.dumps(res, default=date_serializer),
                           params={"modulename": collection})
    return result


async def WARN(message):
    res = call_log(loglevel="Warn", data=message)
    result = requests.post(url=create_log, data=json.dumps(res, default=date_serializer),
                           params={"modulename": collection})
    return result


async def DEBUG(message):
    res = call_log(loglevel="Debug", data=message)
    result = requests.post(url=create_log, data=json.dumps(res, default=date_serializer),
                           params={"modulename": collection})
    return result


async def TRACE(message):
    res = call_log(loglevel="Trace", data=message)
    result = requests.post(url=create_log, data=json.dumps(res, default=date_serializer),
                           params={"modulename": collection})
    return result
