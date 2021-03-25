import time

currentTime = time.monotonic
# currentTime = time.time


class PID(object):

    def __init__(self, Kp: float, Ki: float, Kd: float, sampleTime=0.01, outputLimits=(None, None)):
        """
        constructor of PID controller
        :param Kp: proportional value
        :param Ki: integral value
        :param Kd: derivative value
        :param sampleTime: sample time or no sample time
        :param outputLimits: output limits or no output limits
        """

        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.sampleTime = sampleTime

        if self.sampleTime is None:
            self.multiplier = 1 / 1e+15
        else:
            self.multiplier = 1

        self.minOutput, self.maxOutput = outputLimits

        self.controlError = False

        self.reset()

    def __call__(self, inputVar, setpoint=0.0):
        """
        calculates the PID output
        :param inputVar: input value
        :param setpoint: setpoint
        :return: PID output
        """

        if inputVar > abs(90):
            self.controlError = True
            return 0

        now = currentTime()

        dt = now - self.lastTime if now - self.lastTime else 0.00009

        if self.sampleTime is not None and dt < self.sampleTime and self.lastOutput is not None:
            # only update every sample_time seconds
            return self.lastOutput
        # compute error terms
        error = setpoint - inputVar
        d_input = inputVar - (self.lastInput if self.lastInput is not None else inputVar)
        self.proportional = self.Kp * error

        # compute integral and derivative terms
        self.integral = self.integral + self.Ki * error * dt
        if abs(self.output) > abs(inputVar):
            self.integral = self.integral * 0.9
        self.integral = self.clamp(self.integral, self.outputLimits)  # avoid integral windup

        self.derivative = -(self.Kd*0.01) * ((self.lastError - error) / dt)
        self.lastError = error

        self.output = self.proportional + self.integral + self.derivative + self.buffer2

        self.output = self.clamp(self.output, self.outputLimits)
        self.buffer2 = self.derivative + self.buffer2 * 0.9

        # keep track of state
        self.lastOutput = self.output
        self.lastInput = inputVar
        self.lastTime = now
        return self.output

    def clamp(self, value, limits):
        lower, upper = limits
        if value is None:
            return None
        elif upper is not None and value > upper:
            return upper
        elif lower is not None and value < lower:
            return lower

        return value

    def reset(self):
        """
        Reset the PID controller internals, setting each term to 0 as well as cleaning the integral,
        the last output and the last input (derivative calculation).
        """
        self.proportional = 0.0
        self.integral = 0.0
        self.derivative = 0.0

        self.lastTime = currentTime()
        self.lastOutput = None
        self.lastInput = None

        self.lastError = 0.0
        self.buffer = 0.0
        self.buffer2 = 0.0
        self.output = 0.0

    @property
    def outputLimits(self):
        return self.minOutput, self.maxOutput

    @outputLimits.setter
    def outputLimits(self, limits):
        """Setter for the output limits"""
        if limits is None:
            self.minOutput, self.maxOutput = None, None
            return

        minOutput, maxOutput = limits

        if None not in limits and maxOutput < minOutput:
            raise ValueError('lower limit must be less than upper limit')

        self.minOutput = minOutput
        self.maxOutput = maxOutput

        self.integral = self.clamp(self.integral, self.outputLimits)
        self.lastOutput = self.clamp(self.lastOutput, self.outputLimits)
