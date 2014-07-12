#!/usr/bin/env python
# encoding: utf-8

import socks
import socket


# HOST = "baidu.com"
HOST = "better-goagent.blogspot.jp"
LOCATION = "/2013/11/goagent-306-cr4.html"
PORT = 80

s = socks.socksocket()
s.setproxy(socks.PROXY_TYPE_SOCKS5, "106.187.50.89", 1080)
# s.setproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 1080, rdns=True)
s.connect((HOST, PORT))
# s.settimeout(0)

def decript_data(response):
    encript_data = []

    for data in response:
        data = chr(ord(data) ^ 0x12)
        encript_data.append(data)

    return "".join(encript_data)

def encript_data(send_message):
    decript_data = []

    for data in send_message:
        data = chr(ord(data) ^ 0x12)
        decript_data.append(data)

    data_to_send = "".join(decript_data)

    print "*******data to send\n", data_to_send

    return data_to_send


http_connect_message = "GET " + LOCATION + " HTTP/1.1\r\nHost: " + HOST +"\r\n\r\n"
s.sendall(encript_data(http_connect_message))


# TODO 用HTTP协议的话，content-length来判断内容长度

#Now receive data
content_length = None

fp = s.makefile('rb', 0)

# Initialize with Simple-Response defaults
line = fp.readline()
print "reply:", repr(line)
if not line:
    # Presumably, the server closed the connection before
    # sending a valid response.
    raise Exception("opps")
try:
    [version, status, reason] = line.split(None, 2)
except ValueError:
    try:
        [version, status] = line.split(None, 1)
        reason = ""
    except ValueError:
        # empty version will cause next test to fail and status
        # will be treated as 0.9 response.
        version = ""

# while True:
#     try:
#         data = s.recv(4096)
#         print "*******get encript response\n", data
#         print "*******get response for http header\n", decript_data(data)
#     except socket.error:
#         continue
#     if not data:
#         break

s.close()
