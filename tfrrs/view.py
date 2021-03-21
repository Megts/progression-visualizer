#TFRRS Visualizer Program
#By: Nick Meling and Matt Egts

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from ncaa_db_queries import DB
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter
from datetime import datetime


db = DB('ncaa.db')
TOP = 400
LEFT = 150
WIDTH = 700
HEIGHT = 500

class StartWindow(object):
    def setupStartWindow(self, MainWindow):
#Window set up
        MainWindow.setGeometry(TOP,LEFT,WIDTH,HEIGHT)
        MainWindow.setFixedSize(700,500)
        MainWindow.setWindowTitle("TFRRS Visualizer")
        MainWindow.setStyleSheet("background-color: gray;")
        self.centralwidget = QWidget(MainWindow)

#Text description
        self.descriptionLabel = QLabel("This program will allow you to visualize athlete statistics in Cross Country or Track and Field. You will be prompted to select NCAA Division, Gender, College, Sport, and Event.",
                                        self.centralwidget)
        self.descriptionLabel.setWordWrap(True)
        self.descriptionLabel.setFont(QFont("Arial", 20))
        self.descriptionLabel.setAlignment(Qt.AlignCenter)
        self.descriptionLabel.setGeometry((WIDTH-375)//2,10,375,325)
        self.descriptionLabel.setStyleSheet('QLabel {color: Orange}')

#Button to continue to next window
        self.continueButton = QPushButton("Click here to continue", self.centralwidget)
        self.continueButton.setGeometry(275,350,150,50)
        self.continueButton.setStyleSheet("background-color: orange;")

        MainWindow.setCentralWidget(self.centralwidget)

class CollegeSelection(object):
#Window set up for window that user selects Division, Gender, and College
    def setupCollegeSelection(self, MainWindow):
        MainWindow.setGeometry(TOP,LEFT,WIDTH,HEIGHT)
        MainWindow.setWindowTitle("TFRRS Visualizer")
        MainWindow.setStyleSheet("background-color: gray;")
        self.centralwidget = QWidget(MainWindow)

#Division Selector
        self.division = QComboBox(self.centralwidget)
        self.division.setGeometry(350,50,150,50)
        self.division.addItem('Divsion 1')
        self.division.addItem('Divison 2')
        self.division.addItem('Division 3')
        self.division.setStyleSheet("background-color: orange;")
        self.div = 1

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
        self.gen = 'm'

        self.genderLabel= QLabel(self.centralwidget)
        self.genderLabel.setText('Gender')
        self.genderLabel.setGeometry(200,150,150,50)
        self.genderLabel.setAlignment(Qt.AlignCenter)
        self.genderLabel.setStyleSheet('QLabel {color: Orange}')
        self.genderLabel.setFont(QFont('Arial', 15))

#College Selector
        self.college= QComboBox(self.centralwidget)
        self.college.setGeometry(350,250, 150, 50)
        self.name_id = db.get_div_teams(self.div, self.gen)
        team_names = [name for name, id in self.name_id]
        self.college.addItems(team_names)
        self.college_id = self.name_id[0][1]
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

    def divisionchange(self,i):
        self.college.clear()
        self.div = i + 1
        self.name_id = db.get_div_teams(self.div, self.gen)
        team_names = [name for name, id in self.name_id]
        self.college.clear()
        self.college.addItems(team_names)
        self.division.setCurrentIndex(i)

    def genderchange(self, i):
        self.college.clear()
        if i == 0:
            self.gen = 'm'
        else:
            self.gen = 'f'
        self.name_id = db.get_div_teams(self.div, self.gen)
        team_names = [name for name, id in self.name_id]
        self.college.clear()
        self.college.addItems(team_names)
        self.gender.setCurrentIndex(i)

    def collegechange(self,i):
        self.college_id = self.name_id[i][1]

class AthleteSelection(object):
    def setupAthleteSelection(self, MainWindow, college_id):
        self.college_id = college_id
        MainWindow.setGeometry(TOP,LEFT,WIDTH,HEIGHT)
        MainWindow.setWindowTitle("TFRRS Visualizer")
        MainWindow.setStyleSheet("background-color: gray;")
        self.centralwidget = QWidget(MainWindow)

#Athlete Selector
        self.athlete=QComboBox(self.centralwidget)
        self.athlete.setGeometry(250,25,200,50)
        self.athletes = db.get_init_team_roster(self.college_id)
        athlete_names = [name for name, id in self.athletes]
        self.ath_id = self.athletes[0][1]
        self.athlete.addItems(athlete_names)
        self.athlete.setStyleSheet("background-color: orange;")

        self.athleteLabel= QLabel(self.centralwidget)
        self.athleteLabel.setText("Athlete(s)")
        self.athleteLabel.setAlignment(Qt.AlignCenter)
        self.athleteLabel.setGeometry(100,25,150,50)
        self.athleteLabel.setAlignment(Qt.AlignCenter)
        self.athleteLabel.setStyleSheet('QLabel {color: Orange}')
        self.athleteLabel.setFont(QFont("Arial", 15))


#Season Selector
        self.season= QComboBox(self.centralwidget)
        self.season.setGeometry(100,250,200,50)
        seasons = db.get_athlete_seasons(self.ath_id)
        self.season.addItems(seasons)
        self.season.setStyleSheet("background-color: orange;")
        self.season_picked = self.season.currentText()

        self.seasonLabel= QLabel(self.centralwidget)
        self.seasonLabel.setText('Season')
        self.seasonLabel.setGeometry(0,250,100,50)
        self.seasonLabel.setAlignment(Qt.AlignCenter)
        self.seasonLabel.setStyleSheet('QLabel {color: Orange}')
        self.seasonLabel.setFont(QFont("Arial", 15))

#Event Selector
        self.event= QComboBox(self.centralwidget)
        self.event.setGeometry(475,250,200,50)
        events = db.get_athlete_season_events(self.ath_id, self.season_picked)
        self.event.addItems(events)
        self.event_picked = self.event.currentText()
        self.event.setStyleSheet("background-color: orange;")

        self.eventLabel = QLabel(self.centralwidget)
        self.eventLabel.setText('Event')
        self.eventLabel.setGeometry(375,250,100,50)
        self.eventLabel.setAlignment(Qt.AlignCenter)
        self.eventLabel.setStyleSheet('QLabel {color: Orange}')
        self.eventLabel.setFont(QFont("Arial", 15))

#Update Button
        self.updateButton= QPushButton(self.centralwidget)
        self.updateButton.setText("Plot Selected Event")
        self.updateButton.setGeometry(275,425,150, 50)
        self.updateButton.setStyleSheet("background-color: orange;")

        MainWindow.setCentralWidget(self.centralwidget)

#Back Button
        self.backButton=QPushButton(self.centralwidget)
        self.backButton.setText("Back")
        self.backButton.setGeometry (50,425, 150, 50)
        self.backButton.setStyleSheet("background-color: orange;")

        MainWindow.setCentralWidget(self.centralwidget)

#Button to go to statViewer window
        self.statButton=QPushButton(self.centralwidget)
        self.statButton.setText("View Athlete Stats")
        self.statButton.setGeometry(500,425,150,50)
        self.statButton.setStyleSheet("background-color: orange;")

        MainWindow.setCentralWidget(self.centralwidget)

#Add Athlete Button
        self.addButton=QPushButton(self.centralwidget)
        self.addButton.setText("+")
        self.addButton.setGeometry(475,25,50,50)
        self.addButton.setStyleSheet("background-color: orange;")
        self.addButton.pressed.connect(self.action)

        MainWindow.setCentralWidget(self.centralwidget)



#Show second athlete selector when prompted by addButton
    def action(self):

        self.athlete2=QComboBox(self.centralwidget)
        self.athlete2.setGeometry(250,100,200,50)
        self.athlete2.setStyleSheet("background-color: orange;")

        print(self.college_id, [self.ath_id], self.season_picked, self.event_picked)
        self.athletes2 = db.get_remaining_team_roster(self.college_id, [self.ath_id], self.season_picked, self.event_picked)
        self.ath_id2 = self.athletes2[0][1]
        athlete_names2 = [name for name, id in self.athletes2]
        self.athlete2.addItems(athlete_names2)


        self.athlete2.show()


    def seasonChange(self,i):
        self.season_picked = self.season.itemText(i)
        events = db.get_athlete_season_events(self.ath_id, self.season_picked)
        self.event.clear()
        self.event.addItems(events)

    def eventChange(self, i):
        self.event_picked = self.event.itemText(i)

    def athleteChange(self,i):
        self.ath_id = self.athletes[i][1]
        seasons = db.get_athlete_seasons(self.ath_id)
        self.season.clear()
        self.season.addItems(seasons)
        self.season_picked = self.season.currentText()
        events = db.get_athlete_season_events(self.ath_id, self.season_picked)
        self.event.clear()
        self.event.addItems(events)
        self.event_picked = self.event.currentText()

class GraphViewer(object):
    def setupGraphViewer(self, MainWindow, athlete_id, event_name, season):
        MainWindow.setGeometry(TOP,LEFT,WIDTH,HEIGHT)
        MainWindow.setWindowTitle("TFRRS Visualizer")
        MainWindow.setStyleSheet("background-color: gray;")
        self.centralwidget = QWidget(MainWindow)

#Back Button on Graph
        self.backButton=QPushButton(self.centralwidget)
        self.backButton.setText("Back")
        self.backButton.setGeometry (275,425, 150, 50)
        self.backButton.setStyleSheet("background-color: orange;")

        MainWindow.setCentralWidget(self.centralwidget)



#Graph Formatting and Inputs
        sc = Canvas(self.centralwidget, width = 650, height = 400)
        sc.move((WIDTH-650)//2,0)
        marks, dates, units, wind2, wind4 = db.get_athlete_results(athlete_id, event_name, season)
        marks, dates, units, wind2, wind4 = db.get_athlete2_results(athlete_id, event_name, season)
        sc.axes.plot(dates, marks, color = 'orange', marker = 'o', linestyle = 'None')
        sc.axes.plot(dates, marks, color = 'black', marker ='.')
        ath_name = db.get_ahtlete_name(athlete_id)
        #ath_name2 = db.get_athlete_name(athlete_id)
        sc.axes.set(xlabel = "Years", ylabel = units, title = '{} - {} {}'.format(ath_name,season,event_name))

        years = mdates.YearLocator()
        months = mdates.MonthLocator()
        years_fmt = mdates.DateFormatter('%Y')
        time = mdates.AutoDateLocator()
        time_fmt = mdates.AutoDateFormatter(time)

        sc.axes.xaxis.set_major_locator(years)
        sc.axes.xaxis.set_major_formatter(years_fmt)
        sc.axes.xaxis.set_minor_locator(months)

        datemin = datetime(dates[0].year,1,1)
        datemax = datetime(dates[-1].year + 1,1,1)
        sc.axes.set_xlim(datemin,datemax)
        if units != 'Meters':
            print('formatting y axis')
            sc.axes.yaxis.set_major_locator(time)
            sc.axes.yaxis.set_major_formatter(time_fmt)
            sc.axes.format_ydata = mdates.DateFormatter('%M:%S.%f')

        sc.axes.format_xdata = mdates.DateFormatter('%Y-%m-%d')
        sc.fig.autofmt_xdate()

        MainWindow.setCentralWidget(self.centralwidget)


class Canvas(FigureCanvas):
    def __init__(self,parent=None, width = 400, height= 400, dpi=100):
        px = 1/plt.rcParams['figure.dpi']
        self.fig=Figure(figsize=(width*px,height*px),dpi=dpi)
        self.axes= self.fig.add_subplot(111)
        super(Canvas, self).__init__(self.fig)
        self.setParent(parent)

class StatViewer(object):
    def setupStatViewer(self, MainWindow, athlete_id):
        MainWindow.setGeometry(TOP,LEFT,WIDTH,HEIGHT)
        MainWindow.setWindowTitle("TFRRS Visualizer")
        MainWindow.setStyleSheet("background-color: gray;")
        self.centralwidget = QWidget(MainWindow)

#Statistics description label
        self.statDescriptionLabel = QLabel(self.centralwidget)
        self.statDescriptionLabel.setText("Statistics for Selected Athlete(s) and Event")
        self.statDescriptionLabel.setGeometry(150,25,400,50)
        self.statDescriptionLabel.setStyleSheet('QLabel {color: Orange}')
        self.statDescriptionLabel.setFont(QFont("Arial", 20))

#Athlete 1 Name and Stats
        self.ath1 = QLabel(self.centralwidget)
        self.ath1.setText("Athlete 1 Goes Here")
        self.ath1.setGeometry(75,100,150,25)
        self.ath1.setStyleSheet('QLabel {font-weight: bold; color: Orange}')
        self.ath1.setFont(QFont("Arial", 15))

        self.ath1PR = QLabel(self.centralwidget)
        test = db.get_athlete_pr(self, athlete_id, event_name)
        self.ath1PR.setText(test)
        self.ath1PR.setGeometry(75,150,150,25)
        self.ath1PR.setAlignment(Qt.AlignCenter)

        self.ath1PR1 = QLabel(self.centralwidget)
        self.ath1PR1.setText("3.56")
        self.ath1PR1.setGeometry(75,200,150,25)
        self.ath1PR1.setAlignment(Qt.AlignCenter)

        self.ath1Imp = QLabel(self.centralwidget)
        self.ath1Imp.setText("3.56")
        self.ath1Imp.setGeometry(75,250,150,25)
        self.ath1Imp.setAlignment(Qt.AlignCenter)

        self.ath1Imp1 = QLabel(self.centralwidget)
        self.ath1Imp1.setText("3.56")
        self.ath1Imp1.setGeometry(75,300,150,25)
        self.ath1Imp1.setAlignment(Qt.AlignCenter)

#Athlete 2 Name
        self.ath2 =QLabel(self.centralwidget)
        self.ath2.setText("Athlete 2 Goes Here")
        self.ath2.setGeometry(475,100,150,25)
        self.ath2.setStyleSheet('QLabel {font-weight: bold; color: Orange}')
        self.ath2.setFont(QFont("Arial", 15))

        self.ath2PR = QLabel(self.centralwidget)
        self.ath2PR.setText("3.56")
        self.ath2PR.setGeometry(475,150,150,25)
        self.ath2PR.setAlignment(Qt.AlignCenter)

        self.ath2PR1 = QLabel(self.centralwidget)
        self.ath2PR1.setText("3.56")
        self.ath2PR1.setGeometry(475,200,150,25)
        self.ath2PR1.setAlignment(Qt.AlignCenter)

        self.ath2Imp = QLabel(self.centralwidget)
        self.ath2Imp.setText("3.56")
        self.ath2Imp.setGeometry(475,250,150,25)
        self.ath2Imp.setAlignment(Qt.AlignCenter)

        self.ath2Imp1 = QLabel(self.centralwidget)
        self.ath2Imp1.setText("3.56")
        self.ath2Imp1.setGeometry(475,300,150,25)
        self.ath2Imp1.setAlignment(Qt.AlignCenter)

#Personal Best Label
        self.prLabel = QLabel(self.centralwidget)
        self.prLabel.setText("PR")
        self.prLabel.setGeometry(300,150,100,25)
        self.prLabel.setStyleSheet('QLabel {font-weight: bold; color: Orange}')
    #Need PB Input

#Personal Best 1st Year
        self.pr1Label = QLabel(self.centralwidget)
        self.pr1Label.setText("PR (First Year)")
        self.pr1Label.setGeometry(300,200,100,25)
        self.pr1Label.setStyleSheet('QLabel {font-weight: bold; color: Orange}')

#Improvement Overall
        self.OverallImpLabel = QLabel(self.centralwidget)
        self.OverallImpLabel.setText("Overall Imp")
        self.OverallImpLabel.setGeometry(300,250,100,25)
        self.OverallImpLabel.setStyleSheet('QLabel {font-weight: bold; color: Orange}')

#Improvement First Year
        self.Imp1Label= QLabel(self.centralwidget)
        self.Imp1Label.setText("Imp (First Year)")
        self.Imp1Label.setGeometry(300,300,100,25)
        self.Imp1Label.setStyleSheet('QLabel {font-weight: bold; color: Orange}')


#Button to go back to athlete selector window
        self.backButton = QPushButton(self.centralwidget)
        self.backButton.setText("Back")
        self.backButton.setGeometry(275,425,150,50)
        self.backButton.setStyleSheet("background-color: orange;")
        self.backButton.setFont(QFont('Arial', 15))

        MainWindow.setCentralWidget(self.centralwidget)


class MainWindow(QMainWindow):

    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.startWindow = StartWindow()
        self.collegeSelection = CollegeSelection()
        self.athleteSelection = AthleteSelection()
        self.graphViewer = GraphViewer()
        self.statViewer = StatViewer()
        self.startStartWindow()

    def startStartWindow(self):
        self.startWindow.setupStartWindow(self)
        self.startWindow.continueButton.clicked.connect(self.startCollegeSelection)
        self.show()


    def startCollegeSelection(self):
        self.collegeSelection.setupCollegeSelection(self)
        self.collegeSelection.nextButton.clicked.connect(self.startAthleteSelection)
        self.collegeSelection.gender.activated.connect(self.collegeSelection.genderchange)
        self.collegeSelection.division.activated.connect(self.collegeSelection.divisionchange)
        self.collegeSelection.college.activated.connect(self.collegeSelection.collegechange)
        self.show()



    def startAthleteSelection(self):
        self.athleteSelection.setupAthleteSelection(self,self.collegeSelection.college_id)
        self.athleteSelection.backButton.clicked.connect(self.startCollegeSelection)
        self.athleteSelection.updateButton.clicked.connect(self.startGraphViewer)
        self.athleteSelection.season.activated.connect(self.athleteSelection.seasonChange)
        self.athleteSelection.event.activated.connect(self.athleteSelection.eventChange)
        self.athleteSelection.athlete.activated.connect(self.athleteSelection.athleteChange)
        self.athleteSelection.statButton.clicked.connect(self.startStatViewer)
        self.show()

    def startGraphViewer(self):
        self.graphViewer.setupGraphViewer(self, self.athleteSelection.ath_id, self.athleteSelection.event_picked, self.athleteSelection.season_picked)
        self.graphViewer.backButton.clicked.connect(self.startAthleteSelection)

        self.show()

    def startStatViewer(self):
        self.statViewer.setupStatViewer(self, athlete_id)
        self.statViewer.backButton.clicked.connect(self.startAthleteSelection)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())
