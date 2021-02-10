import socket
import threading
import time


class RCV_WIFI_MODULE(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True

        #VAR INIT
        self.udpIp = ""
        self.udpPort = 12345
        self.pingPort = 12346
        self.smartphoneIP = 0
        self.sock = None
        self.data = None
        self.targetSpeedFB = 0
        self.rotateStrength = 0
        self.Kp = 0.0
        self.Ki = 0.0
        self.Kd = 0.0
        self.newData = False
        self.constantsReceived = False
        self.error = False

        self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.sock.bind((self.udpIp,self.udpPort))

        self.start()

        print("\nRcvWifi initialized")

    def run(self):

        #global newData
        #newData = False

        print("\nOwn IP: " + str(socket.gethostbyname(socket.gethostname() + ".local")))


        print("\nWait for first Data from Smartphone..")
        while True:

            if not self.newData:

                #start = float(time.process_time()) #debug time measurement

                self.data, (self.ip, self.port) = self.sock.recvfrom(1024) # buffer size is 1024 bytes
                self.smartphoneIP = self.ip # set Smartphone IP

                if self.data is not None:
                    length = len(self.data)

                    try:

                        if self.data.decode("utf-8").count("|") == 3:
                            print("\nConnection initialization: send {0} Bytes back to {1}:{2}".format(length, self.ip, self.pingPort))

                            readableString = self.data.decode("utf-8")
                            randomBytes, Kp, Ki, Kd = readableString.split("|")
                            self.Kp = float(Kp)
                            self.Ki = float(Ki)
                            self.Kd = float(Kd)

                            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                            sock.sendto(self.data, (self.ip, self.pingPort))
                            self.constantsReceived = True
                            self.newData = False

                        elif self.data.decode("utf-8").count("|") == 1:

                            readableString = self.data.decode("utf-8")
                            strengthL, strengthR = readableString.split("|")

                            print("strengthL: " + strengthL + ", strengthR: " + strengthR)

                            self.targetSpeedFB = int(strengthL)
                            self.rotateStrength = int(strengthR)                        

                            #print("\n cycletime: " + str(float(float(time.process_time()) - float(start)))) #debug zeitmessung
                            
                            self.newData = True
                        else:
                            self.error = True
                    except Exception as e:
                        print("\nWifi Error: "+ str(e))
             
                        
class SEND_WIFI_MODULE(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True

        #VAR INIT
        self.smartphoneIP = 0
        self.SEND_PORT = 12348
        self.sendFlag = True
        self.msg = ""

        self.start()

        print("\nSendWifi initialized")

    def run(self):

        while True:

            time.sleep(1)

            if self.smartphoneIP != 0:

                if self.msg != "":

                    #prepare data:
                    data = bytearray(self.msg, "UTF-8")

                    #

                    if self.sendFlag:

                        self.sendFlag = False

                        try:
                            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                            sock.sendto(data, (self.Smartphone_IP, self.SEND_PORT))
                            #print("Msg: '"+str(self.msg)+"' send to: "+str(self.Smartphone_IP)+":"+str(self.SEND_PORT))
                            self.sendFlag = True

                        except Exception as e:
                                print("\nWifi Error: "+ str(e))
               
