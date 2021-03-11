#!/usr/bin/python                                                                                                                                                                     

import socket
import time

s = socket.socket()
address = ("localhost", 7757)

# TODO: Client should listen for server messages at all times

try:
    s.connect(address)
    print("Connected!")
    time.sleep(2)

    s.send(b"client")
    reply = s.recv(1024).decode('utf-8')
    reply = str(reply)
    print(reply)

    if reply == "client":
        print("Connected as a client")
        while True:
            # Operations
            time.sleep(2)
            print("client polling server")

    else:
        print("Could not confirm as a client")
        

except KeyboardInterrupt as e:
    print("Client Stopped")

except BrokenPipeError as e:
    print("Server connection error")

except Exception as e:
    print(e)
    print("Failed to connect to "+str(address))



s.close()

