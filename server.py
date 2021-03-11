#!/usr/bin/python
import socket
import _thread
from models import db, Server, Message
import random


clientCount = 0

#TODO: UDP listener thread to receive messages from other servers at all times
#These must then be forwarded to clients
#TODO: Forward received messages to clients either where they are received
#Or in a separate thread if needed
#Main thread: Listens for new connections
#Per client thread: Listens for client messages
#UDP listen thread: Listens for messages from other servers

#TODO: Send old messages to new clients/servers (that they might have missed)
#as they connect for synchronization, but maybe not necessary?

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

# Must know own address
def sendMessageToServers(message, ownServer):
    #fake multicast
    for server in getServerList()
        if server.address != ownServer:
            adr = server.address.split(":")
            ip = adr[0]
            #UDP Port = Port + 1
            port = str(int(adr[1]) +1)
            s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            s.sendto(message.encode('utf-8'), ip, port)
