
from __future__ import print_function
from __future__ import division
import bluetooth
import time


# set bluetooth connection
hc06_new = '20:15:12:04:25:19'  # our device's mac address
port = 1  # this port number has been fixed now, must delete the device to change it!!!

def main():
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    print('log: Trying to connect to {}'.format(hc06_new))
    sock.connect((hc06_new, port))
    sock.settimeout(100.0)
    print('log: Connected!')

    message = 'this is the beginning'
    sock.send(message)
    while True:
        sock.send(message)
        received = sock.recv(64)
        if received:
            print('log: we received this: {}'.format(received[0:7]))
        pass
        if received == 'bad':
            break
        time.sleep(0.1)
    sock.close()
    pass



if __name__ == '__main__':
    main()