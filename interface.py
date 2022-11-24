import typing

from PyQt5 import QtGui, QtCore, QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, \
    QLineEdit, QRadioButton, QStackedWidget, QGridLayout, QProgressBar, QSlider, QCheckBox, QFrame
import sys
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor
from PyQt5.QtCore import Qt, QObject, QEvent
from PyQt5.uic import loadUi
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import random
import matplotlib.pyplot as plt

from Widgets.WPltBig import WPltBig
from Widgets.WZoneConstructor import WZoneConstructor


class box(QWidget):
    def __init__(self, name: str, top=None, left=None, width=None, height=None):
        super().__init__()
        self.name = name
        self.colors = [Qt.red, Qt.black, Qt.white, Qt.yellow]
        self.InitWindow()

    def InitWindow(self):
        self.show()

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
        self.width = 1000
        self.height = 650
        grid = QGridLayout()
        self.setLayout(grid)
        positions = [
            (0, 0, 1, 2),
            (0, 2, 1, 1),
            (1, 0, 1, 1),
            (1, 1, 1, 1),
            (1, 2, 1, 1)
        ]
        # row: int, column: int, rowSpan: int, columnSpan: int
        for position in positions:
            if position[0] == 0 and position[1] == 0:
                lay00 = QVBoxLayout()
                lay_ = QGridLayout()
                label = QLabel("Создание зон")
                label.setAlignment(QtCore.Qt.AlignCenter)
                lay_.addWidget(label, 0, 0)
                lay_.addWidget(WZoneConstructor(), 1, 0, 100, 1)

                lay00.addLayout(lay_)
                slider = QSlider(Qt.Horizontal)
                slider.valueChanged.connect(self.update_color_for_zones)
                lay00.addWidget(slider)
                grid.addLayout(lay00, *position)
            elif position[0] == 0 and position[1] == 2:
                plotlib = WPltBig()
                lay_ = QVBoxLayout()
                lay_.addWidget(plotlib)
                # grid.addLayout(lay_, 0,2)
                grid.addLayout(lay_, 0, 2, 1, 75)
            elif position[0] == 1 and position[1] == 1:
                lay_ = QVBoxLayout()
                lay_.addWidget(WidgetCreatingModel())
                grid.addLayout(lay_, *position)
            else:
                # label = QLabel(name)
                widget = Widget1()
                # label.setStyleSheet('QLabel {background-color: #A3C1DA; color: red;}')
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


class WidgetSetModelParameters(QWidget):
    def __init__(self, checkbox_states: typing.Dict[str, bool], parent=None):
        QWidget.__init__(self, parent=parent)
        layout = QGridLayout(self)
        positions = []
        for i in range(len(checkbox_states)):
            positions.append([i if i % 2 == 0 else i - 1, 0 if i % 2 == 0 else 2])
            positions.append([i if i % 2 == 0 else i - 1, 1 if i % 2 == 0 else 3])
        num_ = 0
        for name, value in checkbox_states.items():
            if value:
                label = QLabel(name)
                label.setAlignment(QtCore.Qt.AlignCenter)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
                layout.addWidget(label, *positions[num_])
                line_edit = QLineEdit()
                # label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
                line_edit.setSizePolicy(sizePolicy)
                line_edit.setFixedWidth(50)
                layout.addWidget(line_edit,  *positions[num_+1])

                num_+=2
                # lay.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        # for name, value in checkbox_states.items():
        #     if value:
        #         # I'm so tired of doing this
        #         # Unfinished
        #         lay = QHBoxLayout()
        #         label = QLabel(name)
        #         # label.setAlignment(QtCore.Qt.AlignLeft)
        #         sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        #
        #         lay.addWidget(label)
        #         line_edit = QLineEdit()
        #         label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        #         line_edit.setSizePolicy(sizePolicy)
        #         # line_edit.setAlignment(QtCore.Qt.AlignLeft)
        #         # line_edit.resize(70, 20)
        #         # line_edit.setMaximumSize(QtCore.QSize(16777215, 25))
        #         line_edit.setFixedWidth(50)
        #         # line_edit.setMaxLength(5)
        #         # line_edit.setDisabled(True)
        #         lay.addWidget(line_edit)
        #        # lay.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        #         layout.addLayout(lay)


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

        layout_child_1_2 = QVBoxLayout()
        label_set_value = QLabel("Устанвка значений")
        label_set_value.setAlignment(QtCore.Qt.AlignCenter)
        layout_child_1_2.addWidget(label_set_value)
        self.widget_m = WidgetSetModelParameters(self.checkbox_states)
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
        # self.lay_m.deleteLater()
        self.lay_m.removeWidget(self.widget_m)
        # self.widget_m.deleteLater()
        self.widget_m = WidgetSetModelParameters(self.checkbox_states)
        self.lay_m.addWidget(self.widget_m, 0, 0)


def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
