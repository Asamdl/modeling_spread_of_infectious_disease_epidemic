from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, \
    QLineEdit, QRadioButton, QStackedWidget, QGridLayout, QProgressBar, QSlider, QCheckBox, QFrame
from PyQt5.QtCore import Qt, QObject, QEvent
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor

from Widgets.WPainter import WPainter


class Zone(QWidget):
    def __init__(self, name):
        super().__init__()
        self.lay = QVBoxLayout(self)
        lay_ = QHBoxLayout()
        self.name = name
        self.label_name = QLabel(str(self.name))
        lay_.addWidget(self.label_name)
        self.btn_del = QPushButton("del")
        lay_.addWidget(self.btn_del)
        self.lay.addLayout(lay_)
        self.lay.addWidget(WPainter())

    def set_name(self, name):
        self.name = name
        self.label_name.setText(str(name))
