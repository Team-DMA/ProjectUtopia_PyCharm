
gpsBytes = b'$GPGLL,4910.94496,N,00832.53388,E,123553.00,A,A*6C\r\n'

tmp = gpsBytes.decode("utf-8")
print(tmp)
