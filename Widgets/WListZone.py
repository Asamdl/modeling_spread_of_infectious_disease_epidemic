from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QListWidget, QListWidgetItem
from PyQt5.QtCore import QEvent

from PyQt5 import QtWidgets


class WListZone(QWidget):

    def __init__(self):
        super().__init__()
        self.number_of_zones = 0
        self.zones_names = dict()
        self.window_layout = QVBoxLayout(self)
        layout_add_zone = QHBoxLayout()
        self.input_name = QLineEdit()
        self.input_name.setPlaceholderText('Название зоны')
        self.btn = QtWidgets.QPushButton("Доавить")
        self.btn.clicked.connect(self.add_item)
        layout_add_zone.addWidget(self.input_name)
        layout_add_zone.addWidget(self.btn)
        self.window_layout.addLayout(layout_add_zone)
        self.listWidget = QListWidget()
        # self.listWidget.addItem(QListWidgetItem("Solo"))
        self.listWidget.installEventFilter(self)
        # self.listWidget.itemSelectionChanged.connect(self.selectionChanged)
        self.listWidget.itemActivated.connect(self.itemActivated_event)

        # listWidgetItem = QListWidgetItem("GeeksForGeeks")
        # self.listWidget.addItem(listWidgetItem)

        self.window_layout.addWidget(self.listWidget)

    def selectionChanged(self):
        el = self.listWidget.selectedItems()
        print("Selected items: ", self.listWidget.selectedItems())

    def update_list_widget(self):
        self.listWidget.clear()
        for zone_name in self.zones_names.keys():
            self.listWidget.addItem(QListWidgetItem(zone_name))

    def itemActivated_event(self, item):
        print(item.text())

    def eventFilter(self, obj, event):
        if obj is self.listWidget and event.type() == QEvent.ContextMenu:
            item = self.listWidget.currentItem()
            if item:
                name = item.text()
                del self.zones_names[name]
                self.update_list_widget()
                print(f'element {name} del')
        return super().eventFilter(obj, event)

    def add_item(self):
        name = f"{self.input_name.text()}"
        if name not in self.zones_names and len(name) > 0:
            self.zones_names[name] = "zod"
            self.listWidget.addItem(QListWidgetItem(name))
        else:
            self.input_name.clear()
