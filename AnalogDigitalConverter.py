from ADS1x15 import ADS1015
import threading
import time

batteryEmpty = 10
batteryFull = 13

def scale(old_value, old_min, old_max, new_min, new_max):
    new_value = ((old_value - old_min) / (old_max - old_min)) * (new_max - new_min) + new_min
    return new_value


def clamp(value, minOut, maxOut):
    if value > maxOut:
        return maxOut
    elif value < minOut:
        return minOut

    return value


class ANALOG_DIGITAL_CONVERTER(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.adc = ADS1015()
        self.channel = 0
        self.gain = 1
        self.data = 0
        self.voltage = 0
        self.percentage = 0
        self.start()

    def run(self):
        while True:
            self.data = self.adc.read_adc(self.channel, self.gain)
            # 1Bit=3mV
            self.voltage = self.data / 155
            self.percentage = scale(self.voltage, batteryEmpty, batteryFull, 0, 100)
            self.percentage = clamp(self.percentage, 0, 100)
            time.sleep(0.1)

            print("Voltage: " + str(self.voltage) + ", Percentage: " + str(self.percentage))


tmp = ANALOG_DIGITAL_CONVERTER()

while True:
    pass
