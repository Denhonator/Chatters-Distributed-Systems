#!/usr/bin/python                                                                                                                                                                      

import socket
import _thread

def on_new_client(clientsocket,addr):
    while True:
        try:
            msg = clientsocket.recv(1024).decode('utf-8')
        except Exception as e:
            print(e)
            break
        print(str(addr) + " >> " + msg)
        if msg[:3] == "MSG":
            msg = b"SRV:MSG received OK"
        else:
            msg = b"SRV:Received non-MSG"
        clientsocket.send(msg)
        
    print(str(addr) + " disconnected")   # Should check connection with ping
    clientsocket.close()

s = socket.socket()
host = ''
port = 7757

print("Server started!")

s.bind((host, port))
s.listen(5)

while True:
   c, addr = s.accept()
   print("Got connection from" + str(addr))
   _thread.start_new_thread(on_new_client,(c,addr))
s.close()
