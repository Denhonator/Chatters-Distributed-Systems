import socket
import _thread
import socketserver
from random import randint
from app.database import models
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
                connected_clients.append(connected_client)
                response, new_server = is_new_server_needed()
                is_client = True

            if response:
                print("Too much traffic, switch to {}", format(new_server))
                connected_client.send( new_server.encode() ) #respond client with an id of a server
                
            else:
                print("sending messages to other servers as well...")
                send_UDP_message(message.encode())
                models.save_new_message(constants.TCP_PORT, str(message), str(connected_client))
                message = b"OK"
                connected_client.send( message ) # Send OK, so client can continue spamming

                print("DONE")
                print("Waiting for new connections...")

        except BrokenPipeError as e:
            print(e)

        except Exception as e:
            print(e)


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


def send_UDP_message(message):
    #UDP_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    for server in models.get_servers():
        if int(server.id) != constants.UDP_PORT:
            UDP_socket.sendto(message, (constants.UDP_IP, int(server.id)))


def is_new_server_needed():
    if len(connected_clients) % 2 == 0:
        servers = models.get_servers()
        number_of_servers = len(servers)
        random_number = randint(0, number_of_servers - 1)
        random_server = servers[random_number].id
        return True, str(random_server)
    else:
        return False, "0000"


# Remove a client from the list
def remove_client(connected_client):
    if connected_client in connected_clients:
        connected_clients.remove(connected_client)


