import math
import smbus


#debug

class GYRO(object):

    def __init__(self):

        #Register
        self.power_mgmt_1 = 0x6b

        self.bus = smbus.SMBus(1) # bus = smbus.SMBus(0) fuer Revision 1
        
        self.address = 0x68       # via i2cdetect, Addresse rausfinden!
        self.bus.write_byte_data(self.address, 0x19, 7)
        
        # Aktivieren, um das Modul ansprechen zu koennen
        self.bus.write_byte_data(self.address, self.power_mgmt_1, 1)
        self.bus.write_byte_data(self.address, 0x1A, 0)
        self.bus.write_byte_data(self.address, 0x1B, 24)
        self.bus.write_byte_data(self.address, 0x38, 1)
        
        self.gyroskop_x = 0
        self.gyroskop_y = 0
        self.gyroskop_z = 0
        self.gyroskop_x_skaliert = 0
        self.gyroskop_y_skaliert = 0
        self.gyroskop_z_skaliert = 0
        self.beschleunigung_x = 0
        self.beschleunigung_y = 0
        self.beschleunigung_z = 0
        self.beschleunigung_x_skaliert = 0
        self.beschleunigung_y_skaliert = 0
        self.beschleunigung_z_skaliert = 0
        self.x_rotation = 0
        self.y_rotation = 0
        print("Gyroskop iniziiert")


    #Methoden
    def read_byte(self,reg):

        return self.bus.read_byte_data(self.address, reg)
     

    def read_word(self,reg):

        h = self.bus.read_byte_data(self.address, reg)
        l = self.bus.read_byte_data(self.address, reg+1)
        value = (h << 8) + l
        return value
     

    def read_word_2c(self,reg):

        val = self.read_word(reg)
        if (val >= 0x8000):
            return -((65535 - val) + 1)
        else:
            return val
     

    def dist(self,a,b):

        return math.sqrt((a*a)+(b*b))
     

    def get_y_rotation(self,x,y,z):

        radians = math.atan2(x, self.dist(y,z))
        return -math.degrees(radians)
     

    def get_x_rotation(self,x,y,z):

        radians = math.atan2(y, self.dist(x,z))
        return math.degrees(radians)


    def read_gyro(self):
        
        #self.gyroskop_x = self.read_word_2c(0x43)
        #self.gyroskop_y = self.read_word_2c(0x45)
        #self.gyroskop_z = self.read_word_2c(0x47)

        #self.gyroskop_x_skaliert = self.gyroskop_x / 131
        #self.gyroskop_y_skaliert = self.gyroskop_y / 131
        #self.gyroskop_z_skaliert = self.gyroskop_z / 131

        self.beschleunigung_x = self.read_word_2c(0x3b)
        self.beschleunigung_y = self.read_word_2c(0x3d)
        self.beschleunigung_z = self.read_word_2c(0x3f)
     
        self.beschleunigung_x_skaliert = self.beschleunigung_x / 16384.0
        self.beschleunigung_y_skaliert = self.beschleunigung_y / 16384.0
        self.beschleunigung_z_skaliert = self.beschleunigung_z / 16384.0

        self.x_rotation = self.get_x_rotation(self.beschleunigung_x_skaliert, self.beschleunigung_y_skaliert, self.beschleunigung_z_skaliert)
        self.y_rotation = self.get_y_rotation(self.beschleunigung_x_skaliert, self.beschleunigung_y_skaliert, self.beschleunigung_z_skaliert)
        
        #print("gyroskop_x = %f" % self.gyroskop_x)
        #print("gyroskop_y = %f" % self.gyroskop_y)
        #print("gyroskop_z = %f" % self.gyroskop_z)
        #print("gyroskop_x_skaliert = %f" % self.gyroskop_x_skaliert)
        #print("gyroskop_y_skaliert = %f" % self.gyroskop_y_skaliert)
        #print("gyroskop_z_skaliert = %f" % self.gyroskop_z_skaliert)
        #print("beschleunigung_x = %f" % self.beschleunigung_x)
        #print("beschleunigung_y = %f" % self.beschleunigung_x)
        #print("beschleunigung_z = %f" % self.beschleunigung_x)
        #print("beschleunigung_x_skaliert = %f" % self.beschleunigung_x_skaliert)
        #print("beschleunigung_y_skaliert = %f" % self.beschleunigung_x_skaliert)
        #print("beschleunigung_z_skaliert = %f" % self.beschleunigung_x_skaliert)
        print("x_rotation = %f" % self.x_rotation)
        print("y_rotation = %f" % self.y_rotation)
    

