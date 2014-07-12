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
s.settimeout(0)

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


#Now receive data
response = []
# FIXME 这里需要content-length配合
while True:
    try:
        data = s.recv(4096)
    except socket.error:
        continue

    if not data:
        break
    response.append(data)

response = "".join(response)
# response = "".join(s.recv(1024))
print "*******get encript response\n", response
print "*******get response for http header\n", decript_data(response)

s.close()
