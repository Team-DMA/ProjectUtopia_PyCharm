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

        self.pwmL = GPIO.PWM(enPinL, 1000)
        self.pwmR = GPIO.PWM(enPinR, 1000)
        self.pwmL.start(0)
        self.pwmR.start(0)
        self.pwmL.ChangeDutyCycle(0)
        self.pwmR.ChangeDutyCycle(0)
        print("motor control initialized")

    def set_speed_left(self, speed: int):
        """
        setting the speed of the left motor
        :param speed: wanted speed
        """
        forceL = min(15, abs(speed))

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
        setting the speed of the right motor
        :param speed: wanted speed
        """
        forceR = min(15, abs(speed))

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
        """
        setting the speed of both motors
        :param speed: wanted speed
        """
        self.set_speed_left(speed)
        self.set_speed_right(speed)

    def stop(self):
        """
        stopping the motors
        """
        self.set_speed(0)
