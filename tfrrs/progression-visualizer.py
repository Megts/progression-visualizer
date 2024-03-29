#TFRRS Visualizer Program
#By: Nick Meling and Matt Egts

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from ncaa_db_queries import DB
import numpy as np
from numpy import datetime64, timedelta64
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter, AutoMinorLocator


db = DB('ncaa.db')
TOP = 400
LEFT = 150
WIDTH = 700
HEIGHT = 500
# Handle high resolution displays:
if hasattr(Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)


class StartWindow(object):
    def setupStartWindow(self, MainWindow):
#Window set up
        MainWindow.setGeometry(TOP,LEFT,WIDTH,HEIGHT)
        MainWindow.setFixedSize(700,500)
        MainWindow.setWindowTitle("TFRRS Visualizer")
        MainWindow.setStyleSheet("background-color: Light gray")
        self.centralwidget = QWidget(MainWindow)

#Text description
        self.descriptionLabel = QLabel("This program will allow you to visualize athlete statistics in Cross Country or Track and Field. You will be prompted to select NCAA Division, Gender, College, Sport, and Event.",
                                        self.centralwidget)
        self.descriptionLabel.setWordWrap(True)
        self.descriptionLabel.setFont(QFont("Arial"))
        self.descriptionLabel.setAlignment(Qt.AlignCenter)
        self.descriptionLabel.setGeometry(5,10,690,400)
        self.descriptionLabel.setStyleSheet('color: Blue; font-size: 30px')

#Button to continue to next window
        self.continueButton = QPushButton("Click here to continue", self.centralwidget)
        self.continueButton.setGeometry(5,450,690,30)
        #self.continueButton.setStyleSheet("background-color: Light gray;")
        self.continueButton.setStyleSheet("background-color: Blue;  color: White; font-size: 20px")
        self.continueButton.setFont(QFont("Arial"))

        MainWindow.setCentralWidget(self.centralwidget)


class CollegeSelection(object):

    def __init__(self):
        self.div_i = 0
        self.gen_lst = ['m','f']
        self.gen_i = 0
        self.gen = self.gen_lst[self.gen_i]
        self.college_i = 0
        self.athlete_i = 0
        self.season_i = 0
        self.event_i = 0

    def setupCollegeSelection(self, MainWindow):
        print('setting up new window')
        wpadding= 50
        hpadding= 25
        hboxpadding= 25
        labelw=150
        labelh=25
        MainWindow.setGeometry(TOP,LEFT,WIDTH,HEIGHT)
        MainWindow.setFixedSize(WIDTH, HEIGHT)
        MainWindow.setWindowTitle("TFRRS Visualizer")
        MainWindow.setStyleSheet("background-color:  Light gray")
        self.centralwidget = QWidget(MainWindow)

#Division Selector
        self.division = QComboBox(self.centralwidget)
        self.division.setGeometry(350,25,175,40)
        self.division.addItem('Divsion 1')
        self.division.addItem('Divison 2')
        self.division.addItem('Division 3')
        #self.division.setFont(QFont("Arial", 20))
        #self.division.setStyleSheet("text-color: blue;")
        self.division.setEditable(True)
        self.division.setCurrentIndex(self.div_i)
        self.line_edit = self.division.lineEdit()
        self.line_edit.setAlignment(Qt.AlignCenter)
        self.line_edit.setReadOnly(True)
        self.div = self.div_i +1

        self.divisionLabel= QLabel(self.centralwidget)
        self.divisionLabel.setText('Division')
        self.divisionLabel.setGeometry(150,25,150,40)
        self.divisionLabel.setAlignment(Qt.AlignCenter)
        self.divisionLabel.setStyleSheet('QLabel {color: Blue; font-size: 20px}')
        self.divisionLabel.setFont(QFont("Arial"))

#Gender Selector
        self.gender= QComboBox(self.centralwidget)
        self.gender.setGeometry(350,90,175,40)
        self.gender.addItem('Male')
        self.gender.addItem('Female')
        #self.gender.setStyleSheet("background-color: orange;")
        #self.gender.setFont(QFont("Arial", 20))
        self.gender.setEditable(True)
        self.gender.setCurrentIndex(self.gen_i)
        self.line_edit = self.gender.lineEdit()
        self.line_edit.setAlignment(Qt.AlignCenter)
        self.line_edit.setReadOnly(True)

        self.genderLabel= QLabel(self.centralwidget)
        self.genderLabel.setText('Gender')
        self.genderLabel.setGeometry(150,90,150,40)
        self.genderLabel.setAlignment(Qt.AlignCenter)
        self.genderLabel.setStyleSheet('QLabel {color: Blue; font-size: 20px}')
        self.genderLabel.setFont(QFont('Arial'))

#College Selector
        self.college= QComboBox(self.centralwidget)
        self.college.setGeometry(350,155,175,40)
        self.name_id = db.get_div_teams(self.div, self.gen)
        team_names = [name for name, id in self.name_id]
        self.college.addItems(team_names)
        self.college_id = self.name_id[self.college_i][1]
        #self.college.setStyleSheet("background-color: orange;")
        self.college.setEditable(True)
        self.college.setCurrentIndex(self.college_i)
        self.line_edit = self.college.lineEdit()
        self.line_edit.setAlignment(Qt.AlignCenter)
        self.line_edit.setReadOnly(True)

        self.collegeLabel= QLabel(self.centralwidget)
        self.collegeLabel.setText('College')
        self.collegeLabel.setGeometry(150,155,150,40)
        self.collegeLabel.setAlignment(Qt.AlignCenter)
        self.collegeLabel.setStyleSheet('QLabel {color: Blue; font-size: 20px}')
        self.collegeLabel.setFont(QFont('Arial'))

#Athlete Selector
        self.athlete=QComboBox(self.centralwidget)
        self.athlete.setGeometry(350,220,175,40)
        self.athletes = db.get_init_team_roster(self.college_id)
        athlete_names = [name for name, id in self.athletes]
        if len(self.athletes) > 0:
            athlete_names = [name for name, id in self.athletes]
            self.ath_id = self.athletes[self.athlete_i][1]
        else:
            athlete_names = []
            self.ath_id = None
        self.athlete.addItems(athlete_names)
        #self.athlete.setStyleSheet("background-color: orange;")
        self.athlete.setEditable(True)
        self.athlete.setCurrentIndex(self.athlete_i)
        self.line_edit = self.athlete.lineEdit()
        self.line_edit.setAlignment(Qt.AlignCenter)
        self.line_edit.setReadOnly(True)

        self.athleteLabel= QLabel(self.centralwidget)
        self.athleteLabel.setText("Athlete")
        self.athleteLabel.setAlignment(Qt.AlignCenter)
        self.athleteLabel.setGeometry(150,220,150,40)
        self.athleteLabel.setAlignment(Qt.AlignCenter)
        self.athleteLabel.setStyleSheet('QLabel {color: Blue; font-size: 20px}')
        self.athleteLabel.setFont(QFont("Arial"))

#Season Selector
        self.season= QComboBox(self.centralwidget)
        self.season.setGeometry(350,285,175,40)
        seasons = db.get_athlete_seasons(self.ath_id)
        self.season.addItems(seasons)
        #self.season.setStyleSheet("background-color: orange;")
        self.season.setCurrentIndex(self.season_i)
        self.season_picked = self.season.currentText()
        self.season.setEditable(True)
        self.line_edit = self.season.lineEdit()
        self.line_edit.setAlignment(Qt.AlignCenter)
        self.line_edit.setReadOnly(True)

        self.seasonLabel= QLabel(self.centralwidget)
        self.seasonLabel.setText('Season')
        self.seasonLabel.setGeometry(150,285,150,40)
        self.seasonLabel.setAlignment(Qt.AlignCenter)
        self.seasonLabel.setStyleSheet('QLabel {color: Blue; font-size: 20px}')
        self.seasonLabel.setFont(QFont("Arial"))

#Event Selector
        self.event= QComboBox(self.centralwidget)
        self.event.setGeometry(350,350,175,40)
        events = db.get_athlete_season_events(self.ath_id, self.season_picked)
        self.event.addItems(events)
        self.event.setCurrentIndex(self.event_i)
        self.event_picked = self.event.currentText()
        #self.event.setStyleSheet("background-color: orange;")
        self.event.setEditable(True)
        self.line_edit = self.event.lineEdit()
        self.line_edit.setAlignment(Qt.AlignCenter)
        self.line_edit.setReadOnly(True)

        self.eventLabel = QLabel(self.centralwidget)
        self.eventLabel.setText('Event')
        self.eventLabel.setGeometry(150,350,150,40)
        self.eventLabel.setAlignment(Qt.AlignCenter)
        self.eventLabel.setStyleSheet('QLabel {color: Blue; font-size: 20px}')
        self.eventLabel.setFont(QFont("Arial"))

        MainWindow.setCentralWidget(self.centralwidget)

#Update Button
        self.graphButton= QPushButton(self.centralwidget)
        self.graphButton.setText("Plot Selected Event")
        self.graphButton.setGeometry(25,425,200,40)
        self.graphButton.setStyleSheet("background-color: Blue;  color: White; font-size: 20px")
        self.graphButton.setFont(QFont("Arial"))
        #self.graphButton.setBackground(
        #self.graphButton.setStyleSheet('color: White;')

        MainWindow.setCentralWidget(self.centralwidget)

#Button to go to statViewer window
        self.statButton=QPushButton(self.centralwidget)
        self.statButton.setText("View Athlete Stats")
        self.statButton.setGeometry(250,425,200,40)
        self.statButton.setStyleSheet("background-color: Blue;  color: White; font-size: 20px")
        self.statButton.setFont(QFont("Arial"))

        MainWindow.setCentralWidget(self.centralwidget)

#Update Roster
        self.updateRoster= QPushButton(self.centralwidget)
        self.updateRoster.setText("Update Roster")
        self.updateRoster.setGeometry(475,425,200,40)
        self.updateRoster.setStyleSheet("background-color: Blue;  color: White; font-size: 20px")
        self.updateRoster.setFont(QFont("Arial"))

        self.toggle_buttons()

        MainWindow.setCentralWidget(self.centralwidget)

    def toggle_buttons(self):
        print(self.ath_id, self.event_picked)
        if self.event_picked == '':
            self.graphButton.blockSignals(True)
            self.statButton.blockSignals(True)
            self.graphButton.setStyleSheet("background-color: Red;  color: White; font-size: 20px")
            self.statButton.setStyleSheet("background-color: Red;  color: White; font-size: 20px")
        else:
            self.graphButton.blockSignals(False)
            self.statButton.blockSignals(False)
            self.graphButton.setStyleSheet("background-color: Blue;  color: White; font-size: 20px")
            self.statButton.setStyleSheet("background-color: Blue;  color: White; font-size: 20px")


    def divisionchange(self,i):
        if i != -1:
            self.div_i = i
            self.college.clear()
            self.div = self.div_i + 1
            self.update_colleges()

    def genderchange(self, i):
        if i != -1:
            self.gen_i = i
            self.gen = self.gen_lst[self.gen_i]
            self.update_colleges()

    def collegechange(self,i):
        if i != -1:
            self.college_i = i
            self.college_id = self.name_id[self.college_i][1]
            self.update_athletes()

    def athleteChange(self,i):
        if i != -1:
            self.athlete_i = i
            self.ath_id = self.athletes[self.athlete_i][1]
            self.update_seasons()


    def seasonChange(self,i):
        if i != -1:
            self.season_i = i
            self.season_picked = self.season.itemText(self.season_i)
            self.update_events()

    def eventChange(self, i):
        if i != -1:
            self.event_i = i
            self.event_picked = self.event.itemText(self.event_i)

    def update_colleges(self):
        self.name_id = db.get_div_teams(self.div, self.gen)
        team_names = [name for name, id in self.name_id]
        self.college_i = 0
        self.college_id = self.name_id[self.college_i][1]
        self.college.clear()
        self.college.addItems(team_names)
        self.update_athletes()

    def update_athletes(self):
        self.athletes = db.get_init_team_roster(self.college_id)
        if len(self.athletes) > 0:
            athlete_names = [name for name, id in self.athletes]
            self.athlete_i = 0
            self.ath_id = self.athletes[self.athlete_i][1]
        else:
            athlete_names = []
            self.ath_id = None
        self.athlete.clear()
        self.athlete.addItems(athlete_names)
        self.update_seasons()

    def update_seasons(self):
        self.season_i = 0
        seasons = db.get_athlete_seasons(self.ath_id)
        self.season.clear()
        self.season.addItems(seasons)
        self.season_picked = self.season.currentText()
        self.update_events()

    def update_events(self):
        events = db.get_athlete_season_events(self.ath_id, self.season_picked)
        self.event.clear()
        self.event.addItems(events)
        self.event_i = 0
        self.event_picked = self.event.currentText()
        self.toggle_buttons()

    def update_roster(self):
        db.update_college_roster(self.college_id)
        self.update_athletes()
        self.updateRoster.blockSignals(True)




'''class AthleteSelection(object):
    def setupAthleteSelection(self, MainWindow, college_id):

        MainWindow.setGeometry(TOP,LEFT,WIDTH,HEIGHT)
        MainWindow.setWindowTitle("TFRRS Visualizer")
        MainWindow.setStyleSheet("background-color: gray;")
        self.centralwidget = QWidget(MainWindow)










#Back Button
        self.backButton=QPushButton(self.centralwidget)
        self.backButton.setText("Back")
        self.backButton.setGeometry (50,425, 150, 50)
        self.backButton.setStyleSheet("background-color: orange;")

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


    '''

class GraphViewer(object):
    def setupGraphViewer(self, MainWindow, athlete_ids, event_name, season):
        MainWindow.setGeometry(TOP,LEFT,WIDTH,HEIGHT)
        MainWindow.setWindowTitle("TFRRS Visualizer")
        MainWindow.setStyleSheet("background-color: Light gray;")
        self.centralwidget = QWidget(MainWindow)

#Back Button on Graph
        self.backButton=QPushButton(self.centralwidget)
        self.backButton.setText("Back")
        self.backButton.setGeometry (25,435, 650, 40)
        self.backButton.setStyleSheet("background-color: Blue;  color: White; font-size: 20px")
        self.backButton.setFont(QFont("Arial"))

        MainWindow.setCentralWidget(self.centralwidget)



#Graph Formatting and Inputs
        sc = Canvas(self.centralwidget, width = 650, height = 400)
        sc.move((WIDTH-650)//2,15)
        colors = {2015:'k',2016:'y',2017:'m',2018:'c',2019:'r',2020:'g',2021:'b'}
        lstyes = ['-',':','--','-.']
        units = None
        for athlete_id in athlete_ids:
            ath_name = db.get_ahtlete_name(athlete_id)
            completed_seasons, units = db.get_athlete_results(athlete_id, event_name, season)
            for year in completed_seasons:
                marks,wind2,wind4,dates,season_year = year
                sc.axes.plot(dates, marks, color=colors[season_year], linestyle='-', marker='o', label=f'{ath_name} {season_year}')

        sc.axes.set(xlabel = "Months", ylabel = units, title = f'{season} {event_name}')
        sc.axes.legend()

        years = mdates.YearLocator()
        months = mdates.MonthLocator()
        time = mdates.AutoDateLocator()
        months_fmt = mdates.DateFormatter('%b')
        time_fmt = FuncFormatter(self.time_to_4digs)

        if season == 'XC':
            datemin = np.datetime64('2000-08-24')
            datemax = np.datetime64('2000-12-01')
        if season == 'Indoor':
            datemin = np.datetime64('1999-12-01')
            datemax = np.datetime64('2000-03-21')
        if season == 'Outdoor':
            datemin = np.datetime64('2000-03-01')
            datemax = np.datetime64('2000-07-01')
        sc.axes.set_xlim(datemin,datemax)

        sc.axes.xaxis.set_major_locator(months)
        sc.axes.xaxis.set_major_formatter(months_fmt)
        sc.axes.xaxis.set_minor_locator(AutoMinorLocator(4))

        if units == 'Time':
            sc.axes.yaxis.set_major_locator(time)
            sc.axes.yaxis.set_major_formatter(time_fmt)

        MainWindow.setCentralWidget(self.centralwidget)

    def time_to_4digs(self, time, pos = None):
        timestr = mdates.num2date(time).strftime('%M:%S.%f')
        while timestr[0] in ['0',':']:
            timestr = timestr[1:]
        if ':' in timestr:
            return timestr.split('.')[0]
        return timestr[:5]

class Canvas(FigureCanvas):
    def __init__(self,parent=None, width = 400, height= 400, dpi=100):
        px = 1/plt.rcParams['figure.dpi']
        self.fig=Figure(figsize=(width*px,height*px),dpi=dpi)
        self.axes= self.fig.add_subplot(111)
        super(Canvas, self).__init__(self.fig)
        self.setParent(parent)

class StatViewer(object):
    def setupStatViewer(self, MainWindow, athlete_id, event_name, season):
        MainWindow.setGeometry(TOP,LEFT,WIDTH,HEIGHT)
        MainWindow.setWindowTitle("TFRRS Visualizer")
        MainWindow.setStyleSheet("background-color: Light gray;")
        self.centralwidget = QWidget(MainWindow)

#Athlete 1 Name and Stats
        ath_name = db.get_ahtlete_name(athlete_id)
        self.ath1 = QLabel(self.centralwidget)
        self.ath1.setText(f"{ath_name}'s Career Stats in the {season} {event_name}")
        self.ath1.setGeometry(75,75,550,30)
        self.ath1.setStyleSheet('QLabel {font-size: 20px; font-weight: bold; color: Blue;}')
        self.ath1.setFont(QFont("Arial"))
        self.ath1.setAlignment(Qt.AlignCenter)

        pr = db.get_athlete_pr(athlete_id, event_name, season)
        if isinstance(pr, timedelta64):
            pr = db.format_timedelta(pr)
        self.ath1PR = QLabel(self.centralwidget)
        self.ath1PR.setText(str(pr))
        self.ath1PR.setGeometry(375,150,100,25)
        self.ath1PR.setAlignment(Qt.AlignCenter)
        self.ath1PR.setFont(QFont("Arial"))
        self.ath1PR.setStyleSheet('QLabel {font-size: 20px}')

        pr1 = db.get_athlete_first_year_pr(athlete_id, event_name, season)
        if isinstance(pr1, timedelta64):
            pr1 = db.format_timedelta(pr1)
        self.ath1PR1 = QLabel(self.centralwidget)
        self.ath1PR1.setText(str(pr1))
        self.ath1PR1.setGeometry(375,225,100,25)
        self.ath1PR1.setAlignment(Qt.AlignCenter)
        self.ath1PR1.setFont(QFont("Arial"))
        self.ath1PR1.setStyleSheet('QLabel {font-size: 20px}')

        imp = db.get_athlete_overall_imp(athlete_id, event_name, season)
        if isinstance(imp, timedelta64):
            imp = db.format_timedelta(imp)
        self.ath1Imp = QLabel(self.centralwidget)
        self.ath1Imp.setText(str(imp))
        self.ath1Imp.setGeometry(375,300,100,25)
        self.ath1Imp.setAlignment(Qt.AlignCenter)
        self.ath1Imp.setFont(QFont("Arial"))
        self.ath1Imp.setStyleSheet('QLabel {font-size: 20px}')

        imp1 = db.get_athlete_first_year_imp(athlete_id, event_name, season)
        if isinstance(imp1, timedelta64):
            imp1 = db.format_timedelta(imp1)
        self.ath1Imp1 = QLabel(self.centralwidget)
        self.ath1Imp1.setText(str(imp1))
        self.ath1Imp1.setGeometry(375,375,100,25)
        self.ath1Imp1.setAlignment(Qt.AlignCenter)
        self.ath1Imp1.setFont(QFont("Arial"))
        self.ath1Imp1.setStyleSheet('QLabel {font-size: 20px}')

#Personal Best Label
        self.prLabel = QLabel(self.centralwidget)
        self.prLabel.setText("Personal Best")
        self.prLabel.setGeometry(100,150,250,25)
        self.prLabel.setStyleSheet('QLabel {font-weight: bold; color: Blue; font-size: 20px;}')
        self.prLabel.setFont(QFont("Arial"))

#Personal Best 1st Year
        self.pr1Label = QLabel(self.centralwidget)
        self.pr1Label.setText("Season Best 1st Year")
        self.pr1Label.setGeometry(100,225,250,25)
        self.pr1Label.setStyleSheet('QLabel {font-weight: bold; color: Blue; font-size: 20px;}')
        self.pr1Label.setFont(QFont("Arial"))

#Improvement Overall
        self.OverallImpLabel = QLabel(self.centralwidget)
        self.OverallImpLabel.setText("Overall Improvement")
        self.OverallImpLabel.setGeometry(100,300,250,25)
        self.OverallImpLabel.setStyleSheet('QLabel {font-weight: bold; color: Blue; font-size: 20px;}')
        self.OverallImpLabel.setFont(QFont("Arial"))

#Improvement First Year
        self.Imp1Label= QLabel(self.centralwidget)
        self.Imp1Label.setText("Improvement 1st Year")
        self.Imp1Label.setGeometry(100,375,250,25)
        self.Imp1Label.setStyleSheet('QLabel {font-weight: bold; color: Blue; font-size: 20px;}')
        self.Imp1Label.setFont(QFont("Arial"))


#Button to go back to athlete selector window
        self.backButton = QPushButton(self.centralwidget)
        self.backButton.setText("Back")
        self.backButton.setGeometry(275,425,150,50)
        self.backButton.setGeometry (25,435, 650, 40)
        self.backButton.setStyleSheet("background-color: Blue;  color: White; font-size: 20px;")
        self.backButton.setFont(QFont("Arial"))

        MainWindow.setCentralWidget(self.centralwidget)


class MainWindow(QMainWindow):

    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.startWindow = StartWindow()
        self.collegeSelection = CollegeSelection()
        #self.athleteSelection = AthleteSelection()
        self.graphViewer = GraphViewer()
        self.statViewer = StatViewer()
        self.startStartWindow()

    def startStartWindow(self):
        self.startWindow.setupStartWindow(self)
        self.startWindow.continueButton.clicked.connect(self.startCollegeSelection)
        self.show()

    def startCollegeSelection(self):
        self.collegeSelection.setupCollegeSelection(self)
        #self.collegeSelection.nextButton.clicked.connect(self.startAthleteSelection)
        self.collegeSelection.gender.currentIndexChanged.connect(self.collegeSelection.genderchange)
        self.collegeSelection.division.currentIndexChanged.connect(self.collegeSelection.divisionchange)
        self.collegeSelection.college.currentIndexChanged.connect(self.collegeSelection.collegechange)
        self.collegeSelection.graphButton.clicked.connect(self.startGraphViewer)
        self.collegeSelection.updateRoster.clicked.connect(self.collegeSelection.update_roster)
        self.collegeSelection.season.currentIndexChanged.connect(self.collegeSelection.seasonChange)
        self.collegeSelection.event.currentIndexChanged.connect(self.collegeSelection.eventChange)
        self.collegeSelection.athlete.currentIndexChanged.connect(self.collegeSelection.athleteChange)
        self.collegeSelection.statButton.clicked.connect(self.startStatViewer)

        self.show()

    def startGraphViewer(self):
        if self.collegeSelection.ath_id != None:
            self.graphViewer.setupGraphViewer(self, [self.collegeSelection.ath_id], self.collegeSelection.event_picked, self.collegeSelection.season_picked)
            self.graphViewer.backButton.clicked.connect(self.startCollegeSelection)
            self.show()
        else:
            self.startCollegeSelection()

    def startStatViewer(self):
        if self.collegeSelection.ath_id != None:
            self.statViewer.setupStatViewer(self, self.collegeSelection.ath_id, self.collegeSelection.event_picked, self.collegeSelection.season_picked)
            self.statViewer.backButton.clicked.connect(self.startCollegeSelection)
            self.show()
        else:
            self.startCollegeSelection()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())
