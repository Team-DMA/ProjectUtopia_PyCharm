from pid_malanders import PID
from PID_forTest import PID_Lukas
import time

import matplotlib.pyplot as plt

import pandas as pd

from input_simulation import INPUT_SIM

setpoint = 0
Kp = 0.3
Ki = 0.008
Kd = 0.005
# Ki = 0.1
# Kd = 0.7

"""
Gute Werte für M-Regler: Kp = 1.05, Ki = 0.5, Kd = 0.007
Gute Werte für L-Regler: Kp = 0.8, Ki = 0.4, Kd = 0.005
"""

pid = PID(Kp, Ki, Kd, setpoint)
pid.proportional_on_measurement = True
pid.sample_time = 0.001

pid2 = PID_Lukas(Kp, Ki, Kd)

startTime = time.time()

pidDataList = [setpoint]
timeDataList = [0]
gyroDataList = [setpoint]
waitTime = 0.0  # in seconds

tmpInputClass = INPUT_SIM()

gyro_y = 0


def scale(old_value, old_min, old_max, new_min, new_max):
    new_value = ((old_value - old_min) / (old_max - old_min)) * (new_max - new_min) + new_min
    return new_value


while True:

    if tmpInputClass.enabled:

        tmpInputClass.readyToGet = True

        # pid.sample_time = timeForPid
        gyro_y = tmpInputClass.gyro_y
        #output = pid(gyro_y)                           # M-Regler
        output = pid2.pid(gyro_y, setpoint, 0, 0.01)    # L-Regler
        now = time.time() - startTime

        gyroDataList.append(gyro_y)

        #pidDataList.append(scale(output, 0, 30, 0, 15))   # Regler Skalierung
        pidDataList.append(output)                          # Regler unskaliert

        timeDataList.append(now)

        tmpInputClass.readyToGet = False

    else:

        print("\nTrying to write file...")

        try:
            # data
            columns = ["Time", "ControlValue", "Gyroskop"]
            rows = zip(timeDataList, pidDataList, gyroDataList)

            # combine rows and column names into pandas dataframe
            data = pd.DataFrame(rows, columns=columns)

            data.plot(x="Time", y=["ControlValue", "Gyroskop"])
            plt.show()

            #data.to_excel('PID_DATA_EXCEL.xlsx', sheet_name='new_sheet', index=False)

            print("\nFile saved. Exiting...")

            exit()

        except Exception as e:
            print("\nError: " + str(e))
