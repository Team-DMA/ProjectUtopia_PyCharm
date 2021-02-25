import time




class PID_Dominik(object):

    def __init__(self, Kp: float, sampleTime):

        # given Variables
        self.Kp = Kp

        self.TN_ms = 15.0
        # Variables init
        self.output = 0.0
        self.outputBefore = 0.0
        self.difference = 0.0
        self.differenceBefore = 0.0
        self.TA_ms = sampleTime

        self.c1 = self.Kp * (1 + (self.TA_ms / (2 * self.TN_ms)))
        self.c2 = self.Kp * (1 - (self.TA_ms / (2 * self.TN_ms)))
        # measured
        # self.timeForARun = 0.00009

        # still has to be adjusted
        self.maxBuffer = 10000.0
        self.maxOutput = 100.0

        print("PID initialized")

    def pid(self, inputVar, setpoint):






        self.difference = setpoint - inputVar

        # main PID




        self.output = -inputVar + self.c1 * self.difference - self.differenceBefore * self.c2

        self.outputBefore = self.output
        self.differenceBefore = self.difference


        print("motor output = %f" % (self.output))

        #return int(round((self.output / self.maxOutput) * -15))
        return self.output