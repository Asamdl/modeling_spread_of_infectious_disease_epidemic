from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, \
    QLineEdit, QRadioButton, QStackedWidget, QGridLayout, QProgressBar, QSlider, QCheckBox, QFrame
from PyQt5.QtCore import Qt, QObject, QEvent
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor
import random


class WPainter(QWidget):
    def __init__(self):
        super().__init__()
        self.colors = [Qt.red, Qt.black, Qt.white, Qt.yellow]

    def mousePressEvent(self, e):
        if e.buttons() == Qt.LeftButton:
            print(e.x(), e.y())

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        color = random.choice(self.colors)
        painter.setBrush(QBrush(color, Qt.CrossPattern))
        w = self.geometry().width()
        h = self.geometry().height()
        painter.drawRect(0, 0, w, h)
