from functools import partial

from PyQt5.QtWidgets import QWidget, QGridLayout

from Widgets.WAddZone import WAddZone
from Widgets.WZone import WZone


class WZoneConstructor(QWidget):
    def __init__(self):
        super().__init__()
        self.number_of_zones = 4
        self.grid_options = (2, 3)
        self.positions = [(i, j) for i in range(self.grid_options[0]) for j in range(self.grid_options[1])]
        self.maximum_number_of_zones = len(self.positions)
        self.zones = dict()
        self.grid = QGridLayout(self)
        self.add_widget = self.create_add_widget()
        self.add_widget_is_deleted = True
        self.create_zones()
        self.set_del_func_for_zone()
        self.show_zones()

    def create_zones(self):
        for i in range(self.number_of_zones):
            zone = WZone(name=i)
            self.zones[zone.id] = zone

    def update_name_zones(self):
        for i in range(self.number_of_zones):
            self.zones[i].set_name(i)

    def set_del_func_for_zone(self):
        for zone in self.zones.values():
            self.add_zone_delete_function(zone)

    def show_zones(self):
        if self.number_of_zones > 0:
            if self.number_of_zones < self.maximum_number_of_zones:
                for zone, position in zip(self.zones.values(), self.positions[:self.number_of_zones]):
                    self.grid.addWidget(zone, *position)
                self.grid.addWidget(self.add_widget, *self.positions[self.number_of_zones:self.number_of_zones + 1][0])
            elif self.number_of_zones == self.maximum_number_of_zones:
                for zone, position in zip(self.zones.values(), self.positions[:self.number_of_zones]):
                    self.grid.addWidget(zone, *position)
            else:
                print(f"{self.number_of_zones=} > {self.maximum_number_of_zones=}")
        else:
            self.grid.addWidget(self.add_widget, *self.positions[0])

    def add_zone_delete_function(self, zone: WZone):
        zone.btn_del.clicked.connect(partial(self.action_del_zone, id_element=zone.id))

    def create_add_widget(self):
        add_widget = WAddZone()
        add_widget.btn.clicked.connect(self.action_add_zone)
        return add_widget

    def clear_grid(self):
        for zone in self.zones.values():
            self.grid.removeWidget(zone)
        if self.add_widget_is_deleted:
            self.grid.removeWidget(self.add_widget)
        elif self.number_of_zones < self.maximum_number_of_zones:
            self.add_widget = self.create_add_widget()
            self.add_widget_is_deleted = True
            self.grid.addWidget(self.add_widget, *self.positions[self.number_of_zones])

    def action_add_zone(self):
        if self.number_of_zones < self.maximum_number_of_zones:
            self.add_zone()
            self.clear_grid()
            self.show_zones()
        if self.number_of_zones == self.maximum_number_of_zones:
            self.add_widget.deleteLater()
            self.add_widget_is_deleted = False

    def add_zone(self):
        zone = WZone(self.number_of_zones)
        self.add_zone_delete_function(zone)
        self.zones[zone.id] = zone
        self.number_of_zones += 1

    def action_del_zone(self, id_element):
        if self.number_of_zones > 0:
            self.del_zone(id_element)
            self.clear_grid()
            self.show_zones()

    def del_zone(self, id_element):
        try:
            self.number_of_zones -= 1
            self.grid.removeWidget(self.zones[id_element])
            self.zones[id_element].deleteLater()
            del self.zones[id_element]
            for zone, i in zip(self.zones.values(), range(self.number_of_zones)):
                zone.set_name(i)
        except IndexError:
            print(IndexError)
