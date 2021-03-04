from ADS1x15 import ADS1015
import threading
import time

class ANALOG_DIGITAL_CONVERTER(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.adc = ADS1015()
        self.channel = 0
        self.gain = 1
        self.data = 0
        self.start()
        self.voltage = 0


    def run(self):
        while True:
            self.data = self.adc.read_adc(self.channel, self.gain)
            #1Bit=3mV
            self.voltage = 33000/((self.data/3)/1000*20000)

            time.sleep(0.1)