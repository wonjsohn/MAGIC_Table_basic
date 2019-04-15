import cv2
import imutils
from save import save_output_at
import time
from shape_detection import detectShapesInTable
import pickle
import numpy as np
import glob
import os

####################################################
###   take a snap shot of a board from webcam   ####
####################################################
def take_snapshot(args, width, centerx, centery, table_halfw, table_halfh, timeTag, camera_port, screen_w,screen_h):
    cam = cv2.VideoCapture(camera_port)
    cv2.namedWindow("test")
    """ Window positioning """
    cv2.moveWindow("test", screen_w - 758 - 640 , 0)  # Move it to (x, y)


    """ instruction window """
    # Create a black image (by Rashida)
    instructions = np.zeros((480, 640, 3), np.uint8)

    # Write some Text

    font = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (10, 100)
    fontScale = .7
    fontColor = (255, 255, 255)
    lineType = 2

    cv2.putText(instructions, 'Snapshot Instructions',
                (10, 50),
                font,
                fontScale,
                fontColor,
                lineType)

    cv2.putText(instructions, '1. Remove cup from camera view',
                bottomLeftCornerOfText,
                font,
                fontScale,
                fontColor,
                lineType)

    cv2.putText(instructions, '2. Press Space Bar to take a snapshot',
                (10, 200),
                font,
                fontScale,
                fontColor,
                lineType)

    cv2.putText(instructions, 'Press Space Bar again if shape detection unsatisfactory',
                (10, 300),
                font,
                fontScale,
                fontColor,
                lineType)

    cv2.putText(instructions, '3. Once you are satisfied place cup back on table ',
                (10, 400),
                font,
                fontScale,
                fontColor,
                lineType)

    cv2.putText(instructions, '4. Press Esc to start trial ',
                (10, 500),
                font,
                fontScale,
                fontColor,
                lineType)
    #
    # # Display the image

    cv2.namedWindow("instruction")
    cv2.moveWindow("instruction", screen_w - 758 - 640 , 480)  # Move it to (x, y)
    cv2.imshow("instruction", instructions)

    img_counter = 0

    while True:
        ret, frame = cam.read()
        
        frame = imutils.resize(frame, width=width)
        frame_copy = frame.copy() # copy for distortion matrix

        cv2.circle(frame, (centerx, centery), 4, (0, 0, 255), 4)
        cv2.rectangle(frame, (centerx- table_halfw, centery - table_halfh), (centerx + table_halfw, centery+ table_halfh), (153, 255, 255), 3)
        cv2.circle(frame, (centerx- table_halfw, centery - table_halfh), 8, (0, 0, 255), 4)
        cv2.circle(frame, (centerx- table_halfw, centery + table_halfh), 8, (0, 0, 255), 4)
        cv2.circle(frame, (centerx+ table_halfw, centery - table_halfh), 8, (0, 0, 255), 4)
        cv2.circle(frame, (centerx+ table_halfw, centery + table_halfh), 8, (0, 0, 255), 4)
            
        if img_counter == 0:
            cv2.imshow("test", frame)
        else:
            cv2.imshow("test", detecting_frame)
            
        if not ret:
            break
        k = cv2.waitKey(1)
        
        if k%256 == 27:
            # ESC pressed
            if img_counter > 0:
                dataOutput_path= save_output_at("snapshots")
                cv2.imwrite(os.path.join(dataOutput_path, timeTag+'.jpg'), prev_frame) # save snapshot image # FIX:CROSS PLATFORM
                dataOutput_path= save_output_at("pickles")
                savefile_circles = os.path.join(dataOutput_path, timeTag+'_circles.dump' )# FIX:CROSS PLATFORM
                pickle.dump(circles, open(savefile_circles, 'wb'))   # save circle characteristics
                pickle.dump(timeTag, open("lastTimeTag.dump", 'wb')) # save the latest time tag.
                print("{} written!".format(savefile_circles))

            print("Escape hit, closing...")
            break
        elif k%256 == 32:
            # SPACE pressed
            dataOutput_path= save_output_at("snapshots")
            img_name = timeTag+".jpg"
            cv2.imwrite(os.path.join(dataOutput_path, timeTag+'.jpg'), frame)

            time.sleep(1)
            circles, detecting_frame = detectShapesInTable(img_name,  centerx, centery, table_halfw, table_halfh)

            prev_frame = frame.copy()
            img_counter += 1

    cam.release()
    cv2.destroyAllWindows()
    print(img_name)
    return img_name, circles
