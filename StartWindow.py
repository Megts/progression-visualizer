#Start up window for TFRRS Visualizer
#By: Nick Meling and Matt Egts

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


def window():
#Window set up
    app=QApplication(sys.argv)
    win=QWidget()
    win.setGeometry(400,150,700,500)
    win.setWindowTitle("TFRRS Visualizer")
    win.setStyleSheet("background-color: gray;")
    
#Text description 1
    label= QLabel(win)
    label.setText("This program will allow you to visualize athlete statistics in Cross Country or Track and Field. You will be prompted to select NCAA Division, Gender, College, Sport, and Event.")
    label.setWordWrap(True)
    label.setAlignment(Qt.AlignCenter)
    label.move(200,200)
    
    label.setStyleSheet('QLabel {color: Orange}')
    
#Button to continue to next window
    button= QPushButton(win)
    button.setText("Click here to continue")
    button.move(285,350)
    button.setStyleSheet("background-color: orange;")
  
    win.show()
    sys.exit(app.exec_())

window()
