import RPi.GPIO as GPIO

print("Importing libs...")

from Echo import ECHO
from Gyro import GYRO
from MotorControl import MOTOR_CONTROL
from PidControl import PID_CONTROL
from SelfDriving import SELF_DRIVING
from Wifi import RCV_WIFI_MODULE
from Wifi import SEND_WIFI_MODULE
from TcpHandler import TCP_HANDLER

print("Starting program...")

# setting pins
GPIO.setmode(GPIO.BOARD)
pinMotorLeftForwards = 29
pinMotorRightForwards = 31
pinMotorLeftBackwards = 33
pinMotorRightBackwards = 35
pinEnMotorLeft = 37
pinEnMotorRight = 38
pinEchoTrigger = 16
pinEchoEcho = 18

# default values for PID
Kp = 0.0
Ki = 0.0
Kd = 0.0

# everything for wifi
print("Generating RCV_WIFI_MODULE_CLASS...")
RCV_WIFI_MODULE_CLASS = RCV_WIFI_MODULE()
print("Generating SEND_WIFI_MODULE_CLASS...")
SEND_WIFI_MODULE_CLASS = SEND_WIFI_MODULE()
print("Generating TCP_HANDLER_CLASS...")
TCP_HANDLER_CLASS = TCP_HANDLER()
#
print("Generating MOTOR_CONTROL_CLASS...")
MOTOR_CONTROL_CLASS = MOTOR_CONTROL(pinEnMotorLeft, pinEnMotorRight, pinMotorLeftForwards, pinMotorLeftBackwards,
                                    pinMotorRightForwards, pinMotorRightBackwards)
print("Generating ECHO_CLASS...")
ECHO_CLASS = ECHO(pinEchoTrigger, pinEchoEcho)
print("Generating GYRO_CLASS...")
GYRO_CLASS = GYRO()

# Placeholder for classes
PID_CONTROL_CLASS = None
SELFDRIVING_CLASS = None

print("Main-Class INIT finished.")

if __name__ == "__main__":
    try:
        while True:
            try:

                if Kp == 0.0 and Ki == 0.0 and Kd == 0.0:
                    if RCV_WIFI_MODULE_CLASS.constantsReceived:
                        # wait until constants received from smartphone
                        print("nKp: " + str(RCV_WIFI_MODULE_CLASS.Kp))
                        print("nKi: " + str(RCV_WIFI_MODULE_CLASS.Ki))
                        print("nKd: " + str(RCV_WIFI_MODULE_CLASS.Kd))
                        Kp = RCV_WIFI_MODULE_CLASS.Kp
                        Ki = RCV_WIFI_MODULE_CLASS.Ki
                        Kd = RCV_WIFI_MODULE_CLASS.Kd

                        # class init
                        PID_CONTROL_CLASS = PID_CONTROL(MOTOR_CONTROL_CLASS, Kp, Ki, Kd)
                        if PID_CONTROL_CLASS is None:
                            print("PID_CLASS not defined")
                        SELFDRIVING_CLASS = SELF_DRIVING(GYRO_CLASS, ECHO_CLASS, PID_CONTROL_CLASS)
                        if SELFDRIVING_CLASS is None:
                            print("SELFDRIVING_CLASS not defined")

                        print("Const. INIT finished.")

                if RCV_WIFI_MODULE_CLASS.constantsReceived and (PID_CONTROL_CLASS is not None):

                    if RCV_WIFI_MODULE_CLASS.newData:
                        SEND_WIFI_MODULE_CLASS.smartphoneIp = RCV_WIFI_MODULE_CLASS.smartphoneIp  # IP set
                        RCV_WIFI_MODULE_CLASS.newData = False
                        # data get, RCV_WIFI_MODULE_CLASS can receive again

                    # read gyroscope
                    GYRO_CLASS.read_gyro()
                    speed = RCV_WIFI_MODULE_CLASS.targetSpeedFB
                    turn = RCV_WIFI_MODULE_CLASS.rotateStrength
                    PID_CONTROL_CLASS.control(GYRO_CLASS.yRotation, speed, turn)

            except Exception as e:  # error handling
                MOTOR_CONTROL_CLASS.stop()
                print("Main-Error: " + str(e))
                GPIO.cleanup()
                break

    except Exception as e:  # error handling
        MOTOR_CONTROL_CLASS.stop()
        print("Main-Error: " + str(e))
        GPIO.cleanup()

    except KeyboardInterrupt:  # KeyboardInterrupt handling
        print("Interrupting program...")

        MOTOR_CONTROL_CLASS.stop()

        # delete objects
        del GYRO_CLASS
        del ECHO_CLASS
        del RCV_WIFI_MODULE_CLASS
        del SEND_WIFI_MODULE_CLASS
        del TCP_HANDLER_CLASS

        PID_CONTROL_CLASS.gen_image()

        print("\nProgram manually aborted. Exiting...")
        GPIO.cleanup()

    finally:  # after finishing, cleanup
        MOTOR_CONTROL_CLASS.stop()
        GPIO.cleanup()
