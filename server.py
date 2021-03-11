#!/usr/bin/python

import socket
import _thread
from models import db, Server, Message
import random


clientCount = 0

def on_new_client(clientsocket,addr, serverAddr):
    global clientCount
    while True:
        try:
            msg = clientsocket.recv(1024).decode('utf-8')
        except Exception as e:
            print(e)
            break
        print(str(addr) + " >> " + msg)
        if msg[:3] == "MSG":
            clientCount += 1
            address = selectServer(clientCount, serverAddr)
            if address != serverAddr:
                msg = b"CHANGE:"+ address
            else:
                msg = b"SRV:MSG received OK"
        else:
            msg = b"SRV:Received non-MSG"
        clientsocket.send(msg)

    print(str(addr) + " disconnected")   # Should check connection with ping
    clientsocket.close()

s = socket.socket()
host = ''
port = 7757

addrString = host + ":" + str(port)


print("Server started!")

s.bind((host, port))
s.listen(5)

while True:
   c, addr = s.accept()
   print("Got connection from" + str(addr))
   _thread.start_new_thread(on_new_client,(c,addr, addrString))
s.close()


def selectServer(numClients, addr):
    # Client changed based on count (to simulate traffic)
    if numClients % 2 == 0:
        selected = random.choice(getServerList())
        return selected.address
    else:
        return addr


def getServerList():
    return Server.Query.all()
