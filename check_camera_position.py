import cv2
import imutils

####################################################
###   take a snap shot of a board from webcam   ####
####################################################
def check_camera(args, width, centerx, centery, table_halfw, table_halfh, timeTag, camera_port):
    cam = cv2.VideoCapture(camera_port)
    cv2.namedWindow("Position_check")

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
            
