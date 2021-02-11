import time
import math
import smbus
import i2c_QMC5883L


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
        # Get I2C bus
        self.bus = smbus.SMBus(1)

        # HMC5883 address, 0x1E
        self.bus.write_byte_data(0x1E, 0x00, 0x60)
        self.bus.write_byte_data(0x1E, 0x02, 0x00)
        # self.hmc5883l = i2c_QMC5883L.QMC5883L(output_range=i2c_QMC5883L.RNG_8G)  # if not the first I2C Device, the 1 has to be changed

    def Compass(self):
        # HMC5883 address, 0x1E and Read data
        data = self.bus.read_i2c_block_data(0x1E, 0x03, 6)

        # Convert the data
        xMag = data[0] * 256 + data[1]
        if xMag > 32767:
            xMag -= 65536

        zMag = data[2] * 256 + data[3]
        if zMag > 32767:
            zMag -= 65536

        yMag = data[4] * 256 + data[5]
        if yMag > 32767:
            yMag -= 65536

        [x, y] = [xMag + 1048, yMag + 2048]

        if x is None or y is None:
            return None
        else:
            b = math.degrees(math.atan2(y, x))
            if b < 0:
                b += 360.0
            b += 2.91666667
            if b < 0.0:
                b += 360.0
            elif b >= 360.0:
                b -= 360.0
        return b
        # Output data to screen
        # print("X-Axis : %d" % xMag + ", Y-Axis : %d" % yMag + ", Z-Axis : %d" % zMag)
        # tmp123 = self.hmc5883l.get_magnet()
        # return tmp123


temp1 = BAROMETER()
temp2 = COMPASS()
while True:
    print(str(temp1.Temperature()))
    print(str(temp1.Pressure()))
    print(str(temp1.Altitude()))
    print(str(temp2.Compass()))
    time.sleep(0.2)
