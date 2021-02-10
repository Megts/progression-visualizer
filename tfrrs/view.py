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
        MainWindow.setFixedSize(700,500)
        MainWindow.setWindowTitle("TFRRS Visualizer")
        MainWindow.setStyleSheet("background-color: gray;")
        self.centralwidget = QWidget(MainWindow)

    #Text description
        #self.descriptionLabel= QLabel(MainWindow)
        self.descriptionLabel = QLabel("This program will allow you to visualize athlete statistics in Cross Country or Track and Field. You will be prompted to select NCAA Division, Gender, College, Sport, and Event.",
                                        self.centralwidget)
        self.descriptionLabel.setWordWrap(True)
        self.descriptionLabel.setFont(QFont("Arial", 15))
        self.descriptionLabel.setAlignment(Qt.AlignCenter)
        self.descriptionLabel.setGeometry(175,200,350,100)
        self.descriptionLabel.setStyleSheet('QLabel {color: Orange}')

    #Button to continue to next window
        #self.continueButton= QPushButton(MainWindow)
        self.continueButton = QPushButton("Click here to continue", self.centralwidget)
        self.continueButton.setGeometry(275,350,150,50)
        self.continueButton.setStyleSheet("background-color: orange;")

        MainWindow.setCentralWidget(self.centralwidget)

class CollegeSelection(object):
    def setupCollegeSelection(self, MainWindow):
        MainWindow.setGeometry(400,150,700,500)
        MainWindow.setWindowTitle("TFRRS Visualizer")
        MainWindow.setStyleSheet("background-color: gray;")
        self.centralwidget = QWidget(MainWindow)

    #Division Selector
        self.division= QComboBox(self.centralwidget)
        self.division.setGeometry(350,50,150,50)
        self.division.addItem('Divsion 1')
        self.division.addItem('Divison 2')
        self.division.addItem('Division 3')
        self.division.setStyleSheet("background-color: orange;")

        self.divisionLabel= QLabel(self.centralwidget)
        self.divisionLabel.setText('Division')
        self.divisionLabel.setGeometry(200,50,150,50)
        self.divisionLabel.setAlignment(Qt.AlignCenter)
        self.divisionLabel.setStyleSheet('QLabel {color: Orange}')
        self.divisionLabel.setFont(QFont('Arial', 15))    

    #Gender Selector
        self.gender= QComboBox(self.centralwidget)
        self.gender.setGeometry(350,150, 150, 50)
        self.gender.addItem('Male')
        self.gender.addItem('Female')
        self.gender.setStyleSheet("background-color: orange;")

        self.genderLabel= QLabel(self.centralwidget)
        self.genderLabel.setText('Gender')
        self.genderLabel.setGeometry(200,150,150,50)
        self.genderLabel.setAlignment(Qt.AlignCenter)
        self.genderLabel.setStyleSheet('QLabel {color: Orange}')
        self.genderLabel.setFont(QFont('Arial', 15))

    #College Selector
        self.college= QComboBox(self.centralwidget)
        self.college.setGeometry(350,250, 150, 50)
        self.college.addItem('Augsburg')
        self.college.addItem('Loras')
        self.college.addItem('Wartburg')
        self.college.addItem('Central')
        self.college.setStyleSheet("background-color: orange;")

        self.collegeLabel= QLabel(self.centralwidget)
        self.collegeLabel.setText('College')
        self.collegeLabel.setGeometry(200,250,150,50)
        self.collegeLabel.setAlignment(Qt.AlignCenter)
        self.collegeLabel.setStyleSheet('QLabel {color: Orange}')
        self.collegeLabel.setFont(QFont('Arial', 15))

    #Next Button
        self.nextButton = QPushButton(self.centralwidget)
        self.nextButton.setText("Next")
        self.nextButton.setGeometry(300,400,100,50)
        self.nextButton.setStyleSheet("background-color: orange;")
        self.nextButton.setFont(QFont('Arial', 15))

        MainWindow.setCentralWidget(self.centralwidget)

class AthleteSelection(object):
    def setupAthleteSelection(self, MainWindow):
        MainWindow.setGeometry(400,150,700,500)
        MainWindow.setWindowTitle("TFRRS Visualizer")
        MainWindow.setStyleSheet("background-color: gray;")
        self.centralwidget = QWidget(MainWindow)

    #Athlete Selector
        self.athlete=QListWidget(self.centralwidget)
        self.athlete.setGeometry(275,100,200,50)
        self.athlete.setAlternatingRowColors(True)
        self.athlete.addItem("Nick")
        self.athlete.addItem("Matt")
        self.athlete.addItem("John")
        self.athlete.addItem("Brock")
        self.athlete.addItem("Levi")
        self.athlete.addItem("Chris")
        self.athlete.setStyleSheet("background-color: orange;")
        #self.athlete.itemClicked(item) Need to be able to select the athletes.
        self.athleteLabel= QLabel(self.centralwidget)
        self.athleteLabel.setText("Athlete(s)")
        self.athleteLabel.setAlignment(Qt.AlignCenter)
        self.athleteLabel.setGeometry(125,100,150,50)
        self.athleteLabel.setAlignment(Qt.AlignCenter)
        self.athleteLabel.setStyleSheet('QLabel {color: Orange}')
        self.athleteLabel.setFont(QFont("Arial", 15))

    #Season Selector
        self.season= QComboBox(self.centralwidget)
        self.season.setGeometry(100,250,200,50)
        self.season.addItem('Cross Country')
        self.season.addItem('Indoor Track and Field')
        self.season.addItem('Outdoor Track and Field')
        self.season.setStyleSheet("background-color: orange;")

        self.seasonLabel= QLabel(self.centralwidget)
        self.seasonLabel.setText('Season')
        self.seasonLabel.setGeometry(0,250,100,50)
        self.seasonLabel.setAlignment(Qt.AlignCenter)
        self.seasonLabel.setStyleSheet('QLabel {color: Orange}')
        self.seasonLabel.setFont(QFont("Arial", 15))

    #Event Selector
        self.event= QComboBox(self.centralwidget)
        self.event.setGeometry(475,250,200,50)
        self.event.addItem('100 m')
        self.event.addItem('200 m')
        self.event.addItem('400 m')
        self.event.addItem('800m')
        self.event.setStyleSheet("background-color: orange;")

        self.eventLabel = QLabel(self.centralwidget)
        self.eventLabel.setText('Event')
        self.eventLabel.setGeometry(375,250,100,50)
        self.eventLabel.setAlignment(Qt.AlignCenter)
        self.eventLabel.setStyleSheet('QLabel {color: Orange}')
        self.eventLabel.setFont(QFont("Arial", 15))

    #Update Button
        self.updateButton= QPushButton(self.centralwidget)
        self.updateButton.setText("Update Selection")
        self.updateButton.setGeometry(275,400,150, 50)
        self.updateButton.setStyleSheet("background-color: orange;")

        MainWindow.setCentralWidget(self.centralwidget)


class MainWindow(QMainWindow):

    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.startWindow = StartWindow()
        self.collegeSelection = CollegeSelection()
        self.athleteSelection = AthleteSelection()
        self.startStartWindow()

    def startStartWindow(self):
        self.startWindow.setupStartWindow(self)
        self.startWindow.continueButton.clicked.connect(self.startCollegeSelection)
        self.show()


    def startCollegeSelection(self):
        self.collegeSelection.setupCollegeSelection(self)
        self.collegeSelection.nextButton.clicked.connect(self.startAthleteSelection)
        self.show()


    def startAthleteSelection(self):
        self.athleteSelection.setupAthleteSelection(self)
        #self.athleteSelection.updateButton.clicked.connect(self.Startgraphwin)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())
