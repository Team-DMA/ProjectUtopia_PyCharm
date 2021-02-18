import serial
import time
import string
import pynmea2


class GPS(object):

    def __init__(self):

        port = "/dev/serial0"
        self.ser = serial.Serial(
            port='/dev/serial0',
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS)

        self.lat = 0.0
        self.lng = 0.0
        self.alt = 0.0
        self.error = False
        print("GPS initialized")

    def gps(self):

        dataout = pynmea2.NMEAStreamReader()  # no idea what that is for
        # newData = str(self.ser.readline())
        newData = self.ser.readline()
        newData = newData.decode("utf-8")

        # if newData[3] == "G" and newData[4] == "P" and newData[5] == "G" and newData[6] == "L" and newData[7] == "L":
        if newData.find("GPGLL"):
            print(newData)
            # newData = newData.replace("b'", "")
            # newData = newData.replace("\\r\\n'", "")
            # newData = newData.replace("\\n", "")
            # newData = newData.replace("'", "")
            newMessage = pynmea2.parse(newData)
            self.lat = newMessage.latitude
            self.lng = newMessage.longitude
            # self.alt = newMessage.altitude
            self.Error = False
        else:
            self.Error = True
        # print("Waiting for GPS...")

        return self.lat, self.lng, self.alt

    def get_latitude(self):
        return self.lat

    def get_longitude(self):
        return self.lng


def generate_lines_that_equal(string, fp):
    for line in fp:
        if line == string:
            yield line


temp = GPS()
while True:
    x, y, alt = temp.gps()
    if temp.Error == False:
        print(str(x) + ", " + str(y) + ", Alt: " + str(alt))
    # time.sleep(0.1)
