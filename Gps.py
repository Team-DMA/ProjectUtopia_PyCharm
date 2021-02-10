import serial
import time
import string
import pynmea2


class GPS(object):

    def __init__(self):

        port = "/dev/ttyAMA0"
        ser = serial.Serial(port, baudrate=9600, timeout=0.5)
        self.lat = 0.0
        self.lng = 0.0

        print("GPS intilized")

    def gps(self):

        dataout = pynmea2.NMEAStreamReader() #no idea what that is for
        newData = ser.readline()

        if newData[0:6] == "$GPRMC":
            newMessage = pynmea2.parse(newData)
            self.lat = newMessage.latitude
            self.lng = newMessage.longitude
            #gps = "Latitude=" + str(self.lat) + "and Longitude=" + str(self.lng)
            #print(gps)

    def get_latitude(self):
        return self.lat

    def get_longitude(self):
        return self.lng