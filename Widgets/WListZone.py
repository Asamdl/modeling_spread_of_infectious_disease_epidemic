from PyQt5 import QtWidgets
from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QListWidget, QListWidgetItem

from Widgets.WZoneParameters import WZoneParameters
from classes.ZoneParameters import CZoneParameters


class WListZone(QWidget):
    def __init__(self,zones):
        super().__init__()
        self.number_of_zones = 0
        self.zones = zones
        self.window_layout = QHBoxLayout(self)
        layout_list_zones = QVBoxLayout()
        layout_add_zone = QHBoxLayout()
        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText('Название зоны')
        self.btn = QtWidgets.QPushButton("Добавить")
        self.btn.clicked.connect(self.add_item)
        layout_add_zone.addWidget(self.input_name)
        layout_add_zone.addWidget(self.btn)
        layout_list_zones.addLayout(layout_add_zone)
        self.listWidget = QListWidget()
        self.listWidget.installEventFilter(self)
        self.listWidget.itemActivated.connect(self.item_activated_event)
        layout_list_zones.addWidget(self.listWidget)
        self.window_layout.addLayout(layout_list_zones)
        self.zone_parameters = WZoneParameters(zones=self.zones)
        self.window_layout.addWidget(self.zone_parameters)
        self.window_layout.setAlignment(Qt.AlignTop)

    def selectionChanged(self):
        el = self.listWidget.selectedItems()
        print("Selected items: ", self.listWidget.selectedItems())

    def update_list_widget(self):
        self.listWidget.clear()
        for zone_name in self.zones.keys():
            self.listWidget.addItem(QListWidgetItem(zone_name))

    def item_activated_event(self, item):
        self.zone_parameters.set_name_zone(item.text())
        self.zone_parameters.widget_for_stage_values.selected_zone = self.zones[item.text()]
        self.zone_parameters.widget_for_stage_values.set_stage_values()
        self.zone_parameters.update_visual_data_of_zones()
        self.zone_parameters.update_visual_connection_value()
        print(item.text())

    def eventFilter(self, obj, event):
        if obj is self.listWidget and event.type() == QEvent.ContextMenu:
            item = self.listWidget.currentItem()
            if item:
                name = item.text()
                del self.zones[name]
                self.update_list_widget()
                print(f'element {name} del')
                if name == self.zone_parameters.widget_for_stage_values.selected_zone.name:
                    self.zone_parameters.set_name_zone("")

                for zone_name, zone_data in self.zones.items():
                    if name in zone_data.connections:
                        del zone_data.connections[name]

                self.zone_parameters.update_visual_data_of_zones()
        return super().eventFilter(obj, event)

    def add_item(self):
        name = f"{self.input_name.text()}"
        if name not in self.zones and len(name) > 0:
            self.zones[name] = CZoneParameters(name=name)
            self.listWidget.addItem(QListWidgetItem(name))
            self.input_name.clear()
        else:
            self.input_name.clear()
