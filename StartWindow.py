#Start up window for TFRRS Visualizer
#By: Nick Meling and Matt Egts

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class StartWindow(object):
    def setupStart(self, win):
    #Window set up
        win.setGeometry(400,150,700,500)
        win.setWindowTitle("TFRRS Visualizer")
        win.setStyleSheet("background-color: gray;")

    #Text description 1
        self.label= QLabel(win)
        self.label.setText("This program will allow you to visualize athlete statistics in Cross Country or Track and Field. You will be prompted to select NCAA Division, Gender, College, Sport, and Event.")
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.move(200,200)

        self.label.setStyleSheet('QLabel {color: Orange}')

    #Button to continue to next window
        self.next_btn= QPushButton(win)
        self.next_btn.setText("Click here to continue")
        self.next_btn.move(285,350)
        self.next_btn.setStyleSheet("background-color: orange;")

class MainWindow(QMainWindow):

    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.startWindow = StartWindow()
        self.collegeSelection = ColSel()
        self.startStartWindow()

    def startStartWindow(self):
        self.startWindow.setupStart(self)
        self.startWindow.next_btn.clicked.connect(self.startCollegeSelection)
        self.show()

    def startCollegeSelection(self):
        self.collegeSelection.setupCollegeSelection(self)
        # put next button event here
        self.show()

if __name__ == 'main':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())
