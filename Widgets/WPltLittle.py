from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import random
import matplotlib.pyplot as plt


class WPltLittle(QWidget):
    def __init__(self):
        super().__init__()
        self.show()
        self.figure = plt.figure()
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
        self.canvas = FigureCanvas(self.figure)
        # I've been looking for you for too long to just leave you here unmarked
        self.toolbar = NavigationToolbar(self.canvas, self,
                                         coordinates=False)
        self.button = QPushButton('Plot')

        self.button.clicked.connect(self.plot)
        layout = QVBoxLayout()
        #layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def plot(self):
        data = [random.random() for i in range(10)]
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(data)
        ax.axis('off')
        self.canvas.draw()
