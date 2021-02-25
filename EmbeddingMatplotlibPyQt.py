import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QWidget
#from ncaa_db_queries import DB

#db= DB('ncaa.db')

class Canvas(FigureCanvas):
    def __init__(self,parent):
        fig,self.ax= plt.subplots(figsize=(5,4),dpi=100,)
        super().__init__(fig)
        self.setParent(parent)

        #x and y data inputs
        date= [1,2,3,4,5,6]
        performance= [1,2,3,4,5,6]

        self.ax.plot(date,performance, color='orange', marker='o',label= 'athlete name goes here', linestyle='None')

        self.ax.set(xlabel='Dates', ylabel= 'Performance Time/Distance',
               title= 'Athlete Performances')
        self.ax.grid()
        self.ax.legend()
        self.resize(700,500)

class AppDemo(QWidget):
    def __init__(self):
        super().__init__()
        

        chart= Canvas(self)

app= QApplication(sys.argv)
demo= AppDemo()
demo.show()
sys.exit(app.exec_())
