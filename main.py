import socket
import _thread
import socketserver
from app.server.udp_server import MyUDPRequestHandler
from app.server import udp_server, server
import constants

connected_clients = []



if __name__ == "__main__":

    try:
        # create UDP server
        UDP_server = socketserver.ThreadingUDPServer( (constants.UDP_IP, constants.UDP_PORT) , MyUDPRequestHandler )
        _thread.start_new_thread(server.listen_UDP_clients, (UDP_server,))
    except OverflowError:
        print("UDP port must be 0-65535")
    except OSError as e:
        print(e)
        raise
    except Exception as e:
        print(e)

    try:
        # create TCP server
        TCP_socket = server.create_TCP_server()
        print("TCP server up and running on {}".format(TCP_socket.getsockname()))
    except OverflowError as e:
        print("TCP port must be 0-65535")
    except OSError as e:
        print(e)
        raise

    # Main loop for listening new connections
    while True:
        try:
            # Establish new TCP connection and start new thread for that client
            TCP_connection, ip_address = TCP_socket.accept()
            connected_clients.append(TCP_connection)
            print( "New connection: {}".format(ip_address))
            _thread.start_new_thread(server.listen_TCP_clients, (TCP_connection, ip_address))

        except KeyboardInterrupt as e:
                print("Server stopped by user")
                break

        except BrokenPipeError as e:
            print("Client disconnected")

    TCP_socket.close()
