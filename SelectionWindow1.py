#Selector Window 1 for TFRRS Visualizer
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
    division= QListWidget(win)
    division.setGeometry(350,50,150,50)
    division.addItem('Divsion 1')
    division.addItem('Divison 2')
    division.addItem('Division 3')
    division.setStyleSheet("background-color: orange;")

    label1= QLabel(win)
    label1.setText('Division')
    label1.setGeometry(200,50,150,50)
    label1.setStyleSheet('QLabel {color: Orange}')
    label1.setFont(QFont('Arial', 15))

#Gender Selector
    gender= QComboBox(win)
    gender.setGeometry(350,150, 150, 50)
    gender.addItem('Male')
    gender.addItem('Female')
    gender.setStyleSheet("background-color: orange;")

    label2= QLabel(win)
    label2.setText('Gender')
    label2.setGeometry(200,150,150,50)
    label2.setStyleSheet('QLabel {color: Orange}')
    label2.setFont(QFont('Arial', 15))
    

#College Selector
    college= QComboBox(win)
    college.setGeometry(350,250, 150, 50)
    college.addItem('Augsburg')
    college.addItem('Loras')
    college.addItem('Wartburg')
    college.addItem('Central')
    college.setStyleSheet("background-color: orange;")

    label3= QLabel(win)
    label3.setText('College')
    label3.setGeometry(200,250,150,50)
    label3.setStyleSheet('QLabel {color: Orange}')
    label3.setFont(QFont('Arial', 15))



#Update Button
    update= QPushButton(win)
    update.setText("Next")
    update.setGeometry(275,400,100,50)
    update.setStyleSheet("background-color: orange;")
    update.setFont(QFont('Arial', 15))


    win.show()
    sys.exit(app.exec())

window()
