

"""

    The following is our project for our instruments and measurements course
"""

from __future__ import print_function
from __future__ import division

import cv2
import numpy as np


def get_diff_image(prev_prev, prev, current):

    """
        basically calculates the difference of 3 frames for background cancellation
    :param prev_prev: at t-2
    :param prev: at t-1
    :param current: at t
    :return: diff image of the last three frames
    """

    diff_1 = cv2.absdiff(current, prev)
    diff_2 = cv2.absdiff(prev, prev_prev)
    return cv2.bitwise_and(diff_1, diff_2)


def get_bounding_boxes(img, contours):
    """
        this function converts contours into bounding rectangles
    :param img:
    :param contours:
    :return:
    """
    for cnt in contours:
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        print(box)
        cv2.drawContours(img, [box], 0, (0, 0, 255), 2)
    return img


def get_enclosing_circle(img, contours):
    """
        this function converts contours into bounding circles
    :param img:
    :param contours:
    :return:
    """

    for cnt in contours:
        (x, y), radius = cv2.minEnclosingCircle(cnt)
        center = (int(x), int(y))
        radius = int(radius)
        if radius >= 40:
            cv2.circle(img, center, radius, (0, 255, 0), 5)
    return img



def detect_motion():

    # get the image feed and store 3 frames at each time step
    camera = cv2.VideoCapture(0)
    _, current_frame = camera.read() # get some initial settings
    # we'll make our diff_frame a difference of 3 consecutive frames for background cancellation
    # and after reading them, must convert them to gray scale first
    prev_prev_frame = cv2.cvtColor(cv2.medianBlur(camera.read()[1], ksize=5), cv2.COLOR_BGR2GRAY)
    prev_frame = cv2.cvtColor(cv2.medianBlur(camera.read()[1], ksize=5), cv2.COLOR_BGR2GRAY)
    current_frame_rbg = cv2.medianBlur(camera.read()[1], ksize=5)
    current_frame = cv2.cvtColor(current_frame_rbg, cv2.COLOR_BGR2GRAY)

    window_name = 'Video Feed'; cv2.namedWindow(winname=window_name)
    while(True):
        diff_frame = get_diff_image(prev_prev=prev_prev_frame, prev=prev_frame, current=current_frame)
        # gray_frame = cv2.cvtColor(diff_frame, cv2.COLOR_BGR2GRAY)
        # (thresh, binarized_frame) = cv2.threshold(diff_frame, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        # binarize with adaptive threshold
        binarized_frame = cv2.adaptiveThreshold(diff_frame.astype(np.uint8), 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                                cv2.THRESH_BINARY, 41, 3)
        # find the contours in this image
        # contours = None
        im, contours, hierarchy = cv2.findContours(binarized_frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # draw those contours now
        # cv2.drawContours(current_frame_rbg, contours, -1, (0,255,0), 3)
        # cv2.drawContours(current_frame_rbg, contours, -1, (0, 255, 0), 3)

        # get circles bounding these contours
        current_frame_rbg = get_enclosing_circle(img=current_frame_rbg, contours=contours)

        # get rects bounding these contours
        # current_frame_rbg = get_bounding_boxes(img=current_frame_rbg, contours=contours)

        # or may be draw bounding boxes
        if False:
            for component in zip(contours, hierarchy):
                currentContour = component[0]
                # currentHierarchy = component[1]
                x, y, w, h = cv2.boundingRect(currentContour)
            #     if len(currentHierarchy) > 1:
                    # if currentHierarchy[2] < 0:
                        # these are the innermost child components
                cv2.rectangle(current_frame_rbg, (x, y), (x + w, y + h), (0, 0, 255), 3)
                    # elif currentHierarchy[3] < 0:
                        # these are the outermost parent components
                        # cv2.rectangle(current_frame_rbg, (x, y), (x + w, y + h), (0, 255, 0), 3)




        # cv2.drawContours(current_frame_rbg, contours, -1, (0, 255, 0), 3)
        # prev_frame = current_frame
        cv2.imshow(window_name, current_frame_rbg)

        # update the image frames
        prev_prev_frame = prev_frame
        prev_frame = current_frame
        current_frame_rbg = cv2.medianBlur(camera.read()[1], ksize=5)
        current_frame = cv2.cvtColor(current_frame_rbg, cv2.COLOR_BGR2GRAY)

        if cv2.waitKey(delay=10) == 27:
            break # basically this means ESC key

    cv2.destroyAllWindows()
    pass


def flip_horizontal(source):
    #flip the img horizontally
    img = source.reshape(-1, 96, 96)
    img = np.flip(img, axis=2)
    img = img.reshape(-1, 96*96)
    return img


def detect_lines(source):

    current_frame = cv2.cvtColor(source, cv2.COLOR_BGR2GRAY)
    # detector = cv2.LineSegmentDetector()
    detector = cv2.createLineSegmentDetector()
    lines = detector.detect(current_frame)[0]
    return detector.drawSegments(current_frame, lines)



def main():
    """
        We will use this function to apply some transformations on our camera feed
    :return:
    """

    cam = cv2.VideoCapture(1)
    # while cam.read()[1].empty:
    #     pass

    kernel_1 = np.asarray([[-1,-2,-1],[0,0,0],[1,2,1]])
    kernel_2 = np.transpose(kernel_1)
    while True:
        frame = cam.read()[1]
        # frame = np.flip(cam.read()[1], axis=1)
        trans_frame_1 = cv2.filter2D(src=frame, ddepth=-1, kernel=kernel_1)
        trans_frame_2 = cv2.filter2D(src=frame, ddepth=-1, kernel=kernel_2)
        combined_trans = np.add(trans_frame_1, trans_frame_2)
        edge_enhanced_image = np.add(frame, combined_trans)
        # show_frame = np.hstack((frame, combined_trans))
        show_frame = np.hstack((frame, combined_trans))
        # cv2.imshow('Video feed', show_frame)
        cv2.imshow('Video feed', detect_lines(frame))
        if cv2.waitKey(1) == 27: # esc key
            break
    pass




if __name__ == '__main__':
    main()


















