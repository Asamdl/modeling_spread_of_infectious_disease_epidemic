from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, \
    QLineEdit, QRadioButton, QStackedWidget, QGridLayout, QProgressBar, QSlider, QCheckBox, QFrame, QScrollArea, \
    QListWidget, QListWidgetItem, QScrollBar

from Widgets.WAddZone import WAddZone
from Widgets.WZone import WZone
from functools import partial
from PyQt5.QtCore import Qt, QObject, QEvent

from Widgets.WZoneElement import WZoneElement


class WListZone(QWidget):
    def __init__(self):
        super().__init__()
        self.number_of_zones = 3

        self.zones = dict()
        self.layout = QVBoxLayout(self)
        self.layout.addStretch()
        self.widget = QWidget()
        self.vbox = QVBoxLayout(self.widget)

        for i in range(3):
            w = QWidget()
            hbox = QHBoxLayout(w)
            hbox.addWidget(WZoneElement(str(i)))

            self.vbox.addWidget(w)

        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        self.layout.addWidget(self.scroll)
        self.layout.addStretch()


