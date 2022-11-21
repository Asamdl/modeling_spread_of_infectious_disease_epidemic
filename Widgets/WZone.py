from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout, QVBoxLayout, QPushButton
from Widgets.WPainter import WPainter
import uuid


class Zone(QWidget):
    def __init__(self, name):
        super().__init__()
        self.lay = QVBoxLayout(self)
        lay_ = QHBoxLayout()
        self.name = name
        self.id = str(uuid.uuid4())
        self.label_name = QLabel(str(self.name))
        lay_.addWidget(self.label_name)
        self.btn_del = QPushButton("del")
        lay_.addWidget(self.btn_del)
        self.lay.addLayout(lay_)
        self.lay.addWidget(WPainter())

    def set_name(self, name):
        self.name = name
        self.label_name.setText(str(name))
