import socket
import threading


class TCP_HANDLER(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True

        self.TCP_IP = ""
        self.TCP_PORT = 12347
        self.BUFFER_SIZE = 20

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.TCP_IP,self.TCP_PORT))
        self.sock.listen(1)
        
        self.start()
        print("\nTCP Handler init.")

    def run(self):

        print("\nWarte auf erste TCP-Daten")
        while True:
            
            connection, client_address = self.sock.accept()

            try:
                #print("\nConnection from: "+str(client_address))
                data = connection.recv(self.BUFFER_SIZE)

            except Exception as e:
                        print("\nTCP-Handler Error: "+ str(e))
            finally:
                connection.close()
