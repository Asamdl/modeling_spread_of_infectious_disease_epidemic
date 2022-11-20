from PyQt5 import QtGui, QtCore
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


class WidgetPlt(QWidget):
    def __init__(self):
        super().__init__()
        self.show()
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        # I've been looking for you for too long to just leave you here unmarked
        self.toolbar = NavigationToolbar(self.canvas, self,
                                         coordinates=False)
        self.button = QPushButton('Plot')
        self.button.clicked.connect(self.plot)
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def plot(self):
        data = [random.random() for i in range(10)]
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(data, '*-')
        self.canvas.draw()


class box(QWidget):
    def __init__(self, top=None, left=None, width=None, height=None):
        super().__init__()
        self.InitWindow()

    def InitWindow(self):
        self.show()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_:
            self.close()

    def mousePressEvent(self, e):
        if e.buttons() == Qt.RightButton:
            # s = e.pos()
            print(e.x(), e.y())

    def paintEvent(self, event=None, changing_number=None):
        print(event)
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.green, Qt.CrossPattern))
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
                buttons_lay = QHBoxLayout()
                button_zone_increment = QPushButton("+")
                buttons_lay.addWidget(button_zone_increment)
                buttons_lay.addWidget(QPushButton("-"))
                lay00 = QVBoxLayout()
                lay00.addLayout(buttons_lay)
                lay_ = QGridLayout()
                for x in range(2):
                    for y in range(2):
                        widget = box()
                        lay_.addWidget(widget, x, y)
                lay00.addLayout(lay_)
                slider = QSlider(Qt.Horizontal)
                lay00.addWidget(slider)
                grid.addLayout(lay00, *position)
            elif position[0] == 0 and position[1] == 2:
                plotlib = WidgetPlt()
                lay_ = QVBoxLayout()
                lay_.addWidget(plotlib)
                grid.addLayout(lay_, *position)
            elif position[0] == 1 and position[1] == 0:
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


class Widget1(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        lay = QVBoxLayout(self)
        for i in range(4):
            lay.addWidget(QPushButton("{}".format(i)))


class WidgetCreatingModel(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        self.stages_names = ["S", "I", "E", "R", "D", "`S"]
        self.name_of_inactive_stages = ["S", "I"]
        self.checkbox_states = dict()
        self.stages_widgets = dict()
        lay = QVBoxLayout(self)
        label_widget = QLabel("Сreating a model")
        lay.addWidget(label_widget)
        lay_stages = QGridLayout()
        positions = [
            (0, 0), (0, 1),
            (1, 0), (1, 1),
            (2, 0), (2, 1)
        ]
        for stage_name,position in zip(self.stages_names,positions):
            widget_check_box = QCheckBox(stage_name, self)
            widget_check_box.stateChanged.connect(self.update_info_about_status_of_checkboxes)
            lay_stages.addWidget(widget_check_box,*position)
            if stage_name in self.name_of_inactive_stages:
                widget_check_box.setEnabled(False)
                widget_check_box.toggle()
                self.checkbox_states[stage_name] = True
            else:
                self.checkbox_states[stage_name] = False
            self.stages_widgets[stage_name] = widget_check_box
        lay.addLayout(lay_stages)
        self.btn = QPushButton("apply")
        self.btn.clicked.connect(self.show_info_about_status_of_checkboxes)
        lay.setAlignment(Qt.AlignCenter)
        lay.addWidget(self.btn)

    def update_info_about_status_of_checkboxes(self, state):
        for stage_name, stage_widget in self.stages_widgets.items():
            self.checkbox_states[stage_name] = True if stage_widget.checkState() == Qt.Checked else False

    def show_info_about_status_of_checkboxes(self):
        for name, state in self.checkbox_states.items():
            print(f"{name} = {state}")
        print()


def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
