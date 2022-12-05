from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QComboBox, QDialogButtonBox, QLabel


class DZoneConnection(QDialog):
    def __init__(self, zones, parent=None):
        super(DZoneConnection, self).__init__(parent)

        layout_self = QVBoxLayout(self)
        layout_self.addWidget(QLabel("Создание связи"))
        self.connection_value = QLineEdit()
        self.zones_combo_box = QComboBox()
        self.zones = zones
        self.update_visual_data_of_zones()

        layout_self.addWidget(self.zones_combo_box)
        layout_self.addWidget(self.connection_value)

        # OK and Cancel buttons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout_self.addWidget(buttons)

    def update_visual_data_of_zones(self):
        self.zones_combo_box.clear()
        for zone_name in self.zones:
            self.zones_combo_box.addItem(zone_name)

    # static method to create the dialog and return (date, time, accepted)
    @staticmethod
    def get_connections_value(zones, parent=None):
        dialog = DZoneConnection(zones=zones,parent=parent)
        result = dialog.exec_()
        selected_zone = dialog.zones_combo_box.currentText()
        value = dialog.connection_value.text()

        return selected_zone, value, result == QDialog.Accepted
