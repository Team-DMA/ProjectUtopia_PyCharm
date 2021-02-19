class PID_Lukas(object):

    def __init__(self, Kp: float, Ki: float, Kd: float):

        # given Variables
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.KdT = 0.9998

        # Variables init
        self.pValue = 0.0
        self.iValue = 0.0
        self.dValue = 0.0
        self.output = 0.0
        self.buffer = 0.0
        self.buffer2 = 0.0
        self.difference = 0.0
        self.differenceBefore = 0.0
        self.controlError = False
        self.compensatedInput = 0.0


        # measured
        # self.timeForARun = 0.00009

        # still has to be adjusted
        self.maxBuffer = 10000.0
        self.maxOutput = 100.0

        print("PID initialized")

    def pid(self, inputVar, setpoint, gyroCompensation: float, timeForARun: float):

        self.compensatedInput = inputVar - gyroCompensation
        self.difference = setpoint - self.compensatedInput

        # main PID

        self.pValue = self.Kp * self.difference
        self.iValue = self.Ki * self.buffer
        self.dValue = -self.Kd * ((self.differenceBefore - self.difference) / timeForARun)
        self.differenceBefore = self.difference

        self.output = self.pValue + self.iValue + self.dValue + self.buffer2

        self.buffer = (self.difference - self.output) * timeForARun + self.buffer
        self.buffer2 = self.dValue + self.buffer2 * self.KdT


        """
        # Catch of extreme values
        if self.buffer > self.maxBuffer:
            self.buffer = self.maxBuffer

        if self.buffer < -self.maxBuffer:
            self.buffer = -self.maxBuffer

        if self.output > self.maxOutput:
            self.output = self.maxOutput
            self.controlError = True
            self.output = 0.0
            self.buffer = 0.0
            self.difference = 0.0
            self.differenceBefore = 0.0

        if self.output < -self.maxOutput:
            self.output = -self.maxOutput
            self.controlError = True
            self.output = 0.0
            self.buffer = 0.0
            self.difference = 0.0
            self.differenceBefore = 0.0
        """
        print("motor output = %f" % (self.output))

        #return int(round((self.output / self.maxOutput) * -15))
        return -self.output