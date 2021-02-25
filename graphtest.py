# graph
import matplotlib.pyplot as plt
import pandas as pd
import random
import time

pidDataList = [0.0]
timeDataList = [0.0]
gyroDataList = [0.0]
startTime = time.time()
time.sleep(0.00005)

#for x in range(1, 10):
tmp = round(random.uniform(1, 10), 3)
print(str(tmp))
now = time.time() - startTime
gyroDataList.append(tmp)
tmp2 = tmp * (round(random.uniform(1, 2), 1))
print(str(tmp2))
pidDataList.append(tmp2)
timeDataList.append(now)

try:
    # data
    columns = ["Time", "ControlValue", "Rotation"]
    rows = zip(timeDataList, pidDataList, gyroDataList)

    # combine rows and column names into pandas dataframe
    data = pd.DataFrame(rows, columns=columns)

    data.plot(x="Time", y=["ControlValue", "Rotation"])

    # data.to_excel('PID_DATA_EXCEL.xlsx', sheet_name='new_sheet', index=False)

    # plt.show(block=False)

    plt.xlabel("Zeit in s")
    plt.title("Regler macht brrrrr")

    plt.savefig('graph_pid.png', bbox_inches='tight')

    print("\nImage generated. Exiting...")

except Exception as e:
    print("\nError while plotting: " + str(e))
