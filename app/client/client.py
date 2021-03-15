#!/usr/bin/python
import sys
import socket
import time
import _thread

disconnect = False

def listen_to_server(socket,addr):
    global disconnect
    while not disconnect:
        try:
            msg = socket.recv(1024).decode('utf-8')
        except Exception as e:
            print(e)
            break
        if msg[:3] == "MSG":
            print(msg[4:])      # Display received message
        elif "FAIL" in msg:
            disconnect = True
        else:
            print(msg)          # Non-MSG

def Connect(address):
    global disconnect

    try:
        connected = False
        while not connected:
            s = socket.socket()
            s.connect(address)
            print("Connected!")
            s.send(b"MSG:HELLO")
            reply = s.recv(1024).decode('utf-8')    # Server should confirm success
            if "OK" in reply:
                connected = True
                _thread.start_new_thread(listen_to_server, (s, address))
                while not disconnect:
                    sendmsg = "MSG:" + input("> ")


                    """ EVALUATION OF DIFFERENT CASES"""
                    if "spam" in sendmsg:
                        for i in range(0,1000):
                            msg = "{}".format(i)
                            s.send(msg.encode('utf-8'))

                    elif "payload" in sendmsg:
                        msg = ""
                        for i in range(1,40000):
                            msg += "{}".format(i)
                        s.send(msg.encode())



                    else:
                        s.send(sendmsg.encode('utf-8'))
                        time.sleep(0.5)
            elif "CHANGE" in reply:
                #"CHANGE:ADDRESS:PORT"

                msgParts = reply.split(":")
                address = (msgParts[1],int(msgParts[2]))
                print("Requested server change to {}".format(address))
                s.close()

                #TODO: Automatically attempt connection to suggested server
            else:
                print("Server was not OK with the message")

    except Exception as e:
        print(e)
        print("Failed to connect to "+str(address))
        raise e

    s.close()


address = ("localhost", int(sys.argv[1]))
Connect(address)
