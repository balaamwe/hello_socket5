#!/usr/bin/env python
# encoding: utf-8

import socks

s = socks.socksocket()
s.setproxy(socks.PROXY_TYPE_SOCKS5, "106.187.50.89", 1080)
# s.setproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 1080, rdns=True)
s.connect(("baidu.com", 80))

http_connect_message = "GET / HTTP/1.1\r\nHost: baidu.com\r\n\r\n"
s.sendall(http_connect_message)

#Now receive data
response = s.recv(4096)
print "get response for http header", response

s.close()
