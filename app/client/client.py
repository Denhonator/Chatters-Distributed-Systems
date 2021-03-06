#!/usr/bin/python
import sys
import socket
import time
import _thread
import threading

disconnect = False
consoleLock = threading.Lock()

def listen_to_server(socket,addr):
    global disconnect
    while not disconnect:
        try:
            msgs = socket.recv(1024).decode('utf-8').split("\\r\\n")
            for msg in msgs:
                if msg[:3] == "MSG":
                    consoleLock.acquire()
                    print(msg[4:])
                    consoleLock.release()    # Display received message
                elif "FAIL" in msg:
                    disconnect = True
                
        except Exception as e:
            print(e)
            break

def Connect(address):
    global disconnect
    global nick

    try:
        connected = False
        while not connected:
            s = socket.socket()
            s.connect(address)
            print("Connected!")
            s.send(b"MSG:HELLO\r\n")
            reply = s.recv(1024).decode('utf-8')    # Server should confirm success
            print(reply)
            if "OK" in reply:
                connected = True
                _thread.start_new_thread(listen_to_server, (s, address))
                while not disconnect:
                    sendmsg = "MSG:" + " {}: \r\n".format(nick) + input("> ")

                    """ EVALUATION OF DIFFERENT CASES"""
                    if "spam" in sendmsg:
                        for i in range(0,50000):
                            sendmsg = "MSG: {}\r\n".format(i)
                            s.send(sendmsg.encode('utf-8'))

                    elif "payload" in sendmsg:
                        msg = ""
                        for i in range(1,40000):
                            sendmsg +="{}".format(i)
                        s.send((sendmsg+"\r\n").encode())



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
    nick = sys.argv[3]
except:
    nick = "anon"
address = (sys.argv[1], int(sys.argv[2]))
Connect(address)
