from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, \
    QLineEdit, QRadioButton, QStackedWidget, QGridLayout, QProgressBar, QSlider, QCheckBox, QFrame

from Widgets.WAddZone import WAddZone
from Widgets.WZone import Zone
from functools import partial


class WZoneConstructor(QWidget):
    def __init__(self):
        super().__init__()
        self.number_of_zones = 4
        self.grid_options = (2, 3)
        self.positions = [(i, j) for i in range(self.grid_options[0]) for j in range(self.grid_options[1])]
        self.maximum_number_of_zones = len(self.positions)
        self.zones = []
        self.grid = QGridLayout(self)
        self.add_widget = self.create_add_widget()
        self.create_zones()
        self.set_del_func_for_zone()
        self.show_zones()

    def create_zones(self):
        for i in range(self.number_of_zones):
            self.zones.append(Zone(name=i))

    def update_name_zones(self):
        for i in range(self.number_of_zones):
            self.zones[i].set_name(str(i))

    def set_del_func_for_zone(self):
        for i in range(self.number_of_zones):
            # на этом этапе индексы правильные но при нажатии на кнопку всегда индекс равен 3 ХМ
            self.zones[i].btn_del.clicked.connect(partial(self.action_del_zone, index=i))

    def show_zones(self):
        if self.number_of_zones > 0:
            if self.number_of_zones < self.maximum_number_of_zones:
                for zone, position in zip(self.zones, self.positions[:self.number_of_zones]):
                    self.grid.addWidget(zone, *position)
                self.grid.addWidget(self.add_widget, *self.positions[self.number_of_zones:self.number_of_zones + 1][0])
            elif self.number_of_zones == self.maximum_number_of_zones:
                for zone, position in zip(self.zones, self.positions[:self.number_of_zones]):
                    self.grid.addWidget(zone, *position)
            else:
                print(f"{self.number_of_zones=} > {self.maximum_number_of_zones=}")
        else:
            self.grid.addWidget(self.add_widget, *self.positions[0])

    def create_add_widget(self):
        add_widget = WAddZone()
        add_widget.btn.clicked.connect(self.action_add_zone)
        return add_widget

    def clear_grid(self):
        for zone in self.zones:
            self.grid.removeWidget(zone)
        self.grid.removeWidget(self.add_widget)

    def action_add_zone(self):
        if self.number_of_zones < self.maximum_number_of_zones:
            self.add_zone()
            self.clear_grid()
            self.show_zones()
        if self.number_of_zones == self.maximum_number_of_zones:
            self.add_widget.deleteLater()

    def add_zone(self):
        self.zones.append(Zone(name=len(self.zones)))
        self.number_of_zones += 1

    def action_del_zone(self, index):
        if self.number_of_zones > 0:
            self.del_zone(index)
            self.update_name_zones()
            self.set_del_func_for_zone()
            self.clear_grid()
            self.show_zones()

    def del_zone(self, index):
        try:
            self.number_of_zones -= 1
            self.grid.removeWidget(self.zones[index])
            self.zones[index].deleteLater()
            del self.zones[index]
            for i in range(self.number_of_zones):
                self.zones[i].set_name(i)
        except IndexError:
            print(IndexError)
