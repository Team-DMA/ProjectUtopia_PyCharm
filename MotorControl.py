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

        self.pwmL = GPIO.PWM(enPinL, 1000000)
        #it has to be tested, if a higher or a lower frequencie performes better
        self.pwmR = GPIO.PWM(enPinR, 1000000)
        self.pwmL.start(0)
        self.pwmR.start(0)
        self.pwmL.ChangeDutyCycle(0)
        self.pwmR.ChangeDutyCycle(0)
        print("motor control initialized")

    def set_speed_left(self, speed: int):

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
            self.pwmL.ChangeDutyCycle(25 + 5 * forceL)
        else:
            self.pwmL.ChangeDutyCycle(0)

    def set_speed_right(self, speed: int):

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
            self.pwmR.ChangeDutyCycle(25 + 5 * forceR)
        else:
            self.pwmR.ChangeDutyCycle(0)

    def set_speed(self, speed: int):

        self.set_speed_left(speed)
        self.set_speed_right(speed)
        # print("speed: %f" % speed)

    def turn_left(self, speed: int):

        self.set_speed_left(0)
        self.set_speed_right(speed)
        print("turn left")

    def turn_right(self, speed: int):

        self.set_speed_right(0)
        self.set_speed_left(speed)
        print("turn right")

    def forward(self, speed: int):

        if speed > 0:
            self.set_speed(speed)
            print("Forwards")

    def backward(self, speed: int):

        if speed < 0:
            self.set_speed(speed)
            print("Backwards")

    def stop(self):

        self.set_speed(0)
