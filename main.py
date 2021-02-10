import RPi.GPIO as GPIO

from Echo import ECHO
from Gyro import GYRO
from MotorControl import MOTOR_CONTROL
from PidControl import PID_CONTROL
from Selfdriving import SELFDRIVING
from Wifi import RCV_WIFI_MODULE
from Gps import GPS

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

# everything for wifi
RCV_WIFI_MODULE_CLASS = RCV_WIFI_MODULE()
# SendWifiThread = wifi.SEND_WIFI_MODULE()
# tcpHandlerClass = tcpHandler.TCP_HANDLER()

MOTOR_CONTROL_CLASS = MOTOR_CONTROL(pinEnMotorLeft, pinEnMotorRight, pinMotorLeftForwards, pinMotorLeftBackwards,
                                    pinMotorRightForwards, pinMotorRightBackwards)
ECHO_CLASS = ECHO(pinEchoTrigger, pinEchoEcho)
GYRO_CLASS = GYRO()
GPS_CLASS = GPS()

# Placeholder for Classes
PID_CONTROL_CLASS = None
SELFDRIVING_CLASS = None


print("Main-Class INIT finished.")

if __name__ == "__main__":
    try:
        while True:
            try:
                if Kp == 0.0 and Ki == 0.0 and Kd == 0.0:
                    if RCV_WIFI_MODULE_CLASS.constantsReceived:
                        print("nKp: "+str(RcvWifiThread.Kp))
                        print("nKi: "+str(RcvWifiThread.Ki))
                        print("nKd: "+str(RcvWifiThread.Kd))
                        Kp = RcvWifiThread.Kp
                        Ki = RcvWifiThread.Ki
                        Kd = RcvWifiThread.Kd

                        # Class init
                        PID_CONTROL_CLASS = PID_CONTROL(MOTOR_CONTROL_CLASS, Kp, Ki, Kd)
                        if PID_CONTROL_CLASS is None:
                            print("PID_CLASS not defined")
                        SELFDRIVING_CLASS = SELFDRIVING(GYRO_CLASS, ECHO_CLASS, PID_CONTROL_CLASS, gyroCompensation)
                        if SELFDRIVING_CLASS is None:
                            print("SELFDRIVING_CLASS not defined")
                        print("Const. INIT finished.")

                if RCV_WIFI_MODULE_CLASS.constantsReceived:

                    if RCV_WIFI_MODULE_CLASS.newData:
                        print("\nTargetSpeedFB: "+str(RCV_WIFI_MODULE_CLASS.targetSpeedFB))
                        # forwards or backwards depending on +/-
                        print("\nRotateStrength: "+str(RCV_WIFI_MODULE_CLASS.rotateStrength))
                        # left or right depending on -/+
                        # SendWifiThread.Smartphone_IP = RcvWifiThread.Smartphone_IP #IP set
                        RCV_WIFI_MODULE_CLASS.newData = False
                        # data crunched, RCV_WIFI_MODULE_CLASS can receive again

                    if True:
                        # read gyroscope
                        GYRO_CLASS.read_gyro()

                        distance = ECHO_CLASS.distance  # Debug
                        print("Debug distance: " + str(distance))  # Debug

                        speed = RCV_WIFI_MODULE_CLASS.targetSpeedFB
                        turn = RCV_WIFI_MODULE_CLASS.rotateStrength
                        PID_CONTROL_CLASS.control(GYRO_CLASS.yRotation, speed, turn, gyroCompensation)
                        GPS_CLASS.gps()
                        gps = "Latitude=" + str(GPS_CLASS.get_latitude()) + "and Longitude=" + \
                              str(GPS_CLASS.get_longitude())
                        print(gps)

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