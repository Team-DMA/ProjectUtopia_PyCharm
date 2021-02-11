import time

import smbus
from i2clibraries import i2c_hmc5883l


# HP206C address, 0x76(118)
# Read data back from 0x10(16), 6 bytes
# cTemp MSB, cTemp CSB, cTemp LSB, pressure MSB, pressure CSB, pressure LSB


class BAROMETER(object):

    def __init__(self):

        # Get I2C bus
        self.bus = smbus.SMBus(1)

        # HP206C address, 0x76(118)
        self.cTemp = 0
        self.pressure = 0
        self.altitude = 0

    def gettemp(self):    

        # Send OSR and channel setting command, 0x44(68)
        self.bus.write_byte(0x76, 0x44 | 0x00)
        time.sleep(0.1)
        data = self.bus.read_i2c_block_data(0x76, 0x10, 6)

        # Convert the data to 20-bits
        self.cTemp = (((data[0] & 0x0F) * 65536) + (data[1] * 256) + data[2]) / 100.00
        self.pressure = (((data[3] & 0x0F) * 65536) + (data[4] * 256) + data[5]) / 100.00
    
    def getaltitude(self):

        # HP206C address, 0x76(118)
        # Send OSR and channel setting command, 0x44(68)
        self.bus.write_byte(0x76, 0x44 | 0x01)

        time.sleep(0.1)

        # HP206C address, 0x76(118)
        # Read data back from 0x31(49), 3 bytes
        # altitude MSB, altitude CSB, altitude LSB
        data = self.bus.read_i2c_block_data(0x76, 0x31, 3)

        # Convert the data to 20-bits
        self.altitude = (((data[0] & 0x0F) * 65536) + (data[1] * 256) + data[2]) / 100.00
  
    def Temperature(self):

        self.gettemp()
        return self.cTemp

    def Pressure(self):

        self.gettemp()
        return self.pressure

    def Altitude(self):

        self.getaltitude()
        return self.altitude


class COMPASS(object):
    def __init__(self):
     
        self.hmc5883l = i2c_hmc5883l.i2c_hmc5883l(1)  # if not the first I2C Device, the 1 has to be changed

        self.hmc5883l.setContinuousMode()
        self.hmc5883l.setDeclination(2, 15)

    def Compass(self):

        return self.hmc58831


temp1 = BAROMETER()
temp2 = COMPASS()
while True:
    print(str(temp1.Temperature()))
    print(str(temp1.Pressure()))
    print(str(temp1.Altitude()))
    print(str(temp2.Compass()))
    time.sleep(0.2)