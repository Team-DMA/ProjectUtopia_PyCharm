import socket
import threading


class TCP_HANDLER(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True

        self.tcpIp = ""
        self.tcpPort = 12347
        self.bufferSize = 20

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.tcpIp, self.tcpPort))
        self.sock.listen(1)

        self.start()
        print("\nTCP Handler init.")

    def run(self):
        """
        Handling the TCP connection for smartphone
        """

        print("\nwait for first TCP Data")
        while True:

            connection, client_address = self.sock.accept()

            try:
                data = connection.recv(self.bufferSize)

            except Exception as e:
                print("\nTCP-Handler Error: " + str(e))
            finally:
                connection.close()
