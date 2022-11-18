from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, \
    QLineEdit, QRadioButton, QStackedWidget, QGridLayout, QProgressBar, QSlider
import sys
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor
from PyQt5.QtCore import Qt, QObject, QEvent
from PyQt5.uic import loadUi
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import random
import matplotlib.pyplot as plt

class Widget_Plt(QWidget):
    def __init__(self):
        super().__init__()
        self.show()
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self, coordinates=False)#I've been looking for you for too long to just leave you here unmarked
        self.button = QPushButton('Plot')
        self.button.clicked.connect(self.plot)
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)

        self.setLayout(layout)

    # action called by the push button
    def plot(self):
        data = [random.random() for i in range(10)]
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(data, '*-')
        self.canvas.draw()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        loadUi("interface.ui", self)
        self.title = "PyQt5 Drawing Tutorial"
        self.top = 150
        self.left = 150
        self.width = 500
        self.height = 500
        self.label2.setText("text")
        self.InitWindow()

    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()


class OverLay(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), QColor(80, 80, 255, 128))


class Filter(QObject):
    def __init__(self, *args, **kwargs):
        QObject.__init__(self, *args, **kwargs)
        self.m_overlay = None
        self.m_overlayOn = None

    def eventFilter(self, obj, event):
        if not obj.isWidgetType():
            return False
        if event.type() == QEvent.MouseButtonPress:
            if not self.m_overlay:
                self.m_overlay = OverLay(obj.parentWidget())
            self.m_overlay.setGeometry(obj.geometry())
            self.m_overlayOn = obj
            self.m_overlay.show()
        elif event.type() == QEvent.Resize:
            if self.m_overlay and self.m_overlayOn == obj:
                self.m_overlay.setGeometry(obj.geometry())
        return False


class LocationParameter():
    def __init__(self, x_axis, y_axis, margin_x_from_el, margin_y_from_el):
        self.x_axis = 0.1
        self.y_axis = 0.1
        self.margin_x_from_el = 0.1
        self.margin_y_from_el = 0.1


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
        painter.setPen(QPen(Qt.green, 8, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.red, Qt.CrossPattern))
        w = self.geometry().width()
        h = self.geometry().height()
        #params = self.get_parameters_for_rectangles()
        #for param in params:
        painter.drawRect(0, 0, w, h)

    def get_parameters_for_rectangles(self):
        w = self.geometry().width()
        h = self.geometry().height()
        result = []
        data = self.zone_location_parameters
        coef = 1 / self.number_of_zones
        for i in range(self.number_of_zones):
            if i != self.number_of_zones - 1:
                result.append(
                    [int(w * data.x_axis / 100), int(h * data.y_axis / 100), int(w * (100 - 2 * data.x_axis) / 100),
                     int(h * (100 - 2 * data.y_axis) / 100)])
            else:
                result.append(
                    [int(coef * w * data.x_axis),
                     int(coef)]
                )
        return result


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "PyQt5"
        self.top = 150
        self.left = 150
        self.width = 500
        self.height = 500



        grid = QGridLayout()
        #grid.setRowStretch(10,10)
        #grid.setColumnStretch(10,10)
        self.setLayout(grid)

        names = ['Cls', 'Bck',
                 'Cls', 'Bck']

        positions = [(i, j) for i in range(2) for j in range(2)]
        for position, name in zip(positions, names):
            if position[0] == 0 and position[1] == 0:
                buttons_lay = QHBoxLayout()
                button_zone_increment = QPushButton("+")
                #button_zone_increment.clicked.connect(self.add_zone)
                buttons_lay.addWidget(button_zone_increment)
                buttons_lay.addWidget(QPushButton("-"))
                lay00 = QVBoxLayout()
                lay00.addLayout(buttons_lay)
                #grid.addLayout(buttons_lay,*position)
                # widget = box()
                #grid.addWidget(widget, *position)
                lay_ = QGridLayout()
                for x in range(2):
                    for y in range(2):
                        widget = box()
                        lay_.addWidget(widget, x, y)
                lay00.addLayout(lay_)
                grid.addLayout(lay00, *position)
            elif position[0] == 0 and position[1] == 1:
                plotlib = Widget_Plt()
                lay_ = QVBoxLayout()
                lay_.addWidget(plotlib)
                grid.addLayout(lay_, *position)
            elif position[0] == 1 and position[1] == 1:
                plotlib = Widget_Plt()
                lay_ = QVBoxLayout()
                lay_.addWidget(plotlib)
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
        self.show()


def main():
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())


class WidgetZone(QWidget):
    def __init__(self, name=None,parent=None):
        QWidget.__init__(self, parent=parent)
        lay = QVBoxLayout(self)
        self.q_widget_zone = box()
        self.name = name
        lay.addWidget(self.q_widget_zone)

    def add_zone(self):
        self.q_widget_zone.paintEvent(f"{self.name}")


class Widget1(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        lay = QVBoxLayout(self)
        for i in range(4):
            lay.addWidget(QPushButton("{}".format(i)))


class Widget2(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        lay = QVBoxLayout(self)
        for i in range(4):
            lay.addWidget(QLineEdit("{}".format(i)))


class Widget3(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        lay = QVBoxLayout(self)
        for i in range(4):
            lay.addWidget(QRadioButton("{}".format(i)))


class stackedExample(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        lay = QVBoxLayout(self)
        self.Stack = QStackedWidget()
        self.Stack.addWidget(Widget1())
        self.Stack.addWidget(Widget2())
        self.Stack.addWidget(Widget3())

        btnNext = QPushButton("Next")
        btnNext.clicked.connect(self.onNext)
        btnPrevious = QPushButton("Previous")
        btnPrevious.clicked.connect(self.onPrevious)
        btnLayout = QHBoxLayout()
        btnLayout.addWidget(btnPrevious)
        btnLayout.addWidget(btnNext)

        lay.addWidget(self.Stack)
        lay.addLayout(btnLayout)

    def onNext(self):
        self.Stack.setCurrentIndex((self.Stack.currentIndex() + 1) % 3)

    def onPrevious(self):
        self.Stack.setCurrentIndex((self.Stack.currentIndex() - 1) % 3)


if __name__ == '__main__':
    # app = QApplication(sys.argv)
    # filt = Filter()
    # window = QWidget()
    # lay = QVBoxLayout(window)
    # for text in ("Foo", "Bar", "Baz"):
    #     label = QLabel(text)
    #     lay.addWidget(label)
    #     label.installEventFilter(filt)
    # window.setMinimumSize(500, 500)
    # window.show()
    # sys.exit(app.exec_())
    main()
