#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os.path
import configparser
import telnetlib
import time

if not os.path.isfile("config.ini"):
    print("config.ini not found - maybe you didn't copy (and customize) the file config-template.ini to config.ini yet?")
    exit(1)

config = configparser.ConfigParser()
config.read("config.ini")


def fhem_task(fhem_cmd):
    tc = telnetlib.Telnet(config['FHEM']['host'], config['FHEM']['telnet_port'])
    tc.read_until(b"Password: ")
    tc.write(config['FHEM']['password'].encode('ascii') + b"\n")
    tc.read_until(b"\n")
    tc.write(fhem_cmd.encode('ascii') + b"\n")
    erg = tc.read_until(b"\n").strip().decode('ascii')
    tc.close()
    return erg


val = {}
# default values
now = time.localtime()
val["year"] = time.strftime("%Y", now)
val["month"] = time.strftime("%m", now)
val["day"] = time.strftime("%d", now)
val["hour"] = time.strftime("%H", now)
val["minute"] = time.strftime("%M", now)
val["second"] = time.strftime("%S", now)
# FHEM values
for req in config['REQUEST']:
    val[req] = fhem_task(config['REQUEST'][req])

pattern = config['OUTPUT']['str']
print(pattern.format_map(val))
