import typing
from functools import partial

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit

from classes.ZoneParameters import CZoneParameters


class WSetModelParameters(QWidget):
    def __init__(self, checkbox_states: typing.Dict[str, bool], parent=None):
        QWidget.__init__(self, parent=parent)
        layout = QVBoxLayout(self)
        self.edit_lines = dict()
        self.checkbox_states = checkbox_states
        self.selected_zone = CZoneParameters("ya")
        for name, value in self.checkbox_states.items():
            if value:
                lay = QHBoxLayout()
                label = QLabel(name)
                size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
                lay.addWidget(label)
                line_edit = QLineEdit()
                line_edit.setSizePolicy(size_policy)
                line_edit.setFixedWidth(70)
                lay.addWidget(line_edit)
                layout.addLayout(lay)
                line_edit.textChanged.connect(
                    partial(self.update_value_in_zone_object, line_name_and_edit=(label.text(), line_edit)))
                self.edit_lines[name] = line_edit

    def disable_all_elements(self):
        for edit_line in self.edit_lines.values():
            edit_line.setEnabled(False)
            edit_line.setText("0")

    def enable_all_elements(self):
        for edit_line in self.edit_lines.values():
            edit_line.setEnabled(True)

    def update_value_in_zone_object(self, line_name_and_edit):
        value = str(line_name_and_edit[1].text())
        if len(value) > 0:
            if value.isdigit():
                self.selected_zone.stages_value[line_name_and_edit[0]] = int(value)

    def set_stage_values(self):
        for stage_name, edit_line in self.edit_lines.items():
            edit_line.setText(str(self.selected_zone.stages_value[stage_name]))

