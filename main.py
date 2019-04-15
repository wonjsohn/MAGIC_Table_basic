__author__ = 'wonjoonsohn'

# -*- coding: utf-8 -*-
############## Local library  ###########################
from snapshots import take_snapshot
from arguments import get_arguments
from shape_detection import  detectShapesInTable
from save import save_output_at, save_video_os, save_dataframe_os
from check_camera_position import check_camera

################### openCV etc.##########################
import numpy as np
import pandas as pd
import pickle
import cv2
import imutils
from imutils.video import FileVideoStream
from imutils.video import WebcamVideoStream
from imutils.video import VideoStream
from imutils.video import FPS
from threading import Thread
from collections import deque
import sys
from scipy import misc
import os
import time
import datetime
import csv

############### popup GUI ############################
from PyQt5 import uic
from PyQt5 import QtCore, QtGui, QtWidgets


##########################################################

####################################################
################  definitions ######################
####################################################
camera_port =0 # Depending on the usb port, it can be 0, 1, 2....

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the

orangeLower = (0, 141, 112) # BGR oramnge postit. 
orangeUpper = (243, 255, 255)  # BGR  orange postit

def ellipse_tracking(hsvmask):
    #########################################################
    ##### track minimum enclosing elipse of this mask #######
    #########################################################
    hsv = hsvmask
    hsvmask = cv2.inRange(hsv, orangeLower, orangeUpper) # cheap
    kernel = np.ones((5,5), np.uint8)
    img_erosion = cv2.erode(hsvmask, kernel, iterations=1)       #
    img_dilation = cv2.dilate(img_erosion, kernel, iterations=3) # erode/dial: 1.3ms

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(img_dilation.copy(), cv2.RETR_EXTERNAL, # 0.5ms
            cv2.CHAIN_APPROX_SIMPLE)[-2]
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:2]
    center = None
    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid

        (x,y),(MA,ma),angle = cv2.fitEllipse(cnts[0])

        x_center = width/2
        y_center = height/2
        ### Projection down to xy plane. Adjustment based on cup height. ######
        #x_adjust = ((lens_h-cup_h)/lens_h)*(x-x_center)
        #y_adjust = ((lens_h-cup_h)/lens_h)*(y-y_center)
        x_adjust = x - x_center
        y_adjust = y - y_center

        xObject = x_center+x_adjust
        yObject = y_center+y_adjust
    else:
        xObject = -1
        yObject = -1
        radius = -1
        MA = 0 
        ma = 0
        angle = 0

    return (xObject, yObject,  MA, ma, angle,  len(cnts))


####################################################
###                    main                     ####
####################################################
def run_main(timeTag):
    ## KEYBOARD command:  esc / "q" key to escape, "d" / "D" key to delete the trial.
    print("KEYBOARD command:  esc / q key to escape, d / D key to delete the trial.")

    """ get screen resolution info"""
    pygame.init()
    screen_w = pygame.display.Info().current_w
    screen_h = pygame.display.Info().current_h
    pygame.quit() # check if this line needs to be disabled

    global width, height, lens_h, cup_h
    width = 640
    height = 480 #360
    lens_h = 0.8 #Lens vertical height 
    cup_h = 0.08 #Cup surface height

    global running 
    running = True
    # color filter range for calcHist
    
    pts = deque(maxlen=args["buffer"])
    pts_orig = deque(maxlen=args["buffer"])

############  camera alignment ###############
    centerx = int(width/2)
    centery = int(height/2)
    #  new table inner dimension: 87cm x 57cm.  (34x22)
    magfactor = 3
    table_width_in_cm = 87
    table_height_in_cm = 57
    table_halfw = table_width_in_cm*magfactor# (large), smaller: 230 table half-width approx. unit in px
    table_halfh = table_height_in_cm*magfactor# # table half-height approx.  # unit in px.

    ### Check if you need another snapshot during experiment due to disturbed camera or table.
    need_to_take_snapshot= False
    need_to_take_snapshot= check_camera(args, width, centerx, centery,table_halfw, table_halfh, timeTag, camera_port, screen_w,screen_h)

    ### take a snapshot of the board in png
    if need_to_take_snapshot:  #
        img_name, circles =take_snapshot(args, width, centerx, centery,table_halfw, table_halfh, timeTag, camera_port, screen_w,screen_h)
    else: #if args.get("video", False):  
        print("load snapshot, load pickle data")

        # just loading snapshot
        lastTimeTag = pickle.load(open("lastTimeTag.dump", 'rb'))
        print("last time tag",lastTimeTag)

        timetag_circles = lastTimeTag + "_circles.dump"
        print(timetag_circles)

        circles = pickle.load(open(os.path.join("Output", "pickles", timetag_circles), 'rb'))
        img_name = lastTimeTag+".png"

        #####  make a copied pickle data with new timeTag  ###########
        dataOutput_path= save_output_at("pickles")
        savefile_circles = os.path.join(dataOutput_path, timeTag+"_circles.dump")

        pickle.dump(circles, open(savefile_circles, 'wb'))   # save circle characteristics
        pickle.dump(timeTag, open("lastTimeTag.dump", 'wb')) # save the latest time tag.

        """ test pick dump multiple """
        print("{} written!".format(savefile_circles))

    print("Image name: ", img_name)

    ###  grab the reference to the camera
    if args.get("thread", False):
        print("thread  started #################################")
        cap = WebcamVideoStream(src=camera_port).start()
    else:
        cap = cv2.VideoCapture(camera_port)

    fps = FPS().start()
    time.sleep(1.0)
           
    # Read the first frame of the video
    if args.get("thread", False):
        frame = cap.read()
    else:
        ret, frame = cap.read()

    # sound effect related
    startCirclefx, endCirclefx, obstablefx, GoSound = sound_effects()

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*args["codec"])

    writer = None
    writer_raw = None
    (h, w) = (None, None)
    zeros = None

    # Cup data to write to file
    dataOut = []
    elapsedTimeList = []
    xObjectList = []
    yObjectList = []
    start_cueList = []
    startTimeList = []
    reachTimeList = []
    goalReachedList = []
    # pandas dataframe output
    data = pd.DataFrame([])

    # Start time
    startTime = time.time()*1000.0
    startTimeRaw = time.time()
    startTimeFormatted = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S:%f")[:-3]
    ###%%%%%% convert to human readable: datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S.%f')

    num_frames = 0
    start_cue = 0
    delete_trial = 0 # whether to delete this trial because it is bad trial
    soundplayed = 0
    inTargetzone = 0  #  in P2P, you are in target zone.
    forceQuit = 0  # when you press 'c' to force quit at the end OR time is up.
    reach_time = 0
    targetzone_time = 0
    reach_time_start = 0
    marker = 0
    in_circle = 0

#########################################################
####################### pygame sound ####################
#########################################################
    if args["mode"] =="pygame":
        pygame.mixer.music.play(-1)


    cv2.namedWindow('main') # main window name
    """ Window positioning """
    cv2.moveWindow("main", 515, 0)  # Move it to (x, y)


################################################
############### main loop  #####################
################################################
    while running:
        if args.get("thread", False): # cheap
            frame_orig = cap.read()
            frame_raw = frame_orig.copy()
        else:
            ret, frame_orig = cap.read()
            if not ret:
                break

        """ Resize the frame to increase speed."""
        frame = imutils.resize(frame_orig, width=width)
        if not args.get("video", False):  # NOT a postprocessing mode
            frame_raw = imutils.resize(frame_raw, width=width)
        t = time.time()

        if args.get("timed", False) > 0:  # time limit was set in -t argument.
            if args["tasktype"]=="p2p":
                if inTargetzone >0 and marker == 0: # end the trial when goal is reached.
                   reach_time = time.time()*1000 - startTime
                   print(reach_time)
                   targetzone_time = time.time()*1000 # the time when the cup entered the target
                   marker = 1

            if  start_cue < 1 and time.time()*1000.0 - startTime > 1*1000.0:  # start go sound at 1 second.
                GoSound.play(0)
                start_cue = 1

            if  time.time()*1000.0 - startTime > args.get("timed", False) * 1000.0:  # in seconds (termination time)                           
                seconds = (time.time()*1000.0 - startTime)/1000.0
                #if args['tasktype'] == "fig8":
                forceQuit = 1
                # Calculate frames per second
                fps_calc  = num_frames / seconds;
                print("Time taken: ", args.get("timed", False), "s, fps: {0}".format(fps_calc))
                break

        # check if the writer is None
        if writer is None:
            # store the image dimensions, initialzie the video writer,
            # and construct the zeros array
            if args.get("video", False):  # postprocessing mode
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            else:
                width = width  # 640
                height = height  # 360 (480 doesn't write to file)

            videoName_path = save_video_os(args, timeTag)

            print('fourcc:', fourcc)
            print('w, h:', width, height)
            writer = cv2.VideoWriter(videoName_path, fourcc, args["fps"],
                                     (width, height), True)
            zeros = np.zeros((height, width), dtype="uint8")

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  # expensive 1.5ms

########  Choose the type of tracking algorithm. ########################
### "el_object" - minimum enclosing elipse. (better when cup is warped toward the edge)
########################################################################
        global xObject, yObject    # have to check if making these global slows down.  WJS.

        if args["marker"] == "el_object": # track ellipse ball
            (xObject, yObject, MA, ma, angle, len_cnts) = ellipse_tracking(hsv)

            if len_cnts > 0:
                # only proceed if the radius meets a minimum size
                if args["trace"] > 0:
                    if int(MA/2+ma/2) > 10 & int(MA/2+ma/2) < 100:
                        # draw the circle and centroid on the frame,
                        # then update the list of tracked points
                        cv2.ellipse(frame,(int(xObject),int(yObject)),(int(MA/2), int(ma/2)),int(angle),0,360,(0,255,0), 3)
                        cv2.circle(frame, (int(xObject),int(yObject)), 5, (0, 0, 255), -1)
            cupx = xObject
            cupy = yObject

        """ P2P: Determine the starting and ending target based on initial coordinate"""
        if args["tasktype"] == "p2p":
            if num_frames == 0: # run only in the first frame, causes no delay.
                if math.hypot(cupx- circles[0][0], cupy-circles[0][1]) < circles[0][2]:
                    start_cicle_ind = 0
                    end_cicle_ind = 1
                elif math.hypot(cupx- circles[1][0], cupy-circles[1][1]) < circles[1][2]:
                    start_cicle_ind = 1
                    end_cicle_ind = 0
                else:
                    start_cicle_ind = 1
                    end_cicle_ind = 0
                    print('cup xObject:', cupx,  ' cup yObject:', cupy)
                    #raise RuntimeError("Cup is not positioned in the start circle.")
                start_x = circles[start_cicle_ind][0]
                start_y = circles[start_cicle_ind][1]
                start_r = circles[start_cicle_ind][2]
                end_x = circles[end_cicle_ind][0]
                end_y = circles[end_cicle_ind][1]
                end_r = circles[end_cicle_ind][2]

        currentTime = time.time()*1000
        elapsedTime = currentTime- startTime

        elapsedTimeList.append(elapsedTime)
        start_cueList.append(start_cue)
        startTimeList.append(startTimeRaw)
        reachTimeList.append(reach_time)
        xObjectList.append(xObject)
        yObjectList.append(yObject)


        pts.appendleft((int(xObject), int(yObject)))

        ### Drawing clock, line trace, and traces. (even if display=0, it can be written to file)
        if args["clock"] > 0:
            drawClock(frame, num_frames, elapsedTime, timeTag, virtual=0)
            # if not args.get("video", False):  # NOT a postprocessing mode
            #     drawClock(frame_raw, num_frames, elapsedTime, timeTag, virtual=0)


        if len(pts) > 100:
            pts_draw = pts[:100] # keep last 100 points to draw line.
        else:
            pts_draw = pts

        """###### line trace  ######"""
        if args["linetrace"] > 0:
            # loop over the set of tracked points (improve to be < O(n))
            for i in range(1, len(pts_draw)):  # what is xrange in python2 is range in python 3
                    if pts_draw[i - 1] is None or pts_draw[i] is None:
                            continue
                    # draw the connecting lines
                    thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
                    cv2.line(frame, pts_draw[i - 1], pts_draw[i], (255, 0, 0), thickness)#blue  (circle)

        """  Cursor potision - In or out of target """
        if args["tasktype"] == "p2p":
            if math.hypot(cupx - start_x, cupy - start_y) < start_r:
                print("in the starting circle")
            if math.hypot(cupx - end_x, cupy - end_y) < end_r:
                inTargetzone = 1
                print("in the end circle")
                in_circle=1
            else:
                in_circle=0

        ###############  audiovidual feedback  ##################
        ## This is very cheap operation
        if args["targetsound"] > 0:  # sound at target
            if args["tasktype"] == "p2p":
                if in_circle:
                    endCirclefx.play(0)  # play once
        if args["targetvisual"] >0:
            if args["tasktype"] == "p2p":
                if in_circle:
                    if num_frames % 8 == 0:  # blinks
                        cv2.circle(frame, (int(end_x), int(end_y)), end_r, (0, 0, 255),  thickness=5)

        """ display"""
        if args["display"] > 0:
            cv2.imshow("main", frame)  # expensive

        ###########  KEYBOARD INPUTS (typical) ##############
	# if the 'q' key is pressed, stop the loop
        k= cv2.waitKey(1) & 0xFF   # very expensive. 19ms. # default output = 255 (at least in python 3.6)
        if k == 27: # esc (Break and save)
            break
        elif k == 67 or k == 99: # "C" and "c" key: completed the fig8 task.
            inTargetzone = 1
            break
        elif k == 68 or k==100: # "D" and "d" key: delete.
            delete_trial = 1
            break

        ############
        # write the frame
        writer.write(frame)  # 1.3ms

        prev_num_frames = num_frames
        num_frames = num_frames + 1
        fps.update()  # update the FPS counter
        
    ### stop the timer and display FPS information
    fps.stop()
    
    print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
    print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))


    """ with meta data written on top """
    if not delete_trial:
        data = pd.DataFrame(
            {'elapsedTime': elapsedTimeList, 'xObject': xObjectList, 'yObject': yObjectList,
             'reachTime': reachTimeList,
             'startCue': start_cueList
             })


        """ GUI popup to ask if the trial was a success"""
        # x = int(input("Was this trial a success?  Y(1) or N(0) "))
        # replace with GUI to ask if this was a successful trial.
        import graphical_panel.popup_window as POPUP
        app = QtWidgets.QApplication(sys.argv)
        w = POPUP.Window()
        # w.setWindowTitle('User Input')
        # w.show()
        retval = [None] * 3
        i = 0
        for ch in w.get_data():
            retval[i] = ch
            i = i + 1
        isSuccess = retval[0]
        print('what does it say: ', isSuccess)
        note = retval[2]

        """ handedness considerations. """
        if args['tasktype'] =='p2p':
            if start_x <= centerx:
                if args['handedness']=="r": # right hander
                    dir_of_move = 'ow'
                else:
                    dir_of_move = 'iw'
            else:
                if args['handedness'] == "r":  # right hander
                    dir_of_move = 'iw'
                else:
                    dir_of_move = 'ow'

        else:
            dir_of_move = 'any'

        sharedFileName = save_dataframe_os(data, args, timeTag, isSuccess, note, dir_of_move)  # write dataframe to file
    writer.release()

    if not args['thread'] >0:
        cap.release()
    cv2.destroyAllWindows()


def drawClock(frame, num_frames, elapsedTime, timeTag, virtual):
    ####################################################
    ### display date/fm on screen (run when recording)##
    ####################################################
    import datetime
    # draw the text and timestamp on the frame
    cv2.putText(frame, "frames: "+str(num_frames), (30, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (224, 255, 255), 1) # color black
    cv2.putText(frame, "Stopwatch: "+str('%0.3f' %(elapsedTime/1000))+"s", (150, 30),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (224, 255, 255), 1) # color black
    if virtual:
        cv2.putText(frame, "frames: " + str(num_frames), (30, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)  # color black
        cv2.putText(frame, "Stopwatch: " + str('%0.3f' % (elapsedTime / 1000)) + "s", (150, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)  # color black
    #cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S.%f%p")[:-5],
#                (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 153), 1) # color black

def sound_effects():
    #######################################################
    #####  Basic sounds from wav (not a game bg sound)  ###
    #######################################################
    pygame.mixer.init()
    local_path = os.getcwd()
    soundfiles_path = os.path.join(str(local_path), "resources","sounds")
    if not os.path.exists(soundfiles_path):
        os.makedirs(soundfiles_path)
    try:
        startCirclefx = pygame.mixer.Sound(os.path.join(soundfiles_path, "chiptone.wav"))#FIX: CROSS PLATFORM
        endCirclefx = pygame.mixer.Sound(os.path.join(soundfiles_path, "up1-chiptone.wav")) #FIX: CROSS PLATFORM
        obstablefx = pygame.mixer.Sound(os.path.join(soundfiles_path, "noisysqueak1.wav")) #FIX: CROSS PLATFORM
        GoSound = pygame.mixer.Sound(os.path.join(soundfiles_path,"start_coin.wav")) #FIX: CROSS PLATFORM
    except:
        raise(UserWarning, "could not load or play soundfiles in 'data' folder :-(")
            
    return startCirclefx, endCirclefx, obstablefx, GoSound

if __name__ == "__main__":
    timeTag = time.strftime("%Y%m%d_%H%M%S")

    import argparse, math, random, sys
    import pygame
    from pygame.locals import *

    ###  get arguments from terminal
    global args  # check speed performance...
    args = get_arguments()

    run_main(timeTag) # Main openCV loop
