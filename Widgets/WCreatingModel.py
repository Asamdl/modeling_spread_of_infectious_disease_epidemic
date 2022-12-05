from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QGridLayout, QCheckBox

from Widgets.WSetModelParameters import WSetModelParameters


class WCreatingModel(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self.stages_names = ["S", "I", "E", "R", "D", "`S"]
        self.name_of_inactive_stages = ["S", "I"]
        self.checkbox_states = dict()
        self.stages_widgets = dict()
        layout_parent = QVBoxLayout(self)
        label_widget = QLabel("Создание модели")
        label_widget.setAlignment(QtCore.Qt.AlignCenter)
        layout_parent.addWidget(label_widget)
        layout_child_1 = QHBoxLayout()

        layout_child_1_1 = QVBoxLayout()
        layout_child_1_1_grid = QGridLayout()
        layout_child_1_1.addWidget(QLabel("Выбор стадий"))
        positions = [
            (0, 0), (0, 1),
            (1, 0), (1, 1),
            (2, 0), (2, 1)
        ]
        for stage_name, position in zip(self.stages_names, positions):
            widget_check_box = QCheckBox(stage_name, self)
            widget_check_box.stateChanged.connect(self.update_info_about_status_of_checkboxes)
            layout_child_1_1_grid.addWidget(widget_check_box, *position)
            if stage_name in self.name_of_inactive_stages:
                widget_check_box.setEnabled(False)
                widget_check_box.toggle()
                self.checkbox_states[stage_name] = True
            else:
                self.checkbox_states[stage_name] = False
            self.stages_widgets[stage_name] = widget_check_box
        layout_child_1_1.addLayout(layout_child_1_1_grid)
        btn = QPushButton("apply")
        btn.clicked.connect(self.show_info_about_status_of_checkboxes)
        layout_child_1_1.setAlignment(Qt.AlignCenter)
        layout_child_1_1.addWidget(btn)
        layout_child_1.addLayout(layout_child_1_1)

        layout_child_1_2 = QVBoxLayout()
        layout_child_1_2.addWidget(QLabel("Устанвка значений"))
        self.widget_m = WSetModelParameters(self.checkbox_states)
        self.lay_m = QGridLayout()
        self.lay_m.addWidget(self.widget_m, 0, 0)
        layout_child_1_2.addLayout(self.lay_m)
        layout_child_1_2.addWidget(QPushButton("apply"))

        layout_child_1.addLayout(layout_child_1_2)
        layout_parent.addLayout(layout_child_1)

    def update_info_about_status_of_checkboxes(self, state):
        for stage_name, stage_widget in self.stages_widgets.items():
            self.checkbox_states[stage_name] = True if stage_widget.checkState() == Qt.Checked else False

    def show_info_about_status_of_checkboxes(self):
        for name, state in self.checkbox_states.items():
            print(f"{name} = {state}")
        print()
        self.lay_m.removeWidget(self.widget_m)
        self.widget_m = WSetModelParameters(self.checkbox_states)
        self.lay_m.addWidget(self.widget_m, 0, 0)