from MotorControl import MOTOR_CONTROL
from PID import PID

# graph
import time
import matplotlib.pyplot as plt
import pandas as pd


def scale(old_value, old_min, old_max, new_min, new_max):
    new_value = ((old_value - old_min) / (old_max - old_min)) * (new_max - new_min) + new_min
    return new_value


# graph
setpoint = 0.0
pidDataList = [setpoint]
timeDataList = [0.0]
gyroDataList = [setpoint]
startTime = time.time()


class PID_CONTROL(object):

    def __init__(self, MotorControlClass: MOTOR_CONTROL, Kp, Ki, Kd):

        # given variables
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd

        # variables initialization
        self.speedLeft = 0
        self.speedRight = 0
        self.i = 10

        # given Classes
        self.PID_CLASS = PID(self.Kp, self.Ki, self.Kd, None)
        self.MOTOR_CONTROL_CLASS = MotorControlClass

        # debug:
        print("Kp = {0}".format(self.Kp))
        print("Ki = {0}".format(self.Ki))
        print("Kd = {0}".format(self.Kd))
        print("PID_CONTROL initialized")

    def __del__(self):
        try:
            # data
            columns = ["Time", "ControlValue", "Rotation"]
            rows = zip(timeDataList, pidDataList, gyroDataList)

            # combine rows and column names into pandas dataframe
            data = pd.DataFrame(rows, columns=columns)

            data.plot(x="Time", y=["ControlValue", "Rotation"])
            #plt.show(block=False)

            plt.xlabel("Zeit in s")
            plt.title("Regler macht brrrrr")

            plt.savefig('graph_pid.png', bbox_inches='tight')

            print("\nImage generated. Exiting...")

        except Exception as e:
            print("\nError while plotting: " + str(e))

    def motor_adjust(self, rotation, speed, turn):

        # ich weiß nicht, ob das funktioniert, gegebenenfalls muss auch noch turn miteinbezogen werden
        # Der veränderte Sollwert soll dafür sorgen, das sich die Drohne nach vorne/hinten kippt, wenn man speed
        # verwendet.
        # vielleicht würde es auch reichen, den Speed nur über den Sollwert für den Regler zu steuern, da er dadurch
        # automatisch nach vorne/hinten fährt.
        #setpoint = speed * 2
        setpoint = 0

        changedValue = self.PID_CLASS(rotation, setpoint)  # PID_CLASS.pid gibt Ausgang zurück
        # changedValue = -(int(round(scale(changedValue, -75, 75, -15, 15))))  # scale, round, to int and minus
        changedValue = (int(round(changedValue)))

        # graph
        now = time.time() - startTime
        gyroDataList.append(rotation)
        pidDataList.append(changedValue)
        timeDataList.append(now)

        return changedValue

    def selfrighting(self, rotation, gyroCompensation: float):

        print("self righting")

        if self.i != 0:
            self.MOTOR_CONTROL_CLASS.set_speed(-15)
            self.i = self.i - 1

        if abs(rotation - gyroCompensation) > 40:
            self.MOTOR_CONTROL_CLASS.set_speed(15)

        if abs(rotation - gyroCompensation) < 45:
            self.PID_CLASS.controlError = False
            self.i = 10

    def control(self, rotation, speed: int, turn: int):

        # if(self.PID_CLASS.controlError == False):
        # print("speed: %d" % speed)
        if turn < 0 and speed > 0:
            self.speedLeft = max(0, speed + turn)
            self.speedRight = speed
        elif turn > 0 and speed > 0:
            self.speedRight = max(0, speed - turn)
            self.speedLeft = speed
        elif turn < 0 and speed < 0:
            self.speedLeft = -max(0, abs(speed - turn))
            self.speedRight = speed
        elif turn > 0 and speed < 0:
            self.speedRight = -max(0, abs(speed + turn))
            self.speedLeft = speed
        elif speed == 0 and turn != 0:
            self.speedLeft = turn
            self.speedRight = -turn
        elif turn == 0 and speed != 0:
            self.speedLeft = speed
            self.speedRight = speed
        else:
            self.speedLeft = 0
            self.speedRight = 0

        motorAdj = self.motor_adjust(rotation, speed, turn)
        # motoranpassung = 0
        # print("speedLeft %d" % (self.speedLeft + motorAdj))
        # print("speedRight %d" % (self.speedRight + motorAdj))

        print("Rotation: " + str(rotation) + ", PID-Output: " + str(motorAdj))

        self.MOTOR_CONTROL_CLASS.set_speed_left(self.speedLeft + motorAdj)
        self.MOTOR_CONTROL_CLASS.set_speed_right(self.speedRight + motorAdj)

        # else:
        #   self.selfrighting(rotation, gyroCompensation)
