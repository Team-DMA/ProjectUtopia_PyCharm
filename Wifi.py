import socket
import threading
import time


class RCV_WIFI_MODULE(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True

        #VAR INIT
        self.UDP_IP = ""
        self.UDP_PORT = 12345
        self.PING_PORT = 12346
        self.Smartphone_IP = 0
        self.sock = None
        self.data = None
        self.targetSpeedFB = 0
        self.rotateStrength = 0
        self.Kp = 0.0
        self.Ki = 0.0
        self.Kd = 0.0
        self.neueDaten = False
        self.KonstantenReceived = False
        self.error = False

        self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.sock.bind((self.UDP_IP,self.UDP_PORT))

        self.start()

        print("\nRcvWifi iniziiert")

    def run(self):

        #global neueDaten
        #neueDaten = False

        print("\nEigene IP: " + str(socket.gethostbyname(socket.gethostname() + ".local")))


        print("\nWarte auf erste Daten von Smartphone...")
        while True:

            if(self.neueDaten == False):

                #start = float(time.process_time()) #debug zeitmessung

                self.data, (self.ip, self.port) = self.sock.recvfrom(1024) # buffer size is 1024 bytes
                self.Smartphone_IP = self.ip #Smartphone IP festlegen

                if(self.data != None):
                    length = len(self.data)

                    try:

                        if(self.data.decode("utf-8").count("|") == 3):
                            print("\nVerbindungsanfrage: Schicke {0} Bytes zurück an {1}:{2}".format(length, self.ip, self.PING_PORT))

                            lesbarerString = self.data.decode("utf-8")
                            randomBytes, Kp, Ki, Kd = lesbarerString.split("|")
                            self.Kp = float(Kp)
                            self.Ki = float(Ki)
                            self.Kd = float(Kd)

                            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                            sock.sendto(self.data, (self.ip, self.PING_PORT))
                            self.KonstantenReceived = True
                            self.neueDaten = False
                        elif(self.data.decode("utf-8").count("|") == 1):

                            lesbarerString = self.data.decode("utf-8")
                            strengthL, strengthR = lesbarerString.split("|")

                            print("stengthL: " + strengthL + ", strengthR: " + strengthR)

                            self.targetSpeedFB = int(strengthL)
                            self.rotateStrength = int(strengthR)                        

                            #print("\nDurchlaufdauer: " + str(float(float(time.process_time()) - float(start)))) #debug zeitmessung
                            
                            self.neueDaten = True
                        else:
                            self.error = True
                    except Exception as e:
                        print("\nWifi Error: "+ str(e))
             
                        
class SEND_WIFI_MODULE(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True

        #VAR INIT
        self.Smartphone_IP = 0
        self.SEND_PORT = 12348
        self.sendFlag = True
        self.msg = ""

        self.start()

        print("\nSendWifi iniziiert")

    def run(self):

        while True:

            time.sleep(1)

            if(self.Smartphone_IP != 0):

                if(self.msg != ""):

                    #Daten vorbereiten:
                    data = bytearray(self.msg, "UTF-8")

                    #

                    if(self.sendFlag == True):

                        self.sendFlag = False

                        try:
                            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                            sock.sendto(data, (self.Smartphone_IP, self.SEND_PORT))
                            #print("Msg: '"+str(self.msg)+"' send to: "+str(self.Smartphone_IP)+":"+str(self.SEND_PORT))
                            self.sendFlag = True

                        except Exception as e:
                                print("\nWifi Error: "+ str(e))
               
