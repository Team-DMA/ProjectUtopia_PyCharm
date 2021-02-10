import RPi.GPIO as GPIO


class MOTOR_CONTROL(object):

    def __init__(self, enPinL: int, enPinR: int, inForwardPinL: int, inBackwardPinL: int, inForwardPinR: int,
                 inBackwardPinR: int):

        self.inForwardPinL = inForwardPinL
        GPIO.setup(inForwardPinL, GPIO.OUT)
        GPIO.output(inForwardPinL, False)

        self.inBackwardPinL = inBackwardPinL
        GPIO.setup(inBackwardPinL, GPIO.OUT)
        GPIO.output(inBackwardPinL, False)

        GPIO.setup(enPinL, GPIO.OUT)

        self.inForwardPinR = inForwardPinR
        GPIO.setup(inForwardPinR, GPIO.OUT)
        GPIO.output(inForwardPinL, False)

        self.inBackwardPinR = inBackwardPinR
        GPIO.setup(inBackwardPinR, GPIO.OUT)
        GPIO.output(inBackwardPinR, False)

        GPIO.setup(enPinR, GPIO.OUT)

        self.pwmL = GPIO.PWM(enPinL, 100)
        self.pwmR = GPIO.PWM(enPinR, 100)
        self.pwmL.start(0)
        self.pwmR.start(0)
        self.pwmL.ChangeDutyCycle(0)
        self.pwmR.ChangeDutyCycle(0)
        print("motor control initialized")

    def setSpeedL(self, speed: int):

        """
            speed might be -15...+15
        """
        forceL = min(15, abs(speed))
        # print ("forceL %d" % forceL)

        if speed > 0:
            GPIO.output(self.inBackwardPinL, False)
            GPIO.output(self.inForwardPinL, True)
        elif speed < 0:
            GPIO.output(self.inForwardPinL, False)
            GPIO.output(self.inBackwardPinL, True)
        else:
            GPIO.output(self.inForwardPinL, False)
            GPIO.output(self.inBackwardPinL, False)

        if forceL > 0:
            self.pwmL.ChangeDutyCycle(10 + 6 * forceL)
        else:
            self.pwmL.ChangeDutyCycle(0)

    def setSpeedR(self, speed: int):

        """
            speed might be -15...+15
        """
        forceR = min(15, abs(speed))
        # print ("forceR %d" % forceR)

        if speed > 0:
            GPIO.output(self.inBackwardPinR, False)
            GPIO.output(self.inForwardPinR, True)
        elif speed < 0:
            GPIO.output(self.inForwardPinR, False)
            GPIO.output(self.inBackwardPinR, True)
        else:
            GPIO.output(self.inForwardPinR, False)
            GPIO.output(self.inBackwardPinR, False)

        if forceR > 0:
            self.pwmR.ChangeDutyCycle(10 + 6 * forceR)
        else:
            self.pwmR.ChangeDutyCycle(0)

    def setSpeed(self, speed: int):

        self.setSpeedL(speed)
        self.setSpeedR(speed)
        # print("speed: %f" % speed)

    def turnLeft(self, speed: int):

        self.setSpeedL(0)
        self.setSpeedR(speed)
        print("turn left")

    def turnRight(self, speed: int):

        self.setSpeedR(0)
        self.setSpeedL(speed)
        print("turn right")

    def forward(self, speed: int):

        if speed > 0:
            self.setSpeed(speed)
            print("Forwards")

    def backward(self, speed: int):

        if speed < 0:
            self.setSpeed(speed)
            print("Backwards")

    def stop(self):

        self.setSpeed(0)
