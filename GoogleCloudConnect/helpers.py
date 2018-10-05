# -*- coding: utf-8 -*-
# @Author: Lorenzo
# @Date:   2017-10-03 10:56:02
# @Last Modified by:   Lorenzo
# @Last Modified time: 2018-10-05 15:49:16

import json
import socket

from microchip.ateccx08a import ateccx08a

def load_device_conf():
    confstream = open('resource://device.conf.json')
    conf = ''
    while True:
        line = confstream.readline()
        if not line:
            break
        conf += line
    return json.loads(conf)

def get_timestamp():
    ip = __default_net["sock"][0].gethostbyname("now.httpbin.org")
    sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock.connect((ip, 80))

    req = (b"GET / HTTP/1.1\r\n"
           b"Host: now.httpbin.org\r\n" 
           b"User-Agent: curl/7.57.0\r\n"
           b"Accept: */*\r\n"
           b"\r\n")

    sock.sendall(req)

    state = 0 # waiting opening double quote to identify key
    timestamp = ""
    current_key = ""
    while True:
        byte = sock.recv(1)
        if state == 0 and byte == '"': # opening double quote
            state = 1 # read double quote content
        elif state == 1 and byte == '"': # closing double quote
            if current_key == "epoch":
                state = 2 # read epoch
            else:
                state = 0
            current_key = ""
        elif state == 1:
            current_key += byte
        elif state == 2:
            if byte == " ":
                state = 3 # read epoch
        elif state == 3:
            if byte == ".":
                break
            timestamp += byte

    timestamp = int(timestamp)
    sock.close()
    return timestamp

conf2atecctype = {
    'ATECC508A': ateccx08a.DEV_ATECC508A,
    'ATECC608A': ateccx08a.DEV_ATECC608A
}
