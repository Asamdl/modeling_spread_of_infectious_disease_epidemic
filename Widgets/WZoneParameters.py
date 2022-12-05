from PyQt5 import QtCore
from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QGridLayout, QCheckBox
from PyQt5.QtCore import Qt
from Widgets.WSetModelParameters import WSetModelParameters


class WZoneParameters(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self.name_of_inactive_stages = ["S", "I"]
        self.checkbox_states = dict()
        self.checkbox_states["S"] = True
        self.checkbox_states["I"] = True
        self.stages_widgets = dict()
        self.widget_for_stage_values = WSetModelParameters(self.checkbox_states)
        layout_self = QVBoxLayout(self)
        layout_self.addWidget(QLabel("Устанвка значений"))
        layout_self.addWidget(self.widget_for_stage_values)
        layout_self.addWidget(QPushButton("apply"))
        layout_self.setAlignment(Qt.AlignTop)
