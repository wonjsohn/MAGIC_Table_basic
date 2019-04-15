import os
import sys
from PyQt5.QtCore import QSize, QCoreApplication, QSettings
from PyQt5.QtWidgets import QApplication, QDialog
# from Ui_MAGicTableGUI import Ui_Dialog # don't need when using loadUi? setupUi not used here
from PyQt5.uic import loadUi
from PyQt5 import uic
from PyQt5 import QtCore, QtGui, QtWidgets


class MAGIcTableGUI_Runner(QDialog):
    def __init__(self):
        super(MAGIcTableGUI_Runner, self).__init__()
        self.settings = None
        self.ui = uic.loadUi('Ui_MAGIcTableGUI.ui', self)   # do not delete as this is one of the ways

        """ Window positioning: top right corner fo the screen """
        frame = self.frameGeometry()
        resolution = QtWidgets.QDesktopWidget().screenGeometry()
        # frame.moveCenter(cp)
        position_x =  resolution.width() - self.geometry().width()
        position_y =  0
        print('x, y:', position_x,  position_y )
        print(' resolution.width(),  resolution.height():', resolution.width() , resolution.height() )
        self.move(position_x, position_y)
        # self.move(frame.topRight())
        # self.resize(1100, 700)


        """ Load saved setting """
        # self.setupUi(self)
        self.loadSettings() # load setting from prev

        self.image = None
        os.chdir("../")

        print(sys.path)

        # connect the slot to the signal by clicking the checkbox to save the state settings
        self.id_comboBox.currentIndexChanged[str].connect(self.id_selectionchange)
        self.reset_to_default_pushButton.clicked.connect(self.resetSettings)
        # self.save_setting_pushButton.clicked.connect(self.saveSettings)
        self.run_pushButton.clicked.connect(lambda: self.run())

    def id_selectionchange(self, i):
        ## list the current combobox selections
        for count in range(self.id_comboBox.count()):
            print(self.id_comboBox.itemText(count))
        print("Current ID index", i, "selection changed ", self.id_comboBox.currentText())

    def resetSettings(self):
        self.settings.clear()
        self.close()

    # Slot checkbox to save the settings
    def saveSettings(self):
        print("save setting attempt")
        self.settings = QSettings("MyCom", "name")
        self.settings.beginGroup("set1")

        """ MODES """
        self.settings.setValue("p2p_radioButton_ln",  self.p2p_radioButton.isChecked())
        self.settings.setValue("fig8_radioButton_ln",  self.fig8_radioButton.isChecked())

        """ SUBJECT INFO """
        self.settings.setValue("sid_lineEdit_ln", self.sid_lineEdit.text())
        self.settings.setValue("rh_radioButton_ln", self.rh_radioButton.isChecked())
        self.settings.setValue("lh_radioButton_ln", self.lh_radioButton.isChecked())
        self.settings.setValue("timelimit_spinBox_ln", self.timelimit_spinBox.value()) # ln: lookup name
        self.settings.setValue("id_comboBox_ln", self.id_comboBox.currentText())
        print("saved current id combobox text: ", self.id_comboBox.currentText())

        """ CHECKBOXES """
        self.settings.setValue("display_checkbox_ln", self.display_checkbox.checkState())
        self.settings.setValue("display_trace_checkbox_ln", self.display_trace_checkbox.checkState())
        self.settings.setValue("display_clock_checkbox_ln", self.display_clock_checkbox.checkState())
        self.settings.setValue("target_sound_checkbox_ln", self.target_sound_checkbox.checkState())
        self.settings.setValue("target_visual_checbox_ln", self.target_visual_checbox.checkState())

        self.settings.endGroup()

    def loadSettings(self):
        print("Loading settings...")
        self.settings = QSettings('MyCom', 'name')
        # self.settings.clear() # may need to clear on errors
        print('All keys: ', self.settings.allKeys())

        if self.settings.allKeys(): # if keys exist
            self.settings.beginGroup("set1") # do not change the name

            """ MODES """
            p2p_radioButton = self.settings.value("p2p_radioButton_ln")
            fig8_radioButton = self.settings.value("fig8_radioButton_ln")

            """ SUBJECT INFO """
            sid_lineEdit = self.settings.value("sid_lineEdit_ln")
            rh_radioButton = self.settings.value("rh_radioButton_ln")
            lh_radioButton = self.settings.value("lh_radioButton_ln")
            timeout = self.settings.value("timelimit_spinBox_ln")
            id_comboBox = self.settings.value("id_comboBox_ln")

            """ CHECKBOXES """
            # load key settings from prev save (find a cleaner way later) do not change the names
            display_checkbox = self.settings.value("display_checkbox_ln")
            display_trace_checkbox = self.settings.value("display_trace_checkbox_ln")
            display_clock_checkbox = self.settings.value("display_clock_checkbox_ln")
            target_sound_checkbox = self.settings.value("target_sound_checkbox_ln")
            target_visual_checbox = self.settings.value("target_visual_checbox_ln")

            ## temp fix (4/2/19)
            if p2p_radioButton == 'true':
                p2p_bool = True
                self.tt = "p2p"
            else:
                p2p_bool = False
                self.tt = "fig8"
            if fig8_radioButton == 'true':
                fig8_bool = True
            else:
                fig8_bool = False

            if rh_radioButton == 'true':
                rh_bool = True
                self.hn = "r"
            else:
                rh_bool = False
                self.hn = "l"
            if lh_radioButton == 'true':
                lh_bool = True
            else:
                lh_bool = False

            """ apply to the current window """
            """ MODES """
            self.p2p_radioButton.setChecked(p2p_bool)
            self.fig8_radioButton.setChecked(fig8_bool)

            """ SUBJECT INFO """
            self.sid_lineEdit.setText(sid_lineEdit)
            self.rh_radioButton.setChecked(rh_bool)
            self.lh_radioButton.setChecked(lh_bool)
            self.timelimit_spinBox.setProperty("value", timeout)
            self.id_comboBox.setProperty("currentText", id_comboBox)
            self.id_comboBox.setProperty("value", id_comboBox)

            """ CHECKBOXES """
            self.display_checkbox.setChecked(display_checkbox)
            self.display_trace_checkbox.setChecked(display_trace_checkbox)
            self.display_clock_checkbox.setChecked(display_clock_checkbox)
            self.target_sound_checkbox.setChecked(target_sound_checkbox)
            self.target_visual_checbox.setChecked(target_visual_checbox)

            """ print out """
            print("loaded subject ID:", sid_lineEdit)
            print("loaded time limit:", timeout)
            print("loaded id box text:", id_comboBox)


            self.settings.endGroup()

        else: # no key exist because reset or deleted
            self.saveSettings()
            self.loadSettings()

    def run(self):
        # call(['python', path])
        self.saveSettings()
        self.loadSettings()

        display_int = 1 if self.display_checkbox.checkState() > 0 else 0
        display_trace_checkbox_int = 1 if self.display_trace_checkbox.checkState() > 0 else 0
        display_clock_checkbox_int = 1 if self.display_clock_checkbox.checkState() > 0 else 0
        target_sound_checkbox_int = 1 if self.target_sound_checkbox.checkState() > 0 else 0
        target_visual_checbox_int = 1 if self.target_visual_checbox.checkState() > 0 else 0

        cmd = "python main.py -mod play -tt " + self.tt \
              + " -sid " + self.sid_lineEdit.text()\
              + " -hn " + self.hn\
              + " -t " + str(self.timelimit_spinBox.value()) \
              + " -idx " + self.id_comboBox.currentText()\
              + " -d " + str(display_int) \
              + ' -tr ' + str(display_trace_checkbox_int)\
              + ' -clk ' + str(display_clock_checkbox_int) \
              + ' -ts ' + str(target_sound_checkbox_int) \
              + ' -tv ' + str(target_visual_checbox_int)

        print('Submitted arguments: ', cmd)
        os.system(cmd)
        # QCoreApplication.instance().quit() # This line closes the GUI window after every run.



if __name__=='__main__':
    app=QApplication(sys.argv)
    window = MAGIcTableGUI_Runner()
    window.setWindowTitle('MAGIC_TABLE_GUI')
    window.show()
    sys.exit(app.exec_())