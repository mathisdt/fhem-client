#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
import os.path
import socket
import time

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
