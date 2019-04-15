import cv2
import numpy as np
import os

#########################################################
###   detect circle / obstacles in the table region  ####
#########################################################

def detectShapesInTable(img_name, centerx, centery, table_halfw, table_halfh ):
        path_filename = os.path.join("Output", "snapshots", img_name) #
        print("path ", path_filename)
        img2 = cv2.imread(path_filename)
        print(img_name)
        #### detect circle . If not satisfied, keep pressing space key for re-detection.######
        ## mask out the table from the zoomed out image
        rec_mask = np.zeros(img2.shape[:2],np.uint8)
        pad = 5
        rec_mask[centery-table_halfh+pad:centery+table_halfh-pad,centerx-table_halfw+pad:centerx+table_halfw-pad] = 255
        masked_frame = cv2.bitwise_and(img2,img2, mask =rec_mask)

        gray = cv2.cvtColor(masked_frame, cv2.COLOR_BGR2GRAY)
        # detect circles in the image
        circles = cv2.HoughCircles(image=gray, method=cv2.HOUGH_GRADIENT, dp=1.6, minDist=100,
                                   param1=50,param2=70,minRadius=20,maxRadius=100)

        # ensure at least some circles were found
        if circles is not None:
            # convert the (x, y) coordinates and radius of the circles to integers
            circles = np.round(circles[0, :]).astype("int")
            # loop over the (x, y) coordinates and radius of the circles
            # remove circles out side of defined table region
            ind = 0
            print("circles:", circles)
            index_to_keep =[]

            for (x, y, r) in circles:
                    # draw the circle in the output image, then draw a rectangle
                    # corresponding to the center of the circle
                    cv2.circle(img2, (x, y), r, (0, 255, 0), 4)

        ###### detect obstacles
        gray = cv2.cvtColor(masked_frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.bilateralFilter(gray, 11, 17, 17)
        edged = cv2.Canny(gray, 30, 200)

        # find contours in the edged image, keep only the largest
        # ones, and initialize our screen contour
        # im2, contours, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # (new 2019)

        contours = sorted(contours, key = cv2.contourArea, reverse = True)[:10]


        detecting_frame = img2.copy()

        return circles, detecting_frame
