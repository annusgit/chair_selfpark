

# Import the required modules
from __future__ import print_function
from __future__ import division
from collections import deque
import argparse as ap
import numpy as np
import bluetooth
import imutils
import pygame
import time
import dlib
import cv2
import get_points


def run(source=0, dispLoc=False):
    # Create the VideoCapture object
    cam = cv2.VideoCapture(source)

    # If Camera Device is not opened, exit the program
    if not cam.isOpened():
        print("Video device or file couldn't be opened")
        exit()
    
    print("Press key `p` to pause the video to start tracking")
    while True:
        # Retrieve an image and Display it.
        retval, img = cam.read()
        img = cv2.flip(img,1) # flip horizontally for correct orientation
        if not retval:
            print("Cannot capture frame device")
            exit()
        key = cv2.waitKey(1)
        if (key == ord('p')):
            break
        elif key == 27:
            print('exiting now!')
            exit(0)
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
        print("ERROR: No object to be tracked.")
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
        img = cv2.flip(img,1) # flip horizontally for correct orientation
        if not retval:
            print("Cannot capture frame device | CODE TERMINATING :(")
            exit()
        # Update the tracker  
        tracker.update(img)
        # Get the position of the object, draw a 
        # bounding box around it and display it.
        rect = tracker.get_position()
        pt1 = (int(rect.left()), int(rect.top()))
        pt2 = (int(rect.right()), int(rect.bottom()))
        cv2.rectangle(img, pt1, pt2, (255, 255, 255), 3)
        # print("Object tracked at [{}, {}]".format(pt1, pt2))
        if False: #dispLoc:
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


def cam_with_grid(kwargs):
    source = int(kwargs['device'])
    # Create the VideoCapture object
    cam = cv2.VideoCapture(source)
    # cam.set(cv2.CV_CAP_PROP_FRAME_WIDTH, 640)
    # cam.set(cv2.CV_CAP_PROP_FRAME_HEIGHT,480)
    #
    # If Camera Device is not opened, exit the program
    if not cam.isOpened():
        print("Video device or file couldn't be opened")
        exit()

    print("Press key `p` to pause the video to start tracking")
    while True:
        # Retrieve an image and Display it.
        retval, img = cam.read()
        img = cv2.flip(img,1) # flip horizontally for correct orientation
        if not retval:
            print("Cannot capture frame device")
            exit()
        key = cv2.waitKey(1)
        if (key == ord('p')):
            break
        elif key == 27:
            print('exiting now!')
            exit(0)
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
        print("ERROR: No object to be tracked.")
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
    line_width = 2; delay = 0.8
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
    counter = 0
    while not over:
        # Read frame from device or file
        retval, img = cam.read()
        img = cv2.flip(img,1) # flip horizontally for correct orientation
        if not retval:
            print("Cannot capture frame device | CODE TERMINATING :(")
            exit()
        # Update the tracker
        tracker.update(img)
        # Get the position of the object, draw a
        # bounding box around it and display it.
        rect = tracker.get_position()
        pt1 = (int(rect.left()), int(rect.top()))
        pt2 = (int(rect.right()), int(rect.bottom()))
        cv2.rectangle(img, pt1, pt2, (255, 255, 255), 3)
        # print("********************************************")
        # print("Object tracked at [{}, {}]".format(pt1, pt2))
        if False: #dispLoc:
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
        # print("you sent: {}".format(message))

        # now draw the grid, with the center of the chair or target as well
        center = ((pt1[0]+pt2[0])/2, (pt1[1]+pt2[1])/2)
        # scale them
        center = map(int, (center[0]/640*scr_width, center[1]/480*scr_height))
        # print("position on grid at {}".format(center))
        # print("********************************************")
        # the following is the center
        pygame.draw.circle(screen, colors['blue'], center, 4)
        pygame.display.update()
        pygame.display.flip()
        # time.sleep(delay)

        # Continue until the user presses ESC key
        key_pressed = cv2.waitKey(1)
        if key_pressed == 27 or key_pressed == ord('q'):
            over = True
            # pass
    # Relase the VideoCapture object
    cam.release()
    pass


def optical_flow(kwargs):
    source = int(kwargs['device'])
    bluetooth_use = int(kwargs['bluetooth'])

    # set bluetooth connection
    hc06_new = '20:15:12:04:25:19' # our device's mac address
    port = 1 # this port number has been fixed now, must delete the device to change it!!!

    if bluetooth_use:
        sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        print('log: Trying to connect to {}'.format(hc06_new))
        sock.connect((hc06_new, port))
        sock.settimeout(100.0)
        print('log: Connected!')
    else:
        print('going without bluetooth')


    # Create the VideoCapture object
    cam = cv2.VideoCapture(source)

    # If Camera Device is not opened, exit the program
    if not cam.isOpened():
        print("Video device or file couldn't be opened")
        exit()

    print("Press key `p` to pause the video to start tracking")
    while True:
        # Retrieve an image and Display it.
        retval, img = cam.read()
        # img = cv2.flip(img,1) # flip horizontally for correct orientation
        if not retval:
            print("Cannot capture frame device")
            exit()
        key = cv2.waitKey(1)
        if (key == ord('p')):
            break
        elif key == 27:
            print('exiting now!')
            exit(0)
        # cv2.namedWindow("Cam Feed", cv2.WINDOW_NORMAL)
        cv2.namedWindow('Cam Feed')
        cv2.imshow("Cam Feed", img)

    # Co-ordinates of objects to be tracked
    # will be stored in a list named `points`

    cv2.destroyWindow("Cam Feed")

    # Co-ordinates of objects to be tracked
    # will be stored in a list named `points`
    points = get_points.run(img)

    if not points:
        print("ERROR: No object to be tracked.")
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
    line_width = 2; delay = 0.5
    pygame.init()
    # pygame.font.init()
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
    counter = 0
    state = "idle"
    while not over:
        # Read frame from device or file
        retval, img = cam.read()
        # img = cv2.flip(img,1) # flip horizontally for correct orientation
        if not retval:
            print("Cannot capture frame device | CODE TERMINATING :(")
            exit()
        # Update the tracker
        tracker.update(img)
        # Get the position of the object, draw a
        # bounding box around it and display it.
        rect = tracker.get_position()
        pt1 = (int(rect.left()), int(rect.top()))
        pt2 = (int(rect.right()), int(rect.bottom()))
        cv2.rectangle(img, pt1, pt2, (255, 255, 255), 3)
        # print("********************************************")
        # print("Object tracked at [{}, {}]".format(pt1, pt2))
        if False: #dispLoc:
            loc = (int(rect.left()), int(rect.top()-20))
            txt = "Object tracked at [{}, {}]".format(pt1, pt2)
            cv2.putText(img, txt, loc , cv2.FONT_HERSHEY_SIMPLEX, .5, (255,255,255), 1)
        # cv2.namedWindow("Cam Feed", cv2.WINDOW_NORMAL)
        # cv2.namedWindow('Cam Feed')
        cv2.imshow("Cam Feed", img)

        # get some events
        # message = 'idle'
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                over = True
            if event.type == pygame.KEYDOWN:
                # let's see which key was pressed
                key_pressed = event.key
                if key_pressed == pygame.K_q or key_pressed == pygame.K_ESCAPE:
                    over = True
                # bluetooth events
                if bluetooth_use:
                    if key_pressed == pygame.K_UP:
                        state = 'up'
                    elif key_pressed == pygame.K_DOWN:
                        state = 'down'
                    elif key_pressed == pygame.K_RIGHT:
                        state = 'right'
                    elif key_pressed == pygame.K_LEFT:
                        state = 'left'
                    elif key_pressed == pygame.K_SPACE:
                        state = 'idle'
        # send or not?
        # print(counter)
        if bluetooth_use:
            counter += 1
            if counter >= 2:
                sock.send(state)
                counter = 0
            # print(counter, state)
            # print("you sent: {}".format(message))

        # now draw the grid, with the center of the chair or target as well
        cart_pos = ((pt1[0]+pt2[0])/2, (pt1[1]+pt2[1])/2)
        cart_pos = map(int, (cart_pos[0]/640*scr_width, cart_pos[1]/480*scr_height))
        pygame.draw.circle(screen, colors['blue'], cart_pos, 4)

        ########################################################################################33
        # drive here
        normalized_position = (cart_pos[0]-scr_width/2, cart_pos[1]-scr_height/2)
        position_in_quadrant = get_quadrant(normalized_position)
        log = "position on grid at {} >> {}".format(normalized_position, position_in_quadrant)
        print(log)

        ########################################################################################33

        # print("********************************************")
        # the following is the center
        pygame.display.update()
        pygame.display.flip()
        # time.sleep(delay)

        # Continue until the user presses ESC key
        key_pressed = cv2.waitKey(1)
        if key_pressed == 27 or key_pressed == ord('q'):
            over = True
            # pass
    # Relase the VideoCapture object
    cam.release()
    if bluetooth_use: sock.close()
    pass


def ball_detect(frame, buffer_size, color):

    lowerLimit, upperLimit = None, None
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


    # resize the frame, blur it, and convert it to the HSV
    # color space
    # frame = imutils.resize(frame, width=600)
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

    needed = True
    center_x, center_y = (0, 0)
    if needed:
        # loop over the set of tracked points
        for i in xrange(1, len(pts)):
            # if either of the tracked points are None, ignore
            # them
            if pts[i - 1] is None or pts[i] is None:
                continue

            # otherwise, compute the thickness of the line and
            # draw the connecting lines
            # thickness = int(np.sqrt(buffer_size / float(i + 1)) * 2.5)
            # cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
            center_x += pts[i][0]
            center_y += pts[i][1]

    return center


def ball_track(kwargs):
    source = int(kwargs['device'])
    bluetooth_use = int(kwargs['bluetooth'])
    color = kwargs['color']
    buffer_size = int(kwargs['buffer'])

    # set bluetooth connection
    hc06_new = '20:15:12:04:25:19' # our device's mac address
    port = 1 # this port number has been fixed now, must delete the device to change it!!!

    if bluetooth_use:
        sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        print('log: Trying to connect to {}'.format(hc06_new))
        sock.connect((hc06_new, port))
        sock.settimeout(100.0)
        print('log: Connected!')
    else:
        print('going without bluetooth')

    # Create the VideoCapture object
    cam = cv2.VideoCapture(source)

    # If Camera Device is not opened, exit the program
    if not cam.isOpened():
        print("Video device or file couldn't be opened")
        exit()

    # now initialize pygame and grid
    scr_width = 650; scr_height = 600
    grid_spacing_vertical = scr_height//2
    grid_spacing_horizontal = scr_width//2
    line_width = 2; delay = 0.5
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

    ########################buffer_size###########################################
    # now open the camera and start the grid
    over = False
    counter = 0
    state = "idle"
    angle = 0.0
    while not over:
        # Read frame from device or file
        retval, img = cam.read()
        # img = cv2.flip(img,1) # flip horizontally for correct orientation
        if not retval:
            print("Cannot capture frame device | CODE TERMINATING :(")
            exit()
        # Update the tracker
        center = ball_detect(frame=img, buffer_size=buffer_size, color=color)
        cv2.circle(img, center, 5, (0, 0, 255), -1)

        # print("********************************************")
        # print("Object tracked at [{}, {}]".format(center))
        cv2.imshow("Cam Feed", img)

        # get some events
        # message = 'idle'
        clear_screen(screen=screen, line_width=line_width, localization_grid=localization_grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                over = True
            if event.type == pygame.KEYDOWN:
                # let's see which key was pressed
                key_pressed = event.key
                if key_pressed == pygame.K_q or key_pressed == pygame.K_ESCAPE:
                    over = True
                # clear screen?
                elif key_pressed == pygame.K_c:
                    clear_screen(screen=screen, line_width=line_width, localization_grid=localization_grid)
                # bluetooth events
                elif bluetooth_use:
                    state = manned_vehicle(key_pressed, state)

        # send or not?
        # print(counter)
        if bluetooth_use:
            counter += 1
            if counter >= 2:
                sock.send(state)
                angle = sock.recv(64)
                counter = 0
            # print(counter, state)
            # print("you sent: {}".format(message))

        # now draw the grid, with the center of the chair or target as well
        if center != None and len(center) == 2:
            cart_pos = (center[0], center[1])
            cart_pos = map(int, (cart_pos[0]/640*scr_width, cart_pos[1]/480*scr_height))
            pygame.draw.circle(screen, colors['blue'], cart_pos, 4)

            ########################################################################################33
            # drive here
            normalized_position = (cart_pos[0]-scr_width/2, -(cart_pos[1]-scr_height/2))
            position_in_quadrant = get_quadrant(normalized_position)
            log = "position on grid at {} >> {}; current angle = {}".format(normalized_position,
                                                                            position_in_quadrant, angle)
            print(log)

            ########################################################################################33

        # print("********************************************")
        # the following is the center
        pygame.display.update()
        pygame.display.flip()
        # time.sleep(0.1)

        # Continue until the user presses ESC key
        key_pressed = cv2.waitKey(1)
        if key_pressed == 27 or key_pressed == ord('q'):
            over = True
            # pass
    # Relase the VideoCapture object
    cam.release()
    if bluetooth_use: sock.close()
    pass


def clear_screen(screen, line_width, localization_grid):
    white = (255, 255, 255)
    black = (0, 0, 0)
    screen.fill(white)

    # draw the localization grid
    for points in localization_grid[:, ]:
        pygame.draw.lines(screen, black, False, [points[0], points[1]], line_width)
        pygame.draw.lines(screen, black, False, [points[2], points[3]], line_width)

    pass


def get_quadrant(cart_position):
    # global position on the grid
    scr_center_x = 0
    scr_center_y = 0

    x, y = cart_position
    if x >= scr_center_x and y < scr_center_y:
        position = 'Quad_1'
        return position
    elif x < scr_center_x and y < scr_center_y:
        position = 'Quad_2'
        return position
    elif x < scr_center_x and y >= scr_center_y:
        position = 'Quad_3'
        return position
    elif x >= scr_center_x and y >= scr_center_y:
        position = 'Quad_4'
        return position


def drive(location, angle, desired_loc=(0,0)):
    diff = desired_loc-location

    pass


def manned_vehicle(key_pressed, state):
    if key_pressed == pygame.K_UP:
        state = 'up'
    elif key_pressed == pygame.K_DOWN:
        state = 'down'
    elif key_pressed == pygame.K_RIGHT:
        state = 'right'
    elif key_pressed == pygame.K_LEFT:
        state = 'left'
    elif key_pressed == pygame.K_SPACE:
        state = 'idle'
    return state


if __name__ == "__main__":
    # Parse command line arguments
    parser = ap.ArgumentParser()
    parser.add_argument('-d', "--deviceID", dest='device', help="Device ID")
    parser.add_argument('-b', "--bluetooth", dest='bluetooth', help="bluetooth")
    parser.add_argument('-f', "--function", dest='function', help="which function to call?")
    parser.add_argument('-buf', "--buffer", dest='buffer', help="buffer size")
    parser.add_argument('-c', "--color", dest='color', help="which color")

    args = vars(parser.parse_args())
    func = eval(args['function'])
    func(args)






