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
        self.datei = open('/dev/serial0', 'r')
        print("GPS initialized")

    def gps(self):

        dataout = pynmea2.NMEAStreamReader()  # no idea what that is for
        newData = str(self.ser.readline())
        #print(str(newData))
        # if "$GPGLL" in str(newData):
        #    print(str(newData))

        #numb = input('GPGLL,')
        #for lines in newData:
        #    if numb == lines[0]:
        #        print(newData)
            #Norden, tmp4, Osten, tmp5 = tmp2.split(",")
            #print("N: %d" % Norden + ", E: %d" % Osten)
        #if newData.find('GPGLL'):
        #    print("juhu")
        print("0: "+ newData[0]+"1: "+ newData[1]+"2: "+ newData[2]+"3: "+ newData[3]+"4: "+ newData[4]+"5: "+ newData[5]+"6: "+ newData[6]+"7: "+ newData[7]+"8: "+ newData[8])
        if newData[3:7] == "GPGLL":
            print("juhu2")
        #if newData[0:8] == "b'$GPGLL":
        #    print("juhu3")
        #if newData[0:2] == "b'":
        #    print("juhu4")
        #  newMessage = pynmea2.parse(newData)
        # self.lat = newMessage.latitude
        # self.lng = newMessage.longitude

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
    temp.gps()
    # print(str(temp.get_latitude()) + ", " + str(temp.get_longitude()))
    # time.sleep(0.1)
