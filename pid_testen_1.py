from PID import PID
import time
from pi_test import PID_Dominik
import matplotlib.pyplot as plt

import pandas as pd

print(str(pd.__version__))

from input_simulation import INPUT_SIM

setpoint = 0
Kp = 0.3
Ki = 3
Kd = 0.008
# Ki = 0.1
# Kd = 0.7

"""
Gute Werte für L-Regler: Kp = 0.2, Ki = 0.7, Kd = 0.005
"""

pid = PID(Kp, Ki, Kd, None, (-75, 75))

pid3 = PID_Dominik(Kp, 10)
pidDataList = [setpoint]
timeDataList = [0.0]
gyroDataList = [setpoint]
waitTime = 0.0  # in seconds

tmpInputClass = INPUT_SIM()

gyro_y = 0

startTime = time.time()


def scale(old_value, old_min, old_max, new_min, new_max):
    new_value = ((old_value - old_min) / (old_max - old_min)) * (new_max - new_min) + new_min
    return new_value


while True:

    if tmpInputClass.enabled:

        tmpInputClass.readyToGet = True

        # pid.sample_time = timeForPid
        gyro_y = tmpInputClass.gyro_y
        output = -pid(gyro_y)  # M-Regler
        # output = pid2.pid(gyro_y, setpoint, 0, 0.01)    # L-Regler
        # output = pid3.pid(gyro_y, setpoint)    #D-Regler
        now = time.time() - startTime

        # output = (int(round(output)))

        gyroDataList.append(gyro_y)

        pidDataList.append(scale(output, -75, 75, -15, 15))   # Regler Skalierung
        #pidDataList.append(output)  # Regler unskaliert

        timeDataList.append(now)

        tmpInputClass.readyToGet = False

    else:

        print("\nTrying to write file...")

        try:
            # data
            columns = ["Time", "Regler-Ausgang", "Gyroskop"]
            rows = zip(timeDataList, pidDataList, gyroDataList)

            # combine rows and column names into pandas dataframe
            data = pd.DataFrame(rows, columns=columns)

            data.plot(x="Time", y=["Regler-Ausgang", "Gyroskop"])

            plt.xlabel("Zeit in s")
            plt.title("PID-T1")

            plt.show()

            # data.to_excel('PID_DATA_EXCEL.xlsx', sheet_name='new_sheet', index=False)

            print("\nFile saved. Exiting...")

            exit()

        except Exception as e:
            print("\nError: " + str(e))
