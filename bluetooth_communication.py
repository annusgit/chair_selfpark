


from __future__ import print_function
from __future__ import division
# import socket as sock
import bluetooth


class Bluetoothman(object):

    """
        this class deals with setting up a bluetooth connection and sending control packets to that vehicle
    """

    def __init__(self, mac_address, port):

        # the device address we want to connect to...
        self.mac_target = mac_address
        self.port = port
        self.socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        pass


    def connect(self):
        self.socket.connect((self.mac_target, self.port))
        print('log: Connection Successful!!!')
        pass


    def send(self, message='run'):

        self.socket.send(message)
        pass


    def close(self):

        # when we terminate the connection
        self.socket.close()


def main():

    import bluetooth
    hc06_new = '20:15:12:04:25:19' # our device's mac address
    port = 1 # this port number has been fixed now, must delete the device to change it!!!

    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((hc06_new, port))
    print('Connected')
    sock.settimeout(100.0)

    while True:
        message = raw_input('Type a message: ')
        if message == 'q':
            break
        sock.send(message)
    sock.close()

    sock.close()
    pass


if __name__ == '__main__':
    main()











