import cv2
import imutils
from save import save_output_at
import time
from shape_detection import detectShapesInTable
import pickle
import os

####################################################
###   take a snap shot of a board from webcam   ####
####################################################
def take_snapshot(args, width, centerx, centery, table_halfw, table_halfh, timeTag, camera_port):
    cam = cv2.VideoCapture(camera_port)
    cv2.namedWindow("test")
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
