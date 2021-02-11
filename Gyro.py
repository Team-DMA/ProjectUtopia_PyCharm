import math
import smbus
# debug
import time


# debug

class GYRO(object):

    def __init__(self):

        # Register
        self.power_mgmt_1 = 0x6b

        self.bus = smbus.SMBus(1)  # bus = smbus.SMBus(0) for Revision 1

        self.address = 0x68  # via i2c detect, address research!
        self.bus.write_byte_data(self.address, 0x19, 7)

        # activate to communicate with the module
        self.bus.write_byte_data(self.address, self.power_mgmt_1, 1)
        self.bus.write_byte_data(self.address, 0x1A, 0)
        self.bus.write_byte_data(self.address, 0x1B, 24)
        self.bus.write_byte_data(self.address, 0x38, 1)

        self.gyroscopeX = 0
        self.gyroscopeY = 0
        self.gyroscopeZ = 0
        self.gyroscopeXScaled = 0
        self.gyroscopeYScaled = 0
        self.gyroscopeZScaled = 0
        self.accelerationX = 0
        self.accelerationY = 0
        self.accelerationZ = 0
        self.accelerationXScaled = 0
        self.accelerationYScaled = 0
        self.accelerationZScaled = 0
        self.xRotation = 0
        self.yRotation = 0
        print("gyroscope initialized")

    # Methods
    def read_byte(self, reg):

        return self.bus.read_byte_data(self.address, reg)

    def read_word(self, reg):

        h = self.bus.read_byte_data(self.address, reg)
        l = self.bus.read_byte_data(self.address, reg + 1)
        value = (h << 8) + l
        return value

    def read_word_2c(self, reg):

        val = self.read_word(reg)
        if val >= 0x8000:
            return -((65535 - val) + 1)
        else:
            return val

    def dist(self, a, b):

        return math.sqrt((a * a) + (b * b))

    def get_y_rotation(self, x, y, z):

        radians = math.atan2(x, self.dist(y, z))
        return -math.degrees(radians)

    def get_x_rotation(self, x, y, z):

        radians = math.atan2(y, self.dist(x, z))
        return math.degrees(radians)

    def read_gyro(self):

        self.gyroscopeX = self.read_word_2c(0x43)
        self.gyroscopeY = self.read_word_2c(0x45)
        self.gyroscopeZ = self.read_word_2c(0x47)

        self.gyroscopeXScaled = self.gyroscopeX / 131
        self.gyroscopeYScaled = self.gyroscopeY / 131
        self.gyroscopeZScaled = self.gyroscopeZ / 131

        self.accelerationX = self.read_word_2c(0x3b)
        self.accelerationY = self.read_word_2c(0x3d)
        self.accelerationZ = self.read_word_2c(0x3f)

        self.accelerationXScaled = self.accelerationX / 16384.0
        self.accelerationYScaled = self.accelerationY / 16384.0
        self.accelerationZScaled = self.accelerationZ / 16384.0

        self.xRotation = self.get_x_rotation(self.accelerationXScaled, self.accelerationYScaled,
                                             self.accelerationZScaled)
        self.yRotation = self.get_y_rotation(self.accelerationXScaled, self.accelerationYScaled,
                                             self.accelerationZScaled)

        print("gyroscopeX = %f" % self.gyroscopeX)
        print("gyroscopeY = %f" % self.gyroscopeY)
        print("gyroscopeZ = %f" % self.gyroscopeZ)
        print("gyroscopeXScaled = %f" % self.gyroscopeXScaled)
        print("gyroscopeYScaled = %f" % self.gyroscopeYScaled)
        print("gyroscopeZScaled = %f" % self.gyroscopeZScaled)
        print("accelerationX = %f" % self.accelerationX)
        print("accelerationY = %f" % self.accelerationY)
        print("accelerationZ = %f" % self.accelerationZ)
        print("accelerationXScaled = %f" % self.accelerationXScaled)
        print("accelerationYScaled = %f" % self.accelerationYScaled)
        print("accelerationZScaled = %f" % self.accelerationZScaled)
        print("xRotation = %f" % self.xRotation)
        print("yRotation = %f" % self.yRotation)


#temp = GYRO()
#while True:
#    temp.read_gyro()
#    time.sleep(0.2)
