#!/usr/bin/python                                                                                                                                                                     

import socket
import time

s = socket.socket()

address = ("localhost", 7757)

# TODO: Client should listen for server messages at all times

try:
    s.connect(address)
    print("Connected!")
    while True:
        s.send(b"MSG:HELLO")
        reply = s.recv(1024).decode('utf-8')    # Server should confirm success
        print(reply)
        time.sleep(2)
except Exception as e:
    print(e)
    print("Failed to connect to "+str(address))

s.close()
