class PID_Dominik(object):

    def __init__(self, Kp: float):

        # given Variables
        self.Kp = Kp

        self.TN_ms = 10.0
        self.TA_ms = 0.0
        # Variables init
        self.output = 0.0
        self.outputBefore = 0.0
        self.difference = 0.0
        self.differenceBefore = 0.0



        # measured
        # self.timeForARun = 0.00009

        # still has to be adjusted
        self.maxBuffer = 10000.0
        self.maxOutput = 100.0

        print("PID initialized")

    def pid(self, inputVar, setpoint, gyroCompensation: float, timeForARun: float):
        self.TA_ms = timeForARun

        self.c1 = self.Kp * (1 + (self.TA_ms / (2 * self.TN_ms)))
        self.c2 = self.Kp * (1 - (self.TA_ms / (2 * self.TN_ms)))


        self.compensatedInput = inputVar - gyroCompensation
        self.difference = setpoint - self.compensatedInput

        # main PID


        self.differenceBefore = self.difference

        self.output = self.outputBefore + self.c1 * self.difference - self.differenceBefore * self.c2

        self.outputBefore = self.output


        print("motor output = %f" % (self.output))

        #return int(round((self.output / self.maxOutput) * -15))
        return self.output