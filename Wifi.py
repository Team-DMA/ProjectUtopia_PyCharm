import socket
import threading
import time
import sys

# for sending msgs
from gps_richtig import GPS
from Barometer import BAROMETER
from Compass import COMPASS
from AnalogDigitalConverter import ANALOG_DIGITAL_CONVERTER


class RCV_WIFI_MODULE(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True

        # VAR INIT
        self.udpIp = ""
        self.udpPort = 12345
        self.pingPort = 12346
        self.smartphoneIp = 0
        self.ip = 0
        self.port = 0
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

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.udpIp, self.udpPort))

        self.start()

        print("\nRcvWifi initialized")

    def run(self):

        # global newData
        # newData = False

        print("\nOwn IP: " + str(socket.gethostbyname(socket.gethostname() + ".local")))

        print("\nWaiting for Dominik...")
        while True:

            if not self.newData:

                # start = float(time.process_time()) #debug time measurement

                self.data, (self.ip, self.port) = self.sock.recvfrom(1024)  # buffer size is 1024 bytes
                self.smartphoneIp = self.ip  # set Smartphone IP

                if self.data is not None:
                    length = len(self.data)

                    try:

                        if self.data.decode("utf-8").count("|") == 3:
                            print("\nConnection initialization: send {0} Bytes back to {1}:{2}".format(length, self.ip,
                                                                                                       self.pingPort))

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

                            # print("strengthL: " + strengthL + ", strengthR: " + strengthR)

                            self.targetSpeedFB = int(strengthL)
                            self.rotateStrength = int(strengthR)

                            # print("\n cycle time: " + str(float(float(time.process_time()) - float(start))))
                            # debug cycle time

                            self.newData = True
                        else:
                            self.error = True
                    except Exception as e:
                        print("\nWifi Error: " + str(e))


class SEND_WIFI_MODULE(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True

        # VAR INIT
        self.smartphoneIp = None
        self.sendPort = 12348
        self.sendFlag = True
        self.msg = ""

        self.GPS_CLASS = GPS()
        self.COMPASS_CLASS = COMPASS()
        self.BAROMETER_CLASS = BAROMETER()
        self.ANALOG_DIGITAL_CONVERTER_CLASS = ANALOG_DIGITAL_CONVERTER()

        self.start()

        print("\nSendWifi initialized")

    def run(self):

        while True:

            time.sleep(1)

            if self.smartphoneIp is not None:

                try:
                    # prepare data:
                    self.msg = str(self.COMPASS_CLASS.compass()) + "|" + \
                               str(self.BAROMETER_CLASS.get_temperature()) + "|" + \
                               str(self.BAROMETER_CLASS.get_altitude()) + "|" + \
                               str(self.BAROMETER_CLASS.get_pressure()) + "|" + \
                               str(self.GPS_CLASS.get_longitude_direction()) + "|" + \
                               str(self.GPS_CLASS.get_longitude()) + "|" + \
                               str(self.GPS_CLASS.get_latitude_direction()) + "|" + \
                               str(self.GPS_CLASS.get_longitude()) + "|" + \
                               str(self.GPS_CLASS.get_altitude()) + "|" + \
                               str(self.ANALOG_DIGITAL_CONVERTER_CLASS.percentage)

                except Exception as e:
                    trace_back = sys.exc_info()[2]
                    line = trace_back.tb_lineno
                    self.msg = "0|0|0|0|0|0|0|0|0|0"
                    print("Data formatting Error in line " + str(line) + ": " + str(e))

                data = bytearray(self.msg, "UTF-8")
                #

                if self.sendFlag:

                    self.sendFlag = False

                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        sock.sendto(data, (self.smartphoneIp, self.sendPort))
                        print("Msg: '" + str(self.msg) + "' send to: " + str(self.smartphoneIp) + ":" + str(
                            self.sendPort))
                        self.sendFlag = True

                    except Exception as e:
                        print("\nWifi Error: " + str(e))
