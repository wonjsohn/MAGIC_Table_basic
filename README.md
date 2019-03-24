MAGIC Table Data Acquisition in Python: Functional code
====================================

``` 
Project Author: Won Joon Sohn (wonjsohn@gmail.com) 
Current appointment: Postdoc research scholar at University of California, Irvine.
```

``` 
Application: 
* Upper limb movement Assessment and/or rehabilitation.  
* Movement strategies analysis
* Object tracking with color and shapes. 
* Multiple objects tracking in real time (not included here)
```

Requirements
------------
Build in python3.6 (other versions works well but the last build was with 3.6)
```bash
pip install pygame numpy ... (many more)
```
*Tip*: use Python Editor like PyCharm to easily build the environment.
An example environment for current system (as of 2018.12.15 by Won Joon):
Note that not all packages displayed here may be necessary to run the magic table.

Snapshot of PyCharm Project setting.
![Libraries](resources/python_libraries.png?raw=true)


How to play
-------
1. Open the MagicTable src folder.
2. `python main.py` + options.
3. Option are play, pp, pygame in broad category. 

```bash
BoardTask   e.g. > main.py -mod "play" -tt "p2p" -sid 'subjectID' -t 30
```
4. SubjectID. Mapping of subjects name - ID in encryped file (subject_mapping.enc).
    * computer0 : any testing trials 
    * NTxxx     : Neurotypicals
    * ASDxxx    : ASD 
5. Position checker - press 'S' to retake the snapshot. Otherwise esc to skip the snapshot. 
6. Snapshot taker - with cup removed from the scene, press space bar to detect the shapes until satisfied, press esc to move on.  
7.  Press esc to break out of current trial. The trial will still be saved.
8.  Press 'D' or 'd' to delete the current trial. It will break out of the trial and not save. 
9.  Press 'C' or 'c' to when the goal is reached in the fig8 task.
 
### Q. How to associate snapshot files with the subsequenct files? 
* New pickle dump files are generated without retaking snapshots. 
* TODO: snapshot files are not required to run any post processing. 


## Important files
* **arguments.py**: Sepcify input parameters to the main.py program
* **main.py**: The central loop for the camera tracking system.
* **save.py**: All the saving related functions.
* **snapshots.py**: For taking a snapshot of a board from webcam.
* **shape_detection.py**:  detect targets and obstacles when you first register the board.
* **colorRangeDetector.py**: Used to tune the color filter indices. If the lighting condition changes, it may be necessary to tune the indices.
* **check_camera_position.py**: the first file to be run (in main.py) to check the camera position.



## Magic talble file structure

MAGIC_TABLE_Root

    |_ graphical_panel
    |_ resouces
        |_ images
        |_ sounds
    |_ Output: (time, x, y, xb, yb) 
        |_videoOutput
        |_snapshots
        |_pickles
        |_dataframeOutput


## Output file structure:

MAGIC_TABLE_Root

    |_ Output: (time, x, y, xb, yb) 
        |__dataframeOutput
        |__vidoeOutput


General output filename convention: [timestamp_mode_subjectID_success.csv]
e.g. 20180910_134223_NT0_success.csv


## More options

* Display Go! with a start sound.
* Display digital clock with precision in ns. 

## Additional files

* videoOutput: recorded video from the camera during trials. Filename: [timestamp_mode_timeDuration_fps.mp4]
    * TODO: change mode name  
* snapshots: snapshots taken. Filename: [timestamp.jpg]
* pickles: timestamp_circles.dump (centers for two circles) / timestamp_rectangles.dump (if any rec is drawn) 
    * TODO: combine the two in one file. 








Output video format
---------------------
```
# -*- coding: utf-8 -*-
– / avi / 112512 kB / I420 / WMP, VLC, Films&TV, MovieMaker
MJPG / avi / 14115 kB / MJPG / VLC
MJPG / mp4 / 5111 kB / 6C / VLC
CVID / avi / 7459 kB / cvid / WMP, VLC, MovieMaker
MSVC / avi / 83082 kB / CRAM / WMP, VLC
X264 / avi / 187 kB / H264 / WMP, VLC, Films&TV, MovieMaker  => doesn't work in Windows...
XVID / avi / 601 kB / XVID / WMP, VLC, MovieMaker
XVID / mp4 / 587 kB / 20 / WMP, VLC, Films&TV, MovieMaker
PIM1 / mp4 / similar to XVID /     MPEG-1 Codec
```


* Python opencv installation option. (as of Sep. 2017) 
```
# -*- coding: utf-8 -*-
cmake -D CMAKE_BUILD_TYPE=RELEASE \
-D CMAKE_INSTALL_PREFIX=/usr/local \
-D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib/modules \
-D PYTHON2_LIBRARY=/usr/local/Cellar/python/2.7.13/Frameworks/Python.framework/Versions/2.7/lib/python2.7/config/libpython2.7.dylib \
-D PYTHON2_INCLUDE_DIR=/usr/local/Cellar/python/2.7.13/Frameworks/Python.framework/Versions/2.7/include/python2.7/ \
-D PYTHON2_EXECUTABLE=$VIRTUAL_ENV/bin/python \
-D BUILD_opencv_python2=ON \
-D BUILD_opencv_python3=OFF \
-D INSTALL_PYTHON_EXAMPLES=ON \
-D INSTALL_C_EXAMPLES=OFF \
-D BUILD_EXAMPLES=ON ..\
```
