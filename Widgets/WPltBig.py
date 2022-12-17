import random

import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class WPltBig(QWidget):
    def __init__(self, result_model):
        super().__init__()
        self.show()
        self.result_model = result_model
        self.figure = plt.figure()

        self.canvas = FigureCanvas(self.figure)
        # I've been looking for you for too long to just leave you here unmarked
        self.toolbar = NavigationToolbar(self.canvas, self,
                                         coordinates=False)
        self.button = QPushButton('Plot')

        self.button.clicked.connect(self.show_result)

        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def show_result(self):
        try:
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            self.list_result_show = [[0, len(self.result_model)]]
            colors = []
            for i in range(max([r[1] for r in self.list_result_show]) - 1):
                colors.append(None)
            plots = []
            for r_i in range(len(self.list_result_show)):
                if r_i == 0:
                    linestyle = "-"
                elif r_i == 1:
                    linestyle = "--"
                elif r_i == 2:
                    linestyle = "-."
                else:
                    linestyle = ":"
                i = 0
                for name in self.result_model:
                    if name != "step":
                        label = name
                        # label = "..." + self.list_result[self.list_result_show[r_i][0]].file_result[
                        #                -self.deep_settings.num_char_label:-4] + " -> " + name
                        # plots += plt.plot(self.result_model["step"],self.result_model[name],label=label, color=colors[i], linestyle=linestyle)
                        ax.plot(self.result_model["step"],
                                self.result_model[name],
                                label=label, color=colors[i], linestyle=linestyle)
                        # colors[i] = plots[-1].get_color()
                        i += 1

            plt.legend()
            plt.grid()

            self.canvas.draw()

        except Exception as e:
            raise SystemExit(1)

    def plot(self):
        data = [random.random() for i in range(10)]
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(data)
        self.canvas.draw()
