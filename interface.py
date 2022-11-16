from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, \
    QLineEdit, QRadioButton, QStackedWidget, QGridLayout
import sys
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor
from PyQt5.QtCore import Qt, QObject, QEvent
from PyQt5.uic import loadUi


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


class box(QWidget):
    def __init__(self, top=None, left=None, width=None, height=None):
        super().__init__()
        self.title = "PyQt5 Drawing Tutorial"
        # self.top = 150
        # self.left = 150
        # self.width = 500
        # self.height = 500

        self.InitWindow()

    def InitWindow(self):
        self.setWindowTitle(self.title)
        # self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_:
            self.close()

    def mousePressEvent(self, e):
        if e.buttons() == Qt.RightButton:
            # s = e.pos()
            print(e.x(), e.y())

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.green, 8, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.red, Qt.CrossPattern))
        w = self.geometry().width()
        h = self.geometry().height()
        painter.drawRect((int)(w * 10 / 100), (int)(h * 10 / 100), (int)(w * 80 / 100), (int)(h * 80 / 100))


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "PyQt5"
        self.top = 150
        self.left = 150
        self.width = 500
        self.height = 500

        grid = QGridLayout()
        self.setLayout(grid)

        names = ['Cls', 'Bck',
                 'Cls', 'Bck']

        positions = [(i, j) for i in range(2) for j in range(2)]
        for position, name in zip(positions, names):
            if position[0] == 0 and position[1] == 0:
                widget = WidgetZone()
                #widget = box()
                grid.addWidget(widget, *position)
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

number_of_zones = 1
class WidgetZone(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent=parent)
        lay = QVBoxLayout(self)
        buttons_lay = QHBoxLayout()
        buttons_lay.addWidget(QPushButton("+"))
        buttons_lay.addWidget(QPushButton("-"))
        lay.addLayout(buttons_lay)
        qwidgetzone = box()
        #label = QLabel("Body")
        #label.setStyleSheet('QLabel {background-color: #A3C1DA; color: red;}')
        lay.addWidget(qwidgetzone)


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
