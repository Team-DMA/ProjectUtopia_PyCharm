class PID(object):

    def __init__(self, Kp: float, Ki: float, Kd: float):

        # given Variables
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd

        # Variables init
        self.output = 0.0
        self.buffer = 0.0
        self.difference = 0.0
        self.differenceBefore = 0.0
        self.controlError = False

        # measured
        # self.timeForARun = 0.00009

        # still has to be adjusted
        self.maxBuffer = 100.0
        self.maxOutput = 50.0

        print("PID initialized")

    def pid(self, inputVar, setpoint, gyroCompensation: float, timeForARun: float):

        compensatedInput = inputVar - gyroCompensation
        self.difference = setpoint - self.output
        self.buffer = self.difference * timeForARun + self.buffer

        # main PID
        self.output = compensatedInput + self.output + self.Kp * self.difference + self.Ki * self.buffer + self.Kd * \
                      ((self.differenceBefore - self.difference) / timeForARun)

        self.differenceBefore = self.difference

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

        print("motor output = %f" % int(round((self.output / self.maxOutput) * -15)))

        return int(round((self.output / self.maxOutput) * -15))
