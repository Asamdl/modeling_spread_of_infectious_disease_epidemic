import typing

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit


class WSetModelParameters(QWidget):
    def __init__(self, checkbox_states: typing.Dict[str, bool], parent=None):
        QWidget.__init__(self, parent=parent)
        layout = QVBoxLayout(self)
        for name, value in checkbox_states.items():
            if value:
                lay = QHBoxLayout()
                label = QLabel(name)
                sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
                lay.addWidget(label)
                line_edit = QLineEdit()
                line_edit.setSizePolicy(sizePolicy)
                line_edit.setFixedWidth(70)
                lay.addWidget(line_edit)
                layout.addLayout(lay)