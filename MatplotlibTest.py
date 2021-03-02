#How to embed Matplotlib in pyqt5

from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Selected Athlete(s) Results")
        self.setGeometry(400,400,900,500)

        self.MyUI()

    def MyUI(self):

        canvas= Canvas(self,width=5, height=5)
        canvas.move(0,0)
        

class Canvas(FigureCanvas):
    def __init__(self, parent= None, width = 5, height = 5, dpi = 100):
        fig= Figure(figsize=(width, height), dpi=dpi)
        self.axes= fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        self.plot()


    def plot(self):
        x = np.array([50,30,40])
        labels= ["Apples", "Bananas", "Melons"]
        ax= self.figure.add_subplot(111)
        ax.pie(x, labels=labels)
        
        
        
        


app = QApplication(sys.argv)
window = Window()
window.show()
app.exec()
