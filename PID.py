import time

currentTime = time.monotonic
# currentTime = time.time


class PID(object):

    def __init__(self, Kp: float, Ki: float, Kd: float, sampleTime=0.01, outputLimits=(None, None)):
        """
            Description
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

        if inputVar > abs(90):
            self.controlError = True
            return 0

        now = currentTime()

        dt = now - self.lastTime if now - self.lastTime else 1e-16

        if self.sampleTime is not None and dt < self.sampleTime and self.lastOutput is not None:
            # only update every sample_time seconds
            return self.lastOutput

        # compute error terms
        error = setpoint - inputVar
        d_input = inputVar - (self.lastInput if self.lastInput is not None else inputVar)
        self.proportional = self.Kp * error

        # compute integral and derivative terms
        #       self.integral = self.integral + self.Ki * error * dt  # M-Regler
        #       self.integral = self.clamp(self.integral, self.outputLimits)  # avoid integral windup
        self.integral = self.Ki * self.buffer  # L-Regler

        #       self.derivative = -self.Kd * d_input / dt  # M-Regler
        self.derivative = -(self.Kd*self.multiplier) * ((self.lastError - error) / dt)  # L-Regler
        self.lastError = error

        #       self.output = self.proportional + self.integral + self.derivative  # M-Regler
        self.output = self.proportional + self.integral + self.derivative + self.buffer2  # L-Regler

        self.buffer = (error - self.output) * dt + self.buffer
        self.buffer2 = self.derivative + self.buffer2 * 0.9999

        # keep track of state
        self.lastOutput = self.output
        self.lastInput = inputVar
        self.lastTime = now
        print (self.output)
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
