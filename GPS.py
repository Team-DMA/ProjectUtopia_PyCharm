import serial
import pynmea2
import threading

class GPS(threading.Thread):

    def __init__(self):

        threading.Thread.__init__(self)
        self.daemon = True

        port = "/dev/serial0"
        self.ser = serial.Serial(
            port='/dev/serial0',
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS)

        self.lat = 49.18249126495341
        self.lng = 8.542124178274259
        self.alt = 0.0
        self.latDir = "N"
        self.lngDir = "O"
        self.error = False
        print("GPS initialized")
        self.start()

    def run(self):
        """
        gets the current position
        """
        dataout = pynmea2.NMEAStreamReader()
        newData = self.ser.readline()
        newData = newData.decode("utf-8")

        if newData.find("GPGGA"):
            print(newData)
            newMessage = pynmea2.parse(newData)
            self.lat = newMessage.lat
            self.lng = newMessage.lon
            self.alt = newMessage.altitude
            self.error = False
        else:
            self.error = True

    def get_latitude(self):
        return self.lat

    def get_longitude(self):
        return self.lng

    def get_altitude(self):
        return self.alt


