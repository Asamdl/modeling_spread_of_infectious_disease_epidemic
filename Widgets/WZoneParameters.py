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
        layout_name = QHBoxLayout()
        self.label_name_zone = QLabel("")
        self.label_name_zone.setAlignment(Qt.AlignRight)
        layout_name.addWidget(QLabel("Название:"))
        layout_name.addWidget(self.label_name_zone)
        layout_self.addLayout(layout_name)
        layout_self.addWidget(self.widget_for_stage_values)
        layout_self.addWidget(QPushButton("apply"))
        layout_self.setAlignment(Qt.AlignTop)
        self.disable_all_elements()

    def disable_all_elements(self):
        self.widget_for_stage_values.disable_all_elements()

    def enable_all_elements(self):
        self.widget_for_stage_values.enable_all_elements()

    def set_name_zone(self, name):
        self.label_name_zone.setText(name)
        if name != "":
            self.enable_all_elements()
        else:
            self.disable_all_elements()
