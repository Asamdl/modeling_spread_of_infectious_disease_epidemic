from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QComboBox

from Widgets.DZoneConnection import DZoneConnection
from Widgets.WSetModelParameters import WSetModelParameters
from classes import ZoneParameters


class WZoneParameters(QWidget):
    def __init__(self, zones: dict[ZoneParameters], parent=None):
        QWidget.__init__(self, parent=parent)
        self.zones = zones
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
        layout_self.addWidget(QLabel("Связи"))
        self.friendly_zones = QComboBox()
        self.friendly_zones.activated.connect(self.print_selected_zone)
        layout_friendly_zones = QHBoxLayout()
        layout_friendly_zones.addWidget(self.friendly_zones)
        btn_add_friendly_zone = QPushButton("+")
        btn_add_friendly_zone.setFixedWidth(25)
        btn_add_friendly_zone.clicked.connect(self.set_connection_value)
        layout_friendly_zones.addWidget(btn_add_friendly_zone)
        layout_self.addLayout(layout_friendly_zones)
        self.update_visual_data_of_zones()
        layout_self.setAlignment(Qt.AlignTop)
        self.disable_all_elements()

    def update_visual_data_of_zones(self):
        if self.label_name_zone.text() in self.zones:
            self.friendly_zones.clear()
            for zone_name in self.zones[self.label_name_zone.text()].connections.keys():
                self.friendly_zones.addItem(zone_name)

    def set_connection_value(self):
        if self.label_name_zone.text() in self.zones:
            friendly_zone, value, result = DZoneConnection.get_connections_value(
                list(set(list(self.zones[self.label_name_zone.text()].connections.keys())+
                         [self.label_name_zone.text()]).symmetric_difference(
                    self.zones.keys())))
            if result:
                self.zones[self.label_name_zone.text()].set_connection(friendly_zone, value)
                self.update_visual_data_of_zones()

    def print_selected_zone(self, index):
        print(self.friendly_zones.currentText())

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
