#Selector Window 2 for TFFRS Visualizer
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

#Athlete Selector
    athlete=QListWidget(win)
    athlete.setGeometry(300,100,150,50)
    athlete.setAlternatingRowColors(True)
    athlete.addItem("Nick")
    athlete.addItem("Matt")
    athlete.addItem("John")
    athlete.setStyleSheet("background-color: orange;")
    #athlete.itemClicked(item) Need to be able to select the athletes.

    labela= QLabel(win)
    labela.setText("Athlete ('s)")
    labela.setGeometry(200,100,100,50)
    labela.setStyleSheet('QLabel {color: Orange}')
    labela.setFont(QFont("Arial", 15))


#Season Selector
    season= QComboBox(win)
    season.setGeometry(100,250,200,50)
    season.addItem('Cross Country')
    season.addItem('Indoor Track and Field')
    season.addItem('Outdoor Track and Field')
    season.setStyleSheet("background-color: orange;")

    labels= QLabel(win)
    labels.setText('Season')
    labels.setGeometry(25,250,50,50)
    labels.setStyleSheet('QLabel {color: Orange}')
    labels.setFont(QFont("Arial", 15))


#Event Selector
    event= QComboBox(win)
    event.setGeometry(475,250,200,50)
    event.addItem('100 m')
    event.addItem('200 m')
    event.addItem('400 m')
    event.addItem('800m')
    event.setStyleSheet("background-color: orange;")

    labele= QLabel(win)
    labele.setText('Event')
    labele.setGeometry(400,250,50,50)
    labele.setStyleSheet('QLabel {color: Orange}')
    labele.setFont(QFont("Arial", 15))

#Update Button
    update= QPushButton(win)
    update.setText("Update Selection")
    update.setGeometry(300,400,150, 50)
    update.setStyleSheet("background-color: orange;")

    win.show()
    sys.exit(app.exec())

window()
