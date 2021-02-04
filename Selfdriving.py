from Echo import ECHO
from Gyro import GYRO
from PidControl import PID_CONTROL


class SELFDRIVING(object):
  
    def __init__(self, GyroClass: GYRO, EchoClass: ECHO, PidClass: PID_CONTROL, gyroCompensation):
    
        #übergebene Variablen
        self.gyroCompensation = gyroCompensation  
        
        #übergebene Klassen
        self.ECHO_CLASS = EchoClass
        self.PID_CONTROL_CLASS = PidClass
        self.GYRO_CLASS = GyroClass



    def detect(self):

        if(self.ECHO_CLASS.distance < 40):
            return True
        else:
            return False
      

    def drive(self):

        if(self.detect() == False):
            self.PID_CONTROL_CLASS.control(self.GYRO_CLASS.x_rotation, 5, 0, self.gyroCompensation)
        else:
            self.PID_CONTROL_CLASS.control(self.GYRO_CLASS.x_rotation, 1, 1, self.gyroCompensation)
