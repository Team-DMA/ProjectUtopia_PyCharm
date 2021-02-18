import threading
import time


class INPUT_SIM(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True

        self.waitTime = 0.0005  # in seconds

        self.gyro_y = 0
        self.enabled = True

        self.readyToGet = False

        self.start()

    def run(self):
        # for x in range(-70, 81):
        #     self.gyro_y = x
        #     time.sleep(self.waitTime)
        #for x in range(80, 0, -1):

        self.gyro_y = 45
        time.sleep(self.waitTime / 2)
        self.gyro_y = 100
        time.sleep(self.waitTime)
        self.gyro_y = 0
        time.sleep(3 * self.waitTime)
        self.gyro_y = -10
        time.sleep(self.waitTime)

        self.gyro_y = 0
        time.sleep(1)

        self.enabled = False

        """
        while True:

            if self.readyToGet:

                self.input_value = 0

                txt = input("Type a new value: ")
                if txt.isnumeric():
                    self.input_value = int(txt)

                    if self.input_value == 1337:
                        self.enabled = False

                    print("\nYour number: " + str(self.input_value))
                else:
                    print("\nWrong input.")
        """
