@echo off
echo Hello this a test batch file
REM[local computer's python path] [path for MAGIcTableGUI_Runner.py]
C:\Users\wonjsohn\AppData\Local\Programs\Python\Python36\python.exe C:\Users\wonjsohn\Documents\GitHub\MAGicTable_opensource\graphical_panel\MAGIcTableGUI_Runner.py %*
REM cmd /k to keep the command window open.
cmd /k