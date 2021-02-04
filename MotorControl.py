import RPi.GPIO as GPIO

class MOTOR_CONTROL(object):

    def __init__(self, enPinL: int,enPinR: int, inForewardPinL: int, inBackwardPinL: int,inForewardPinR: int, inBackwardPinR: int):
        
        self.inForewardPinL = inForewardPinL
        GPIO.setup(inForewardPinL, GPIO.OUT)
        GPIO.output(inForewardPinL, False)
 
        self.inBackwardPinL = inBackwardPinL
        GPIO.setup(inBackwardPinL, GPIO.OUT)
        GPIO.output(inBackwardPinL, False)
 
        GPIO.setup(enPinL, GPIO.OUT)

        self.inForewardPinR = inForewardPinR
        GPIO.setup(inForewardPinR, GPIO.OUT)
        GPIO.output(inForewardPinL, False)
 
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
        print("motorcontrol iniziiert")


    def setSpeedL(self, speed: int):

        """
            speed might be -15...+15
        """
        forceL = min(15, abs(speed))
        #print ("forceL %d" % forceL)

        if (speed > 0):
            GPIO.output(self.inBackwardPinL, False)
            GPIO.output(self.inForewardPinL, True)
        elif (speed < 0):
            GPIO.output(self.inForewardPinL, False)
            GPIO.output(self.inBackwardPinL, True)
        else:
            GPIO.output(self.inForewardPinL, False)
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
        #print ("forceR %d" % forceR)

        if (speed > 0):
            GPIO.output(self.inBackwardPinR, False)
            GPIO.output(self.inForewardPinR, True)
        elif (speed < 0):
            GPIO.output(self.inForewardPinR, False)
            GPIO.output(self.inBackwardPinR, True)
        else:
            GPIO.output(self.inForewardPinR, False)
            GPIO.output(self.inBackwardPinR, False)

        if forceR > 0:
            self.pwmR.ChangeDutyCycle(10 + 6 * forceR)
        else:
            self.pwmR.ChangeDutyCycle(0)


    def setSpeed(self,speed: int):

        self.setSpeedL(speed)
        self.setSpeedR(speed)
        #print("Geschwindigkeit auf %f" % speed)


    def turnLeft(speed: int):

        setSpeedL(0)
        setSpeedR(speed)
        print("links drehen")


    def turnRight(speed: int):

        setSpeedR(0)
        setSpeedL(speed)
        print("rechts drehen")


    def forward(speed: int):

        if(speed > 0):
            setSpeed(speed)
            print("Vorwaerts")


    def backward(speed: int):

        if(speed < 0):
            setSpeed(speed)
            print("Rueckwaerts")


    def stopp():

        setSpeed(0)
