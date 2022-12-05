from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton


class WAddZone(QWidget):
    def __init__(self):
        super().__init__()
        lay_ = QVBoxLayout(self)
        #lay_.addWidget(QLabel("Заглушка"))
        self.btn = QPushButton("Add zone")
        lay_.addWidget(self.btn)