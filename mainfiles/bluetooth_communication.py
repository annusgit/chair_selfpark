


from __future__ import print_function
from __future__ import division
import bluetooth
import argparse
import pygame
import time


def cart_bluetooth(mode='stateless'):

    hc06_new = '20:15:12:04:25:19' # our device's mac address
    port = 1 # this port number has been fixed now, must delete the device to change it!!!

    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    print('log: trying to connect to {}'.format(hc06_new))
    sock.connect((hc06_new, port))
    print('log: Connected!')
    sock.settimeout(100.0)

    scr_width = 650
    scr_height = 600
    pygame.init()
    delay = 0.2
    screen = pygame.display.set_mode([scr_width, scr_height])
    pygame.display.set_caption('testing')
    colors = {'white': (255, 255, 255), 'black': (0, 0, 0), 'red': (255, 0, 0),
              'green': (0, 255, 0), 'blue': (0, 0, 255)}
    screen.fill(colors['white'])

    over = False
    state = 'idle'
    while not over:
        # get some events
        if mode == 'stateless':
            state = 'idle'
        for event in pygame.event.get():
            # if event.type == pygame.QUIT:
            #     over = True
            if event.type == pygame.KEYDOWN:
                # let's see which key was pressed
                key_pressed = event.key
                if key_pressed == pygame.K_q or key_pressed == pygame.K_ESCAPE:
                    over = True
                elif key_pressed == pygame.K_UP:
                    state = 'up'
                elif key_pressed == pygame.K_DOWN:
                    state = 'down'
                elif key_pressed == pygame.K_RIGHT:
                    state = 'right'
                elif key_pressed == pygame.K_LEFT:
                    state = 'left'
                elif key_pressed == pygame.K_SPACE:
                    state = 'idle'
        sock.send(state)
        pygame.display.flip()
        time.sleep(delay)
    sock.close()
    pass



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode', dest='mode', help='how to run the motor, continuous or each state?')
    args = parser.parse_args()
    mode = args.mode
    modes = ['stateful', 'stateless']
    if mode in modes:
        cart_bluetooth(mode=mode)
    else:
        print('log: bad argument for mode, chosing stateless...')
        cart_bluetooth(mode='stateless')











