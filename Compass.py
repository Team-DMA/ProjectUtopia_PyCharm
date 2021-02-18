import math
import smbus

class COMPASS(object):
    def __init__(self):
        # Get I2C bus
        self.bus = smbus.SMBus(1)
        self.address = 0x1E
        # HMC5883 address, 0x1E
        self.bus.write_byte_data(self.address, 0x00, 0x60)
        self.bus.write_byte_data(self.address, 0x02, 0x00)
        # self.hmc5883l = i2c_QMC5883L.QMC5883L(output_range=i2c_QMC5883L.RNG_8G)  # if not the first I2C Device, the 1 has to be changed

    def compass(self):
        # HMC5883 address, 0x1E and Read data
        data = self.bus.read_i2c_block_data(self.address, 0x03, 6)

        # Convert the data
        xMag = data[0] * 256 + data[1]
        if xMag > 32767:
            xMag -= 65536
        xMag = (xMag + 1048)/4

        zMag = data[2] * 256 + data[3]
        if zMag > 32767:
            zMag -= 65536

        yMag = data[4] * 256 + data[5]
        if yMag > 32767:
            yMag -= 65536
        yMag = yMag + 1148

        [x, y] = [xMag, yMag]
        print("X-Axis : %d" % xMag + ", Y-Axis : %d" % yMag + ", Z-Axis : %d" % zMag)
        if x is None or y is None:
            return None
        else:
            orientation = math.degrees(math.atan2(y, x))
            if orientation < 0:
                orientation += 360.0
            orientation += 2.91666667 # magnetic Correction
            if orientation < 0.0:
                orientation += 360.0
            elif orientation >= 360.0:
                orientation -= 360.0
        return orientation
        # Output data to screen

        # tmp123 = self.hmc5883l.get_magnet()
        # return tmp123

    # temp1 = BAROMETER()
temp2 = COMPASS()
while True:
    #    print(str(temp1.Temperature()))
    #    print(str(temp1.Pressure()))
    #    print(str(temp1.Altitude()))
    print(str(temp2.Compass()))
    time.sleep(0.2)
