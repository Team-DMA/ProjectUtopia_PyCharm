from Echo import ECHO
from Gyro import GYRO
from PidControl import PID_CONTROL


class SELF_DRIVING(object):

    def __init__(self, GyroClass: GYRO, EchoClass: ECHO, PidClass: PID_CONTROL):

        # given Classes
        self.ECHO_CLASS = EchoClass
        self.PID_CONTROL_CLASS = PidClass
        self.GYRO_CLASS = GyroClass

    def detect(self):

        if self.ECHO_CLASS.distance < 40:
            return True
        else:
            return False

    def drive(self):

        if not self.detect():
            self.PID_CONTROL_CLASS.control(self.GYRO_CLASS.yRotation, 5, 0)
        else:
            self.PID_CONTROL_CLASS.control(self.GYRO_CLASS.yRotation, 1, 1)
