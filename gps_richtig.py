import serial
import time
import string
import pynmea2


class GPS(object):

    def __init__(self):

        port = "/dev/serial0"
        self.ser = serial.Serial(
           port = '/dev/serial0',
           baudrate = 9600,
           parity=serial.PARITY_NONE,
           stopbits=serial.STOPBITS_ONE,
           bytesize=serial.EIGHTBITS)

        self.lat = 0.0
        self.lng = 0.0
        self.datei = open('/dev/serial0','r')
        print("GPS initialized")

    def gps(self):

        dataout = pynmea2.NMEAStreamReader()  # no idea what that is for
        newData = self.ser.readline()
        #print(str(newData))
        if "$GPGLL" in newData:
            print(str(newData))
        #if newData[2:7] == "$GPRMC":
         #   print(newData)
          #  newMessage = pynmea2.parse(newData)
           # self.lat = newMessage.latitude
            #self.lng = newMessage.longitude

    def get_latitude(self):
        return self.lat

    def get_longitude(self):
        return self.lng


temp = GPS()
while True:
    temp.gps()
    #print(str(temp.get_latitude()) + ", " + str(temp.get_longitude()))
    #time.sleep(0.1)