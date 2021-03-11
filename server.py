#!/usr/bin/python                                                                                                                                                                      

import socket
import _thread

def on_new_client(clientsocket,addr):

    # Message will be "server" or "client"
    msg = clientsocket.recv(1024).decode('utf-8')
    print(msg)
    
    if msg == "client":

        # Responde back to client, "client"
        msg = b"client"
        clientsocket.send(msg)

        while True:
            try:
                msg = clientsocket.recv(1024).decode('utf-8')
                print(msg)

                msg = b"client"
                clientsocket.send(msg)
                

            except BrokenPipeError as e:
                print("Client shut down")
                break
                
            except Exception as e:
                print(e)
                break

    elif msg == "server":

        # Responde back to server, "server"
        msg = b"server"
        clientsocket.send(msg)

        while True:
            try:
                msg = clientsocket.recv(1024).decode('utf-8')
                print(msg)

                msg = b"server"
                clientsocket.send(msg)
                

            except BrokenPipeError as e:
                print("Client shut down")
                break
                
            except Exception as e:
                print(e)
                break

        print(str(addr) + " disconnected")   # Should check connection with ping
        clientsocket.close()



# START
s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host = ''
port = 7757

print("Server started!")

s.bind((host, port))
s.listen(5)

client_list = []

while True:
    try:
        c, addr = s.accept()
        client_list.append(c)
        print("Got connection from" + str(addr))
        _thread.start_new_thread(on_new_client,(c,addr))

    except KeyboardInterrupt as e:
            print("Server stopped SIGTERM")
            break

s.close()