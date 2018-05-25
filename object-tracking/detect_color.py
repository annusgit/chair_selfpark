
from __future__ import print_function
from __future__ import division

from collections import deque
import numpy as np
import argparse
import imutils
import cv2


def find_color(buffer_size, device, color='red'):

    # define the lower and upper boundaries of the "green"
    # ball in the HSV color space, then initialize the
    # list of tracked points
    redLower = (57, 184, 57)
    redUpper = (255, 255, 255)
    greenLower = (38, 46, 0)
    greenUpper = (113, 165, 176)
    blueLower = (69, 43, 37)
    blueUpper = (131, 201, 200)
    if color == 'green':
        lowerLimit = greenLower
        upperLimit = greenUpper
    elif color == 'blue':
        lowerLimit = blueLower
        upperLimit = blueUpper
    elif color == 'red':
        lowerLimit = redLower
        upperLimit = redUpper
    else:
        return -1
    pts = deque(maxlen=buffer_size)
    print(lowerLimit, upperLimit)
    # if a video path was not supplied, grab the reference
    # to the webcam
    cam = cv2.VideoCapture(device)
    if not cam.isOpened():
        print("Video device or file couldn't be opened")
        exit()

    # keep looping
    while True:
        # grab the current frame
        grabbed, frame = cam.read()

        # resize the frame, blur it, and convert it to the HSV
        # color space
        frame = imutils.resize(frame, width=600)
        # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # construct a mask for the color "green", then perform
        # a series of dilations and erosions to remove any small
        # blobs left in the mask
        mask = cv2.inRange(hsv, lowerLimit, upperLimit)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        # find contours in the mask and initialize the current
        # (x, y) center of the ball
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None

        # only proceed if at least one contour was found
        if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

            # only proceed if the radius meets a minimum size
            if radius > 10:
                # draw the circle and centroid on the frame,
                # then update the list of tracked points
                cv2.circle(frame, (int(x), int(y)), int(radius),
                           (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)

        # update the points queue
        pts.appendleft(center)

        # loop over the set of tracked points
        for i in xrange(1, len(pts)):
            # if either of the tracked points are None, ignore
            # them
            if pts[i - 1] is None or pts[i] is None:
                continue

            # otherwise, compute the thickness of the line and
            # draw the connecting lines
            thickness = int(np.sqrt(buffer_size / float(i + 1)) * 2.5)
            cv2.line(frame, pts[i - 1], pts[i], (255, 0, 0), thickness)

        # show the frame to our screen
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF

        # if the 'q' key is pressed, stop the loop
        if key == ord("q") or key == 27:
            break

    # cleanup the camera and close any open windows
    cam.release()
    cv2.destroyAllWindows()



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--buffer', dest='buffer_size')
    parser.add_argument('-d', '--device', dest='device')
    parser.add_argument('-c', '--color', dest='color', help='chose color to track')
    args = parser.parse_args()
    buffer_size = int(args.buffer_size)
    find_color(buffer_size=int(args.buffer_size), device=int(args.device), color=args.color)





