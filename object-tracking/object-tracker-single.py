
# Import the required modules

from __future__ import division
import dlib
import cv2
import argparse as ap
import get_points
import pygame
import numpy as np
import time


def run(source=0, dispLoc=False):
    # Create the VideoCapture object
    cam = cv2.VideoCapture(source)

    # If Camera Device is not opened, exit the program
    if not cam.isOpened():
        print "Video device or file couldn't be opened"
        exit()
    
    print "Press key `p` to pause the video to start tracking"
    while True:
        # Retrieve an image and Display it.
        retval, img = cam.read()
        if not retval:
            print "Cannot capture frame device"
            exit()
        if(cv2.waitKey(10)==ord('p')):
            break
        # cv2.namedWindow("Cam Feed", cv2.WINDOW_NORMAL)
        cv2.namedWindow('Cam Feed')
        cv2.imshow("Cam Feed", img)

        # Co-ordinates of objects to be tracked
        # will be stored in a list named `points`
        #points = get_points.run(img)

    cv2.destroyWindow("Cam Feed")

    # Co-ordinates of objects to be tracked 
    # will be stored in a list named `points`
    points = get_points.run(img) 

    if not points:
        print "ERROR: No object to be tracked."
        exit()
    
    # cv2.namedWindow("Cam Feed", cv2.WINDOW_NORMAL)
    cv2.namedWindow('Cam Feed')
    cv2.imshow("Cam Feed", img)

    # Initial co-ordinates of the object to be tracked 
    # Create the tracker object
    tracker = dlib.correlation_tracker()
    # Provide the tracker the initial position of the object
    tracker.start_track(img, dlib.rectangle(*points[0]))

    while True:
        # Read frame from device or file
        retval, img = cam.read()
        if not retval:
            print "Cannot capture frame device | CODE TERMINATING :("
            exit()
        # Update the tracker  
        tracker.update(img)
        # Get the position of the object, draw a 
        # bounding box around it and display it.
        rect = tracker.get_position()
        pt1 = (int(rect.left()), int(rect.top()))
        pt2 = (int(rect.right()), int(rect.bottom()))
        cv2.rectangle(img, pt1, pt2, (255, 255, 255), 3)
        print "Object tracked at [{}, {}]".format(pt1, pt2)
        if dispLoc:
            loc = (int(rect.left()), int(rect.top()-20))
            txt = "Object tracked at [{}, {}]".format(pt1, pt2)
            cv2.putText(img, txt, loc , cv2.FONT_HERSHEY_SIMPLEX, .5, (255,255,255), 1)
        # cv2.namedWindow("Cam Feed", cv2.WINDOW_NORMAL)
        # cv2.namedWindow('Cam Feed')
        cv2.imshow("Cam Feed", img)
        # Continue until the user presses ESC key
        if cv2.waitKey(1) == 27:
            break

    # Relase the VideoCapture object
    cam.release()


def Main(source=0, dispLoc=False):

    # Create the VideoCapture object
    cam = cv2.VideoCapture(source)

    # If Camera Device is not opened, exit the program
    if not cam.isOpened():
        print "Video device or file couldn't be opened"
        exit()

    print "Press key `p` to pause the video to start tracking"
    while True:
        # Retrieve an image and Display it.
        retval, img = cam.read()
        img = cv2.flip(img,1) # flip horizontally for correct orientation
        if not retval:
            print "Cannot capture frame device"
            exit()
        if (cv2.waitKey(10) == ord('p')):
            break
        # cv2.namedWindow("Cam Feed", cv2.WINDOW_NORMAL)
        cv2.namedWindow('Cam Feed')
        cv2.imshow("Cam Feed", img)

        # Co-ordinates of objects to be tracked
        # will be stored in a list named `points`
        # points = get_points.run(img)

    cv2.destroyWindow("Cam Feed")

    # Co-ordinates of objects to be tracked
    # will be stored in a list named `points`
    points = get_points.run(img)

    if not points:
        print "ERROR: No object to be tracked."
        exit()

    # cv2.namedWindow("Cam Feed", cv2.WINDOW_NORMAL)
    cv2.namedWindow('Cam Feed')
    cv2.imshow("Cam Feed", img)

    # Initial co-ordinates of the object to be tracked
    # Create the tracker object
    tracker = dlib.correlation_tracker()
    # Provide the tracker the initial position of the object
    tracker.start_track(img, dlib.rectangle(*points[0]))
    ###### by this time we have the position of the object to be tracked

    # now initialize pygame and grid
    scr_width = 650; scr_height = 600
    grid_spacing_vertical = scr_height//2
    grid_spacing_horizontal = scr_width//2
    line_width = 2; delay = 0.05
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode([scr_width,scr_height])
    pygame.display.set_caption('Localization Grid')
    colors = {'white': (255, 255, 255), 'black': (0, 0, 0), 'red': (255, 0, 0),
              'green': (0, 255, 0), 'blue': (0, 0, 255)}
    screen.fill(colors['white'])

    # get all the vertices for our localization grid
    localization_grid = []
    for col in range(1, scr_width // grid_spacing_horizontal):
        for row in range(1, scr_height // grid_spacing_vertical):
            # the first two points are for the column and the other two are for the row
            localization_grid.append([(col * grid_spacing_horizontal, 0), (col * grid_spacing_horizontal, scr_height),
                                      (0, row * grid_spacing_vertical), (scr_width, row * grid_spacing_vertical)])
    localization_grid = np.asarray(localization_grid)

    # draw it only once
    for points in localization_grid[:, ]:
        pygame.draw.lines(screen, colors['black'], False, [points[0], points[1]], line_width)
        pygame.draw.lines(screen, colors['black'], False, [points[2], points[3]], line_width)

    ###################################################################
    # now open the camera and start the grid
    over = False
    while not over:
        # Read frame from device or file
        retval, img = cam.read()
        img = cv2.flip(img,1) # flip horizontally for correct orientation
        if not retval:
            print "Cannot capture frame device | CODE TERMINATING :("
            exit()
        # Update the tracker
        tracker.update(img)
        # Get the position of the object, draw a
        # bounding box around it and display it.
        rect = tracker.get_position()
        pt1 = (int(rect.left()), int(rect.top()))
        pt2 = (int(rect.right()), int(rect.bottom()))
        cv2.rectangle(img, pt1, pt2, (255, 255, 255), 3)
        print "********************************************"
        print "Object tracked at [{}, {}]".format(pt1, pt2)
        if dispLoc:
            loc = (int(rect.left()), int(rect.top()-20))
            txt = "Object tracked at [{}, {}]".format(pt1, pt2)
            cv2.putText(img, txt, loc , cv2.FONT_HERSHEY_SIMPLEX, .5, (255,255,255), 1)
        # cv2.namedWindow("Cam Feed", cv2.WINDOW_NORMAL)
        # cv2.namedWindow('Cam Feed')
        cv2.imshow("Cam Feed", img)

        # and here's the grid
        # get some events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                over = True
            if event.type == pygame.KEYDOWN:
                # let's see which key was pressed
                key_pressed = event.key
                if key_pressed == pygame.K_q or key_pressed == pygame.K_ESCAPE:
                    over = True

        # now draw the grid, with the center of the chair or target as well
        center = ((pt1[0]+pt2[0])/2, (pt1[1]+pt2[1])/2)
        # scale them
        center = map(int, (center[0]/640*scr_width, center[1]/480*scr_height))
        print "position on grid at {}".format(center)
        print "********************************************"
        # for points in localization_grid[:, ]:
        #     pygame.draw.lines(screen, colors['black'], False, [points[0], points[1]], line_width)
        #     pygame.draw.lines(screen, colors['black'], False, [points[2], points[3]], line_width)
        #     # the following is the center
        pygame.draw.circle(screen, colors['blue'], center, 4)
        # pygame.display.update()
        pygame.display.flip()
        time.sleep(delay)

        # Continue until the user presses ESC key
        key_pressed = cv2.waitKey(1)
        if key_pressed == 27 or key_pressed == ord('q'):
            over = True
            # pass
    # Relase the VideoCapture object
    cam.release()
    pass


def main():
    # Parse command line arguments
    parser = ap.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-d', "--deviceID", help="Device ID")
    group.add_argument('-v', "--videoFile", help="Path to Video File")
    parser.add_argument('-l', "--dispLoc", dest="dispLoc", action="store_true")
    args = vars(parser.parse_args())

    # Get the source of video
    if args["videoFile"]:
        source = args["videoFile"]
    else:
        source = int(args["deviceID"])
    run(source, args["dispLoc"])


if __name__ == "__main__":
    # Parse command line arguments
    parser = ap.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-d', "--deviceID", help="Device ID")
    group.add_argument('-v', "--videoFile", help="Path to Video File")
    parser.add_argument('-l', "--dispLoc", dest="dispLoc", action="store_true")
    args = vars(parser.parse_args())

    # Get the source of video
    if args["videoFile"]:
        source = args["videoFile"]
    else:
        source = int(args["deviceID"])
    Main(source, args["dispLoc"])
