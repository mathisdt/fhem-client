#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
import datetime
import os.path
import socket
import time
import re

if not os.path.isfile("config.ini"):
    print(
        "config.ini not found - maybe you didn't copy (and customize) the file config-template.ini to config.ini yet?")
    exit(1)

config = configparser.ConfigParser()
config.read("config.ini")


def fhem_task(fhem_cmd):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((config['FHEM']['host'], int(config['FHEM']['telnet_port'])))
    s.send(str.encode(config['FHEM']['password'] + "\n", 'ascii'))
    s.recv(4000)
    s.send((fhem_cmd + "\n").encode('ascii'))
    time.sleep(0.1)
    result = s.recv(128000)
    return result[5:-2].decode('ascii')


def age_hours(timestamp: str, decimal_separator: str = ".", tz: datetime.tzinfo = None):
    try:
        modified_timestamp = re.sub(r'Z', 'UTC', re.sub(r'\.\d{1,3}', '', timestamp))
        given_timestamp = datetime.datetime.strptime(modified_timestamp, '%Y-%m-%dT%H:%M:%S%Z')
        given_timestamp = given_timestamp.replace(tzinfo=tz)
        now_timestamp = datetime.datetime.now(tz=given_timestamp.tzinfo)
        delta: datetime.timedelta = now_timestamp - given_timestamp
        return f"{delta / datetime.timedelta(hours=1):.1f}".replace('.', decimal_separator)
    except:
        return "?"


# default values
now = time.localtime()
year = time.strftime("%Y", now)
month = time.strftime("%m", now)
day = time.strftime("%d", now)
hour = time.strftime("%H", now)
minute = time.strftime("%M", now)
second = time.strftime("%S", now)
# FHEM values
for req in config['REQUEST']:
    locals()[req] = eval(f"fhem_task(config['REQUEST']['{req}'])")

pattern = config['OUTPUT']['str']
print(eval(f"""f'''{pattern}'''"""))
