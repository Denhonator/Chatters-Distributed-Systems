import socketserver
import threading
from app.server import server

class MyUDPRequestHandler(socketserver.DatagramRequestHandler):

    def handle(self):

        print("UDP message from: {}".format(self.client_address))

        # Message received from another server
        datagram = self.rfile.readline().strip().decode('utf-8')


        if "MSG" in datagram and not "DBM" in datagram:
            #send to server clients
            server.castMessageToClients(datagram)
        elif "SERVER" in datagram:
            #Updates for server list
            server.update_Server(datagram)

        elif "DBM" in datagram:
            server.update_Message(datagram)


        #print(threading.current_thread().name)
