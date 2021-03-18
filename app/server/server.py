import socket
import _thread
import socketserver
from random import randint
from database import models
import constants


connected_clients = []
UDP_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def listen_TCP_clients(connected_client, ip_address):
    is_client = False

    while True:
        try:
            message = connected_client.recv(constants.BUFFER_SIZE).decode('utf-8')
            print("A message: '{}' received from {}".format(message, ip_address))

            if not is_client:
                # Add client to client list and check if new server is needed
                connected_clients.append(connected_client)
                response, new_server = is_new_server_needed()
                is_client = True

            if response:
                print("Too much traffic, {}",format(new_server))
                connected_client.send( new_server.encode() ) #respond client with an id of a server

            if "fail" in message:
                #Simulate client fail and disconnetction
                print("client {} disconnected".format(connected_client))
                connected_client.send("FAIL".encode())

            if not "MSG" in message:
                #No MSG identifier in message
                print("invalid message")
                connected_client.send("INVALID".encode())

            else:
                print("sending messages to other servers and clients as well...")
                send_UDP_message(message.encode())
                models.save_new_message(constants.TCP_PORT, str(message), str(connected_client))
                reply = b"OK"
                connected_client.send(reply) # Send OK, so client can continue spamming


                #send msg to own clients except sendee
                print("sending message to other clients")
                for c in connected_clients:
                    print("client :")
                    try:
                        if c != connected_client:
                            c.send(message.encode())
                        else:
                            print("self")
                    except Exception as e:

                        print("invalid client")
                        continue

                print("DONE")
                print("Waiting for new connections...")



        except BrokenPipeError as e:
            raise e
            print(e)
            break

        except Exception as e:
            raise e
            print(e)
            break


def listen_UDP_clients(UDP_server):
    print("UDP server up and running")
    UDP_server.serve_forever()


def create_TCP_server():
    # Create socket for TCP connections, and start the server
    TCP_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCP_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    TCP_socket.bind((constants.TCP_IP, constants.TCP_PORT))
    TCP_socket.listen(constants.BACKLOG)
    return TCP_socket


""" Server to Server Communication"""

def send_UDP_message(message):
    #UDP_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for server in models.get_servers():
        if int(server.id) != constants.UDP_PORT:
            UDP_socket.sendto(message, (server.address, int(server.id)))

def send_Database():
    buf = 1024
    print("sending database items")
    for server in models.get_servers():
        if int(server.id) != constants.UDP_PORT:
            #send servers
            for s in models.get_servers():
                data = "SERVER:{}:{}".format(s.address, s.id) # Format SERVER:IP:PORT
                UDP_socket.sendto(data.encode(), (constants.UDP_IP, int(server.id)))
            #send messages
            for m in models.get_messages():
                data = "DBM:{}:{}:{}:{}".format(m.serverID, m.timestamp, m.message, m.user)
                UDP_socket.sendto(data.encode(), (constants.UDP_IP, int(server.id)))

def update_Server(serverString):
    server = serverString.split(":")
    if not models.session.query(Server).filter_by(id = server[2], address = server[1]):
        models.session.add(Server(server[2], server[1]))

def update_Message(messageString):

    try:
        message = messageString.split(":")
        if not models.session.query(Message).filter_by(serverID = message[1], timestamp = message[2]):
            models.session.add(Message(
            serverID = message[1],
            timestamp = message[2],
            message = message[3],
            user = message[4]))
    except Exception as e:
        print("Error updating message: {}".format(messageString))





""" Server Check, Client Removal and message casting"""

def is_new_server_needed():
    if len(connected_clients) % 2 == 0:
        servers = models.get_servers()
        number_of_servers = len(servers)
        random_number = randint(0, number_of_servers - 1)
        random_server_ip = servers[random_number].address
        random_server_port = servers[random_number].id

        msg = "CHANGE:{}:{}".format(random_server_ip, random_server_port)

        return True, msg
    else:
        return False, b"OK"


# Remove a client from the list
def remove_client(connected_client):
    if connected_client in connected_clients:
        connected_clients.remove(connected_client)

#Send recieved UDP message to clients
def castMessageToClients(message):
    global connected_clients
    print("sending message to other clients")
    for c in connected_clients:
        print("client :")
        try:

            c.send(message.encode())

        except Exception as e:

            print("invalid client")
            continue
