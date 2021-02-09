#Start up window for TFRRS Visualizer
#By: Nick Meling and Matt Egts

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class StartWindow(object):
    def setupStartWindow(self, MainWindow):
    #Window set up
        MainWindow.setGeometry(400,150,700,500)
        MainWindow.setWindowTitle("TFRRS Visualizer")
        MainWindow.setStyleSheet("background-color: gray;")

    #Text description
        self.descriptionLabel= QLabel(MainWindow)
        self.descriptionLabel.setText("This program will allow you to visualize athlete statistics in Cross Country or Track and Field. You will be prompted to select NCAA Division, Gender, College, Sport, and Event.")
        self.descriptionLabel.setWordWrap(True)
        self.descriptionLabel.setAlignment(Qt.AlignCenter)
        self.descriptionLabel.move(200,200)
        self.descriptionLabel.setStyleSheet('QLabel {color: Orange}')

    #Button to continue to next window
        self.continueButton= QPushButton(MainWindow)
        self.continueButton.setText("Click here to continue")
        self.continueButton.move(285,350)
        self.continueButton.setStyleSheet("background-color: orange;")

class CollegeSelection(object):
    def setupCollegeSelection(self, MainWindow):
        MainWindow.setGeometry(400,150,700,500)
        MainWindow.setWindowTitle("TFRRS Visualizer")
        MainWindow.setStyleSheet("background-color: gray;")

    #Gender Selector
        self.gender= QComboBox(MainWindow)
        self.gender.setGeometry(350,150, 150, 50)
        self.gender.addItem('Male')
        self.gender.addItem('Female')
        self.gender.setStyleSheet("background-color: orange;")

        self.genderLabel= QLabel(MainWindow)
        self.genderLabel.setText('Gender')
        self.genderLabel.setGeometry(200,150,150,50)
        self.genderLabel.setStyleSheet('QLabel {color: Orange}')
        self.genderLabel.setFont(QFont('Arial', 15))

    #College Selector
        self.college= QComboBox(win)
        self.college.setGeometry(350,250, 150, 50)
        self.college.addItem('Augsburg')
        self.college.addItem('Loras')
        self.college.addItem('Wartburg')
        self.college.addItem('Central')
        self.college.setStyleSheet("background-color: orange;")

        self.collegeLabel= QLabel(MainWindow)
        self.collegeLabel.setText('College')
        self.collegeLabel.setGeometry(200,250,150,50)
        self.collegeLabel.setStyleSheet('QLabel {color: Orange}')
        self.collegeLabel.setFont(QFont('Arial', 15))

    #Next Button
        self.nextButton = QPushButton(MainWindow)
        self.nextButton.setText("Next")
        self.nextButton.setGeometry(275,400,100,50)
        self.nextButton.setStyleSheet("background-color: orange;")
        self.nextButton.setFont(QFont('Arial', 15))

class AthleteSelection(object):
    def setupAthleteSelection(self, MainWindow):
        MainWindow.setGeometry(400,150,700,500)
        MainWindow.setWindowTitle("TFRRS Visualizer")
        MainWindow.setStyleSheet("background-color: gray;")

    #Athlete Selector
        self.athlete=QListWidget(MainWindow)
        self. athlete.setGeometry(300,100,150,50)
        self. athlete.setAlternatingRowColors(True)
        self.athlete.addItem("Nick")
        self.athlete.addItem("Matt")
        self.athlete.addItem("John")
        self. athlete.setStyleSheet("background-color: orange;")
        #self.athlete.itemClicked(item) Need to be able to select the athletes.
        self.athleteLabel= QLabel(MainWindow)
        self.athleteLabel.setText("Athlete ('s)")
        self.athleteLabel.setGeometry(200,100,100,50)
        self.athleteLabel.setStyleSheet('QLabel {color: Orange}')
        self.athleteLabel.setFont(QFont("Arial", 15))

    #Season Selector
        self.season= QComboBox(MainWindow)
        self.season.setGeometry(100,250,200,50)
        self.season.addItem('Cross Country')
        self.season.addItem('Indoor Track and Field')
        self.season.addItem('Outdoor Track and Field')
        self.season.setStyleSheet("background-color: orange;")

        self.seasonLabel= QLabel(MainWindow)
        self.seasonLabel.setText('Season')
        self.seasonLabel.setGeometry(25,250,50,50)
        self.seasonLabel.setStyleSheet('QLabel {color: Orange}')
        self.seasonLabel.setFont(QFont("Arial", 15))

    #Event Selector
        self.event= QComboBox(MainWindow)
        self.event.setGeometry(475,250,200,50)
        self.event.addItem('100 m')
        self.event.addItem('200 m')
        self.event.addItem('400 m')
        self.event.addItem('800m')
        self.event.setStyleSheet("background-color: orange;")

        self.eventLabel= QLabel(MainWindow)
        self.eventLabel.setText('Event')
        self.eventLabel.setGeometry(400,250,50,50)
        self.eventLabel.setStyleSheet('QLabel {color: Orange}')
        self.eventLabel.setFont(QFont("Arial", 15))

    #Update Button
        self.updateButton= QPushButton(MainWindow)
        self.updateButton.setText("Update Selection")
        self.updateButton.setGeometry(300,400,150, 50)
        self.updateButton.setStyleSheet("background-color: orange;")


class MainWindow(QMainWindow):

    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.startWindow = StartWindow()
        #self.collegeSelection = ColSel()
        self.startStartWindow()

    def startStartWindow(self):
        self.startWindow.setupStart(self)
        self.startWindow.continueButton.clicked.connect(self.startCollegeSelection)
        self.show()

    def startCollegeSelection(self):
        self.CollegeSelection.setupCollegeSelection(self)
        self.startWindow.nextButton.clicked.connect(self.startAthleteSelection)
        self.show()

    #def startAthleteSelection(self):
        #self.AthleteSelection.setupAthleteSelection(self)
        #self.startWindow.updateButton.clicked.connect(self.

if __name__ == 'main':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())
