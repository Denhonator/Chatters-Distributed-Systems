import socketserver
import threading
from app.server import server

class MyUDPRequestHandler(socketserver.DatagramRequestHandler):

    def handle(self):

        print("UDP message from: {}".format(self.client_address))

        # Message received from another server
        datagram = self.rfile.readline().strip().decode('utf-8')

        print(datagram)

        print(threading.current_thread().name)


        #send to server clients
        server.castMessageToClients(datagram)
        
