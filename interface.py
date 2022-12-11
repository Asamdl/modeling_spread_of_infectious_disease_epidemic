import random
import sys

from PyQt5 import QtCore, uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QPushButton, \
    QGridLayout, QSlider, QHBoxLayout, QCheckBox, QFrame

from Widgets.WCreatingModel import WCreatingModel
from Widgets.WListZone import WListZone
from Widgets.WPltBig import WPltBig


class box(QWidget):
    def __init__(self, name: str, top=None, left=None, width=None, height=None):
        super().__init__()
        self.name = name
        self.colors = [Qt.red, Qt.black, Qt.white, Qt.yellow]

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_:
            self.close()

    def mousePressEvent(self, e):
        if e.buttons() == Qt.LeftButton:
            # s = e.pos()
            print(self.name)
            print(e.x(), e.y())

    def paintEvent(self, event=None, changing_number=None):

        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        color = random.choice(self.colors)
        print(color)
        painter.setBrush(QBrush(color, Qt.CrossPattern))
        w = self.geometry().width()
        h = self.geometry().height()
        painter.drawRect(0, 0, w, h)


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "PyQt5"
        self.top = 50
        self.left = 50
        self.width = 1200
        self.height = 650
        grid = QGridLayout()
        self.setLayout(grid)
        positions = [
            (0, 0, 1, 1),
            (0, 1, 1, 1),
            (1, 0, 1, 1),
            (1, 1, 1, 1)
        ]
        for position in positions:
            if position[0] == 0 and position[1] == 0:
                lay00 = QVBoxLayout()
                lay00.addStretch()
                lay_ = QGridLayout()
                label = QLabel("Создание зон")
                label.setAlignment(QtCore.Qt.AlignCenter)
                lay00.addWidget(label)
                lay00.addWidget(WListZone())

                lay00.addStretch()
                slider = QSlider(Qt.Horizontal)
                slider.valueChanged.connect(self.update_color_for_zones)
                lay00.setAlignment(Qt.AlignmentFlag.AlignTop)
                lay00.addWidget(slider)

                grid.setAlignment(Qt.AlignmentFlag.AlignTop)
                grid.addLayout(lay00, *position)
            elif position[0] == 0 and position[1] == 1:
                plotlib = WPltBig()
                lay_ = QVBoxLayout()
                lay_.addWidget(plotlib)
                grid.addLayout(lay_, *position)
            elif position[0] == 1 and position[1] == 0:
                lay_ = QVBoxLayout()
                lay_.addWidget(WidgetCreatingModel())
                grid.addLayout(lay_, *position)
            else:
                widget = Widget1()
                grid.addWidget(widget, *position)
        self.InitWindow()

    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)

    def update_color_for_zones(self):
        pass


class Widget1(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        lay = QVBoxLayout(self)
        for i in range(4):
            lay.addWidget(QPushButton("{}".format(i)))


class widget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        uic.loadUi('test_element.ui', self)


class WidgetCreatingModel(QWidget):
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
        layout_child_1_2 = uic.loadUi('SEIRD`S.ui')
        self.layout_child_1_2_frames = layout_child_1_2.findChildren(QFrame)
        self.WidgetSetModelParameters(self.checkbox_states, self.layout_child_1_2_frames)
        layout_child_1.addWidget(layout_child_1_2)
        layout_parent.addLayout(layout_child_1)

    def WidgetSetModelParameters(self, checkbox_states, layout_frames):
        frames_of_interest = {
            "S": "S_frame",
            "I": "I_solo_frame",
            "E": "E_frame",
            "R": "R_frame",
            "D": "ID_frame",
            "`S": "newS_frame"}
        layout_frames_names = []
        for frame in layout_frames:
            layout_frames_names.append(frame.objectName())

        # ugly? maybe. works? yes.
        if checkbox_states['E']:
            layout_frames[layout_frames_names.index("beta_frame")].show()
            layout_frames[layout_frames_names.index("E_frame")].show()
        else:
            layout_frames[layout_frames_names.index("beta_frame")].hide()
            layout_frames[layout_frames_names.index("E_frame")].hide()
        if checkbox_states['R']:
            layout_frames[layout_frames_names.index("xi_frame")].show()
            layout_frames[layout_frames_names.index("R_frame")].show()
        else:
            layout_frames[layout_frames_names.index("xi_frame")].hide()
            layout_frames[layout_frames_names.index("R_frame")].hide()
        if checkbox_states['D']:
            layout_frames[layout_frames_names.index("ID_frame")].show()
            layout_frames[layout_frames_names.index("I_solo_frame")].hide()
        else:
            layout_frames[layout_frames_names.index("ID_frame")].hide()
            layout_frames[layout_frames_names.index("I_solo_frame")].show()
        if checkbox_states['`S']:
            layout_frames[layout_frames_names.index(
                "idk_frame")].show()  # я не ебу какие эти греческие буковы. надо поменять и в дизайнере и здесь
            layout_frames[layout_frames_names.index("newS_frame")].show()
        else:
            layout_frames[layout_frames_names.index("idk_frame")].hide()
            layout_frames[layout_frames_names.index("newS_frame")].hide()

    def update_info_about_status_of_checkboxes(self, state):
        for stage_name, stage_widget in self.stages_widgets.items():
            self.checkbox_states[stage_name] = True if stage_widget.checkState() == Qt.Checked else False

    def show_info_about_status_of_checkboxes(self):
        for name, state in self.checkbox_states.items():
            print(f"{name} = {state}")
        print()
        self.WidgetSetModelParameters(self.checkbox_states, self.layout_child_1_2_frames)


def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
