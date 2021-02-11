import serial
import time
import string
import pynmea2


class GPS(object):

    def __init__(self):

        port = "dev/ttyAMA0"
        self.ser = serial.Serial(port, baudrate=9600, timeout=0.5)
        self.lat = 0.0
        self.lng = 0.0

        print("GPS initialized")

    def gps(self):

        dataout = pynmea2.NMEAStreamReader()  # no idea what that is for
        newData = self.ser.readline()

        if newData[0:6] == "$GPRMC":
            newMessage = pynmea2.parse(newData)
            self.lat = newMessage.latitude
            self.lng = newMessage.longitude

    def get_latitude(self):
        return self.lat

    def get_longitude(self):
        return self.lng


temp = GPS()
while True:
    print(str(temp.get_latitude()) + ", " + str(temp.get_longitude()))