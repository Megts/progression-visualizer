#Start up window for TFRRS Visualizer
#By: Nick Meling and Matt Egts

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox, QPushButton, QWidget, QDesktopWidget

def window():
#Window set up
    app=QApplication(sys.argv)
    win=QWidget()
    win.setGeometry(400,150,700,700)
    win.setWindowTitle("TFRRS Visualizer")
    win.setStyleSheet("background-color: gray;")
#Text description 1
    label= QLabel(win)
    label.setText("This program will allow you to visualize athlete stats in Cross Country or Track and Field.")
    label.move(100,50)
    label.setStyleSheet("background-color: orange;")
#Text description 2
    label= QLabel(win)
    label.setText("You will be prompted to select NCAA Division, Gender, College, Sport, and Event.")
    label.move(100,66)
    label.setStyleSheet("background-color: orange;")
#Button to continue to next window
    button= QPushButton(win)
    button.setText("Click here to continue")
    button.move(300,350)
    button.setStyleSheet("background-color: orange;")
  
    win.show()
    sys.exit(app.exec_())

window()
