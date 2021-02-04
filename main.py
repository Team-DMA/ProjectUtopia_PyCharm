import RPi.GPIO as GPIO

from Echo import ECHO
from Gyro import GYRO
from MotorControl import MOTOR_CONTROL
from PidControl import PID_CONTROL
from Selfdriving import SELFDRIVING
from Wifi import RCV_WIFI_MODULE

GPIO.setmode(GPIO.BOARD)
pinMotorLeftForwards = 29
pinMotorRightForwards = 31
pinMotorLeftBackwards = 33
pinMotorRightBackwards = 35
pinEnMotorLeft = 37
pinEnMotorRight = 38
pinEchoTrigger = 8
pinEchoEcho = 10
Kp = 0.0
Ki = 0.0
Kd = 0.0
gyroCompensation = 0


# alles zu wifi
RcvWifiThread = RCV_WIFI_MODULE()
# SendWifiThread = wifi.SEND_WIFI_MODULE()
# tcpHandlerClass = tcpHandler.TCP_HANDLER()


MOTOR_CONTROL_CLASS = MOTOR_CONTROL(pinEnMotorLeft, pinEnMotorRight, pinMotorLeftForwards, pinMotorLeftBackwards,
                                    pinMotorRightForwards, pinMotorRightBackwards)
ECHO_CLASS = ECHO(pinEchoTrigger, pinEchoEcho)
GYRO_CLASS = GYRO()

# Platzhalter für Klassen
PID_CONTROL_CLASS = None
SELFDRIVING_CLASS = None


print ("Main-Class INIT finished.")

if __name__ == "__main__":

    try:
        while True:
            try:
                if(Kp == 0.0 and Ki == 0.0 and Kd == 0.0):
                    if(RcvWifiThread.KonstantenReceived == True):
                        print("nKp: "+str(RcvWifiThread.Kp))
                        print("nKi: "+str(RcvWifiThread.Ki))
                        print("nKd: "+str(RcvWifiThread.Kd))
                        Kp = RcvWifiThread.Kp
                        Ki = RcvWifiThread.Ki
                        Kd = RcvWifiThread.Kd

                        # Klassen init
                        PID_CONTROL_CLASS = PID_CONTROL(MOTOR_CONTROL_CLASS, Kp, Ki, Kd)
                        SELFDRIVING_CLASS = SELFDRIVING(GYRO_CLASS, ECHO_CLASS, PID_CONTROL_CLASS, gyroCompensation)

                        print("Const. INIT finished.")

                if(RcvWifiThread.KonstantenReceived == True and Kp != 0.0 and Ki != 0.0 and Kd != 0.0):

                    if(RcvWifiThread.neueDaten == True):
                        print("\nTargetSpeedFB: "+str(RcvWifiThread.targetSpeedFB))
                        # vorwaerts oder rueckwaerts je nach vorzeichen
                        print("\nRotateStrength: "+str(RcvWifiThread.rotateStrength))
                        # links oder rechts mit welcher Geschw. je nach Vorzeichen
                        # SendWifiThread.Smartphone_IP = RcvWifiThread.Smartphone_IP #IP setzen
                        RcvWifiThread.neueDaten = False
                        # daten wurden verarbeitet, also kann RcvWifiThread wieder empfangen

                    if(True):
                        # read gyroskop
                        GYRO_CLASS.read_gyro()

                        distance = ECHO_CLASS.distance # Debug
                        print("Debug Distanz: " + str(distance)) # Debug

                        speed = RcvWifiThread.targetSpeedFB
                        turn = RcvWifiThread.rotateStrength
                        PID_CONTROL_CLASS.control(GYRO_CLASS.x_rotation, speed, turn, gyroCompensation)

                    else:
                        SELFDRIVING_CLASS.drive()

            except Exception as e:
                print("Main-Error: "+str(e))
                GPIO.cleanup()
                break

    except Exception as e:
        print("Main-Error: "+str(e))
        GPIO.cleanup()

    finally:
        GPIO.cleanup()