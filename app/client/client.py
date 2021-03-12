#!/usr/bin/python                                                                                                                                                                     

import socket
import time

s = socket.socket()
address = ("localhost", 7500)
s.connect(address)
print("Connected!")
# TODO: Client should listen for server messages at all times

while True:
    try:
        
        time.sleep(2)

        s.send(b"client")
        reply = s.recv(1024).decode('utf-8')
        print(reply)

    except KeyboardInterrupt as e:
        print("Client Stopped")

    except BrokenPipeError as e:
        print("Server connection error")

    except Exception as e:
        print(e)
        print("Failed to connect to "+str(address))



s.close()

