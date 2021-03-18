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
        #else:
            #print(msg)          # Non-MSG

def Connect(address):
    global disconnect
    global nick

    try:
        connected = False
        while not connected:
            s = socket.socket()
            s.connect(address)
            print("Connected!")
            s.send(b"MSG:HELLO")
            reply = s.recv(1024).decode('utf-8')    # Server should confirm success
            print(reply)
            if "OK" in reply:
                connected = True
                _thread.start_new_thread(listen_to_server, (s, address))
                while not disconnect:
                    sendmsg = "MSG:" + " {}: ".format(nick) + input("> ")

                    """ EVALUATION OF DIFFERENT CASES"""
                    if "spam" in sendmsg:
                        for i in range(0,50000):
                            sendmsg = "MSG: {}".format(i)
                            s.send(sendmsg.encode('utf-8'))

                    elif "payload" in sendmsg:
                        msg = ""
                        for i in range(1,40000):
                            sendmsg +="{}".format(i)
                        s.send(sendmsg.encode())



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
                time.sleep(0.5)

    except Exception as e:
        print(e)
        print("Failed to connect to "+str(address))
        raise e

    s.close()


#MAIN
try:
    nick = input("Enter nick: ").strip()
except:
    nick = "anon"
address = (input("Enter address: ").strip(), int(input("Enter port: ")))
Connect(address)
