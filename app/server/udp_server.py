import socketserver
import threading



class MyUDPRequestHandler(socketserver.DatagramRequestHandler):

    def handle(self):

        print("UDP message from: {}".format(self.client_address))
        

        # Message received from another server
        datagram = str(self.rfile.readline().strip())

        print(threading.current_thread().name)
        #self.wfile.write("Message from Server! Hello Client".encode())
