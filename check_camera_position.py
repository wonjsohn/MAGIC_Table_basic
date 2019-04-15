import cv2
import imutils
import numpy as np
import pygame

####################################################
###   take a snap shot of a board from webcam   ####
####################################################
def check_camera(args, width, centerx, centery, table_halfw, table_halfh, timeTag, camera_port, screen_w, screen_h):
    cam = cv2.VideoCapture(camera_port)
    cv2.namedWindow("Position_check")

    """ Window positioning """
    print('current screen: ', screen_w, screen_h)
    cv2.moveWindow("Position_check", screen_w - 758 - width , 0)  # Move it to (x, y), 758 is GUI width


    """ instruction window """
    # Create a black image (By Rashida)
    img = np.zeros((480, 640, 3), np.uint8)
    # Write some Text
    font = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (10, 100)
    fontScale = .7
    fontColor = (255, 255, 255)
    lineType = 2

    cv2.putText(img, 'OPTION 1: Press Esc to Start Trial',
                bottomLeftCornerOfText,
                font,
                fontScale,
                fontColor,
                lineType)

    cv2.putText(img, '      OR',
                (10, 200),
                font,
                1.5,
                fontColor,
                lineType)

    cv2.putText(img, 'OPTION 2: Press s to take a Snapshot (on the initial trial only)',
                (10, 300),
                font,
                fontScale,
                fontColor,
                lineType)

    cv2.namedWindow("instruction")
    cv2.moveWindow("instruction", screen_w - 758 - width, 480)  # Move it to (x, y)
    cv2.imshow("instruction", img)

    while True:
        ret, frame = cam.read()
        frame = imutils.resize(frame, width=width)        

        cv2.circle(frame, (centerx, centery), 4, (0, 0, 255), 4)
        cv2.rectangle(frame, (centerx- table_halfw, centery - table_halfh), (centerx + table_halfw, centery+ table_halfh), (153, 255, 255), 3)
        cv2.line(frame, (0, centery), (frame.shape[1], centery), (255, 0, 255), thickness=3, lineType=8)
        cv2.line(frame, (centerx, 0), (centerx, frame.shape[0]), (255, 0, 255), thickness=3, lineType=8)
        cv2.circle(frame, (centerx- table_halfw, centery - table_halfh), 8, (255, 0, 255), 4)
        cv2.circle(frame, (centerx- table_halfw, centery + table_halfh), 8, (255, 0, 255), 4)
        cv2.circle(frame, (centerx+ table_halfw, centery - table_halfh), 8, (255, 0, 255), 4)
        cv2.circle(frame, (centerx+ table_halfw, centery + table_halfh), 8, (255, 0, 255), 4)
        cv2.imshow("Position_check", frame)
        
        if not ret:
            break
        k = cv2.waitKey(1)
        
        if k%256 == 27:
            # ESC pressed             
            print("Escape hit, closing...")
            need_to_take_snapshot = False
            break
        elif k%256 == 83 or k%256 == 115:  ## S or s (for snapshot)
            need_to_take_snapshot = True
            break

    cam.release()
    cv2.destroyAllWindows()
    return need_to_take_snapshot
            
