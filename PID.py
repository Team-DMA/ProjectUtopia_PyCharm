class PID(object):

    def __init__(self, Kp:float, Ki:float, Kd:float):
        
        #übergebene Variablen
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        
        #Variablen intiieren
        self.output = 0.0
        self.buffer = 0.0
        self.difference = 0.0
        self.difference_before = 0.0
        self.controlError = False

        #Gemessen
        self.timeForARun = 0.00009

        #muss noch angepasst werden
        self.maxBuffer = 100.0
        self.maxOutput = 50.0


        print("PID iniziiert")
        
    def pid(self, input, Sollwert, gyroCompensation:float):

        compensatedInput = input - gyroCompensation
        self.difference = Sollwert - self.output
        self.buffer = self.difference * self.timeForARun + self.buffer
        
        #Haupt PID
        self.output = compensatedInput + self.output + self.Kp * self.difference + self.Ki * self.buffer  + self.Kd * ((self.difference_before - self.difference) / self.timeForARun)
        
        self.difference_before = self.difference

        #Abfangen extremer Werte
        if(self.buffer > self.maxBuffer):
            self.buffer = self.maxBuffer

        if(self.buffer < -self.maxBuffer):
            self.buffer = -self.maxBuffer

        if(self.output > self.maxOutput):
            self.output = self.maxOutput
            self.controlError = True
            self.output = 0.0
            self.buffer = 0.0
            self.difference = 0.0
            self.difference_before = 0.0

        if(self.output < -self.maxOutput):
            self.output = -self.maxOutput
            self.controlError = True
            self.output = 0.0
            self.buffer = 0.0
            self.difference = 0.0
            self.difference_before = 0.0
        
        print("Motorausgang = %f" % (self.output/self.maxOutput)*15)
        
        return -(self.output/self.maxOutput)*15
