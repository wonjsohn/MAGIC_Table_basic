#!/usr/bin/env python
# -*- coding: utf-8 -*-

# USAGE: You need to specify a filter and "only one" image source
#
# (python) range-detector --filter BGR --image opencv_frame_video.png
# or
# (python) range-detector --filter HSV --webcam

import cv2
import argparse
from operator import xor
import numpy as np
import imutils


def callback(value):
    pass


def setup_trackbars(range_filter, bgrindex):
    # bmin, gmin, rmin, bmax, gmax, rmax
    cv2.namedWindow("Trackbars", 0)
    cv2.resizeWindow("Trackbars", 200, 200);
    
    k=0
    
    for i in ["MIN", "MAX"]:
        v = 0 if i == "MIN" else 255

        for j in range_filter:
            cv2.createTrackbar("%s_%s" % (j, i), "Trackbars", v, 255, callback)
            print(bgrindex[k])
            cv2.setTrackbarPos("%s_%s" % (j, i), "Trackbars", bgrindex[k])
            k = k + 1 
    
    
def get_arguments():
    ap = argparse.ArgumentParser()
    ap.add_argument('-f', '--filter', required=True,
                    help='Range filter. RGB or HSV')
    ap.add_argument('-i', '--image', required=False,
                    help='Path to the image')
    ap.add_argument('-w', '--webcam', required=False,
                    help='Use webcam', action='store_true')
    ap.add_argument('-p', '--preview', required=False,
                    help='Show a preview of the image after applying the mask',
                    action='store_true')
    ap.add_argument('-v', '--valsBGR', nargs='+', required=False, type = int, help='BGR values',
                    default=(24, 142, 0, 120, 255, 255)) # light green
                    #default = (44, 170, 114, 243, 219, 255))
                    #best greenfileter: (24, 76, 0, 120, 199, 255) #  0, 204, 0

                    #green filter:(29, 86, 6, 64, 255, 255)
                    #yellow: (16, 54, 40, 45, 255, 255)
                    #blue: (30, 211, 0, 120,  255, 255)
                    # orange: (0, 141, 112, 243, 255, 255)
                    # light green/red (44, 170, 114, 243, 219, 255)
    
    args = vars(ap.parse_args())

    if not xor(bool(args['image']), bool(args['webcam'])):
        ap.error("Please specify only one image source")

    if not args['filter'].upper() in ['BGR', 'HSV']:
        ap.error("Please speciy a correct filter.")

    return args


def get_trackbar_values(range_filter):
    values = []

    for i in ["MIN", "MAX"]:
        for j in range_filter:
            v = cv2.getTrackbarPos("%s_%s" % (j, i), "Trackbars")
            values.append(v)

    return values


def main():
    args = get_arguments()
    camera_port = 2

    bgrindex = args['valsBGR'] #[bmin, gmin, rmin, bmax, gmax, rmax
    #print bgrindex
    print(bgrindex)
    range_filter = args['filter'].upper()

    if args['image']:
        image = cv2.imread(args['image'])

        if range_filter == 'BGR':
            frame_to_thresh = image.copy()
        else:
            frame_to_thresh = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    else:
        camera = cv2.VideoCapture(camera_port)

    setup_trackbars(range_filter, bgrindex)

    while True:
        if args['webcam']:
            ret, image = camera.read()
            image = imutils.resize(image, width=480)
 #          cv2.resize(img_dilation, (360, 240))

            if not ret:
                break

            if range_filter == 'BGR':
                #frame_to_thresh = image.copy()
                frame_to_thresh = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            else:
                frame_to_thresh = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        v1_min, v2_min, v3_min, v1_max, v2_max, v3_max = get_trackbar_values(range_filter)

        hsvmask = cv2.inRange(frame_to_thresh, (v1_min, v2_min, v3_min), (v1_max, v2_max, v3_max))
        # print "Bmin:", v1_min, " Gmin:", v2_min, " Rmin", v3_min, ", Bmax:", v1_max, " Gmax:", v2_max," Rmax:", v3_max
        print("Bmin:", v1_min, " Gmin:", v2_min, " Rmin", v3_min, ", Bmax:", v1_max, " Gmax:", v2_max," Rmax:", v3_max)


        kernel = np.ones((2,2), np.uint8)
        img_erosion = cv2.erode(hsvmask, kernel, iterations=1)
        img_dilation = cv2.dilate(img_erosion, kernel, iterations=5)
        if args['preview']:
  
            #preview = cv2.bitwise_and(image, image, mask=hsvmask)
            cv2.imshow("Preview", img_dilation)
        else:
 
            cv2.imshow("Original", image)
            cv2.imshow("Thresh", img_dilation)
            

        if cv2.waitKey(1) & 0xFF is ord('q'):
            break


if __name__ == '__main__':
    main()
