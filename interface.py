import typing

from PyQt5 import QtGui, QtCore, QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, \
    QLineEdit, QRadioButton, QStackedWidget, QGridLayout, QProgressBar, QSlider, QCheckBox, QFrame, QScrollArea
import sys
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor
from PyQt5.QtCore import Qt, QObject, QEvent
from PyQt5.uic import loadUi
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import random
import matplotlib.pyplot as plt

from Widgets.WAddZone import WAddZone
from Widgets.WCreatingModel import WCreatingModel
from Widgets.WListZone import WListZone
from Widgets.WPltBig import WPltBig
from Widgets.WPltLittle import WPltLittle
from Widgets.WSetModelParameters import WSetModelParameters
from Widgets.WZoneConstructor import WZoneConstructor


class box(QWidget):
    def __init__(self, name: str, top=None, left=None, width=None, height=None):
        super().__init__()
        self.name = name
        self.colors = [Qt.red, Qt.black, Qt.white, Qt.yellow]
        self.InitWindow()

    def InitWindow(self):
        self.show()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_:
            self.close()

    def mousePressEvent(self, e):
        if e.buttons() == Qt.LeftButton:
            # s = e.pos()
            print(self.name)
            print(e.x(), e.y())

    def paintEvent(self, event=None, changing_number=None):

        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        color = random.choice(self.colors)
        print(color)
        painter.setBrush(QBrush(color, Qt.CrossPattern))
        w = self.geometry().width()
        h = self.geometry().height()
        painter.drawRect(0, 0, w, h)


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "PyQt5"
        self.top = 50
        self.left = 50
        self.width = 1000
        self.height = 650
        grid = QGridLayout()
        self.setLayout(grid)
        positions = [
            (0, 0, 1, 2),
            (0, 2, 1, 1),
            (1, 0, 1, 1),
            (1, 1, 1, 1),
            (1, 2, 1, 1)
        ]
        # row: int, column: int, rowSpan: int, columnSpan: int
        for position in positions:
            if position[0] == 0 and position[1] == 0:
                lay00 = QVBoxLayout()
                lay00.addStretch()
                lay_ = QGridLayout()
                label = QLabel("Создание зон")
                label.setAlignment(QtCore.Qt.AlignCenter)
                lay00.addWidget(label)
                lay00.addWidget(WListZone())


                lay00.addStretch()
                slider = QSlider(Qt.Horizontal)
                slider.valueChanged.connect(self.update_color_for_zones)
                lay00.setAlignment(Qt.AlignmentFlag.AlignTop)
                lay00.addWidget(slider)

                grid.setAlignment(Qt.AlignmentFlag.AlignTop)
                grid.addLayout(lay00, *position)
            elif position[0] == 0 and position[1] == 2:
                plotlib = WPltBig()
                lay_ = QVBoxLayout()
                lay_.addWidget(plotlib)
                # grid.addLayout(lay_, 0,2)
                grid.addLayout(lay_, 0, 2)
            elif position[0] == 1 and position[1] == 1:
                lay_ = QVBoxLayout()
                lay_.addWidget(WCreatingModel())
                grid.addLayout(lay_, *position)
            else:
                # label = QLabel(name)
                widget = Widget1()
                # label.setStyleSheet('QLabel {background-color: #A3C1DA; color: red;}')
                grid.addWidget(widget, *position)
        self.InitWindow()

    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)

    def update_color_for_zones(self):
        pass


class Widget1(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        lay = QVBoxLayout(self)
        for i in range(4):
            lay.addWidget(QPushButton("{}".format(i)))


class widget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        uic.loadUi('test_element.ui', self)








class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.widget = QWidget()
        self.v = QVBoxLayout(self.widget)
        for i in range(10):
            w = QWidget()
            hbox = QHBoxLayout(w)
            hbox.addWidget(WAddZone())
            self.v.addWidget(w)

        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        self.setCentralWidget(self.scroll)
def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
