import uuid

from PyQt5.QtWidgets import QLabel, QWidget, QHBoxLayout, QVBoxLayout, QPushButton


class WZoneElement(QWidget):
    def __init__(self, name):
        super().__init__()
        self.lay = QVBoxLayout(self)
        lay_ = QHBoxLayout()
        self.name = str(name)
        self.id = str(uuid.uuid4())
        self.label_name = QLabel(self.name)
        lay_.addWidget(self.label_name)
        self.parameters = QPushButton("Параметры")
        lay_.addWidget(self.parameters)
        self.connections = QPushButton("Связи")
        lay_.addWidget(self.connections)
        self.lay.addLayout(lay_)

    def set_name(self, name):
        self.name = str(name)
        self.label_name.setText(self.name)
