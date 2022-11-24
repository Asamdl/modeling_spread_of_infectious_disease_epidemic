from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, \
    QLineEdit, QRadioButton, QStackedWidget, QGridLayout, QProgressBar, QSlider, QCheckBox, QFrame


class WAddZone(QWidget):
    def __init__(self):
        super().__init__()
        lay_ = QVBoxLayout(self)
        #lay_.addWidget(QLabel("Заглушка"))
        self.btn = QPushButton("Add zone")
        lay_.addWidget(self.btn)