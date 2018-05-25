

from __future__ import print_function
from __future__ import division

import os
import cv2
from subprocess import call
path = 'assignment'
call('mkdir {}'.format(path), shell=True)

def get_images():
    camera = cv2.VideoCapture(1)
    if not camera.isOpened():
        print('can\'t open this thing!')

    over = False
    counter = 0
    # window = cv2.namedWindow('feed', cv2.WINDOW_NORMAL)
    while not over:
        frame = camera.read()[1]
        frame = cv2.resize(frame, (600, 600))
        cv2.imshow('feed', frame)
        key = cv2.waitKey(1)
        if key == ord('q') or key == 27:
            over = True
        elif key == ord(' '):
            counter += 1
            cv2.imwrite(os.path.join(path, 'image-{}.jpg'.format(counter)), frame)
            print('saved {}'.format(os.path.join(path, 'image-{}.jpg'.format(counter))))
        pass
    pass


if __name__ == '__main__':
    get_images()