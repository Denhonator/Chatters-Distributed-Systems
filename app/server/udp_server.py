import socketserver
import threading
import server

class MyUDPRequestHandler(socketserver.DatagramRequestHandler):

    def handle(self):

        print("UDP message from: {}".format(self.client_address))

        # Message received from another server
        datagram = self.rfile.readline().strip().decode('utf-8')


        if datagram[:3] == "MSG":
            #send to server clients
            server.castMessageToClients(datagram)
        elif "SERVER" in datagram:
            #Updates for server list
            server.update_Server(datagram)

        elif datagram[:3] = "DBM"
            server.update_Message(datagram)


        #print(threading.current_thread().name)
