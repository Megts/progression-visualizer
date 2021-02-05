#Selector Window for TFRRS Visualizer
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

#Division Selector
    division= QComboBox(win)
    division.setGeometry(500,0,150,50)
    division.addItem('Divsion 1')
    division.addItem('Divison 2')
    division.addItem('Division 3')
    division.setStyleSheet("background-color: orange;")

    label1= QLabel(win)
    label1.setText('Division')
    label1.setGeometry(250,-20,100,100)
    label1.setStyleSheet('QLabel {color: Orange}')

#Gender Selector
    gender= QComboBox(win)
    gender.setGeometry(500,100,150,50)
    gender.addItem('Male')
    gender.addItem('Female')
    gender.setStyleSheet("background-color: orange;")

    label2= QLabel(win)
    label2.setText('Gender')
    label2.setGeometry(250,80,100,100)
    label2.setStyleSheet('QLabel {color: Orange}')
    label2.setFont(QFont('Arial', 10))
    

#College Selector
    college= QComboBox(win)
    college.setGeometry(500,200,150,50)
    college.addItem('Augsburg')
    college.addItem('Loras')
    college.addItem('Wartburg')
    college.addItem('Central')
    college.setStyleSheet("background-color: orange;")

    label3= QLabel(win)
    label3.setText('College')
    label3.setGeometry(250,180,100,100)
    label3.setStyleSheet('QLabel {color: Orange}')

#Sport Selector
    sport= QComboBox(win)
    sport.setGeometry(500,300,150,50)
    sport.addItem('Cross Country')
    sport.addItem('Indoor Track and Field')
    sport.addItem('Outdoor Track and Field')
    sport.setStyleSheet("background-color: orange;")

    label4= QLabel(win)
    label4.setText('Season')
    label4.setGeometry(250,280,150,100)
    label4.setStyleSheet('QLabel {color: Orange}')

#Athlete Selector
    athlete= QComboBox(win)
    athlete.setGeometry(500,400,150,50)
    athlete.addItem('Matthew Egts')
    athlete.addItem('Nick Meling')
    athlete.addItem('John Zelle')
    athlete.setStyleSheet("background-color: orange;")

    label5= QLabel(win)
    label5.setText('Athlete')
    label5.setGeometry(250,380,100,100)
    label5.setStyleSheet('QLabel {color: Orange}')

#Event Selector
    event= QComboBox(win)
    event.setGeometry(500,500,150,50)
    event.addItem('100 m')
    event.addItem('200 m')
    event.addItem('400 m')
    event.addItem('800m')
    event.setStyleSheet("background-color: orange;")

    label6= QLabel(win)
    label6.setText('Event')
    label6.setGeometry(250,480,100,100)
    label6.setStyleSheet('QLabel {color: Orange}')

#Update Button
    update= QPushButton(win)
    update.setText("Update")
    update.setGeometry(350,600,100,50)


    win.show()
    sys.exit(app.exec())

window()
