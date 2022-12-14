import random
import sys

from PyQt5 import QtCore, uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QPushButton, \
    QGridLayout, QSlider, QHBoxLayout, QCheckBox, QFrame, QInputDialog
from matplotlib import pyplot as plt

from Widgets.WCreatingModel import WCreatingModel
from Widgets.WListZone import WListZone
from Widgets.WPltBig import WPltBig
from classes.ZoneParameters import CZoneParameters
from classes.classes import Model, Stage, Flow, DictStage
from functions_for_model_file import create_json_file, convert_model_to_json, load_file_model

names_of_the_coefficients_of_the_connections = {("S", "E"): ("α", 0),
                                                ("E", "I"): ("β", 0),
                                                ("I", "D"): ("γ", 0),
                                                ("I", "R"): ("δ", 0),
                                                ("R", "`S"): ("ε", 0),
                                                ("S", "I"): ("β", 1),
                                                ("I", "`S"): ("ε", 1)}
names_of_the_coefficients_of_the_connections_reverse = dict()
for n1, n2 in names_of_the_coefficients_of_the_connections.items():
    names_of_the_coefficients_of_the_connections_reverse[n2] = n1


class box(QWidget):
    def __init__(self, name: str, top=None, left=None, width=None, height=None):
        super().__init__()
        self.name = name
        self.colors = [Qt.red, Qt.black, Qt.white, Qt.yellow]

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
        self.width = 1200
        self.height = 650
        self.zones = dict()
        self.result_model = dict()
        self.stage_coefficients = dict()
        self.stages_value = dict()
        grid = QGridLayout()
        self.setLayout(grid)
        positions = [
            (0, 0, 1, 1),
            (0, 1, 1, 1),
            (1, 0, 1, 1),
            (1, 1, 1, 1)
        ]
        for position in positions:
            if position[0] == 0 and position[1] == 0:
                lay00 = QVBoxLayout()
                lay00.addStretch()
                lay_ = QGridLayout()
                label = QLabel("Создание зон")
                label.setAlignment(QtCore.Qt.AlignCenter)
                lay00.addWidget(label)
                lay00.addWidget(WListZone(self.zones))

                lay00.addStretch()
                #slider = QSlider(Qt.Horizontal)
                #slider.valueChanged.connect(self.update_color_for_zones)
                lay00.setAlignment(Qt.AlignmentFlag.AlignTop)
                #lay00.addWidget(slider)

                grid.setAlignment(Qt.AlignmentFlag.AlignTop)
                grid.addLayout(lay00, *position)
            elif position[0] == 0 and position[1] == 1:
                plot_lib = WPltBig(self.result_model)
                lay_ = QVBoxLayout()
                lay_.addWidget(plot_lib)
                grid.addLayout(lay_, *position)
            elif position[0] == 1 and position[1] == 0:
                lay_ = QVBoxLayout()
                lay_.addWidget(WidgetCreatingModel(zones=self.zones, stage_coefficients=self.stage_coefficients))
                grid.addLayout(lay_, *position)
            else:
                s_widget = Widget1(stage_coefficients=self.stage_coefficients, zones=self.zones,result_model = self.result_model)
                grid.addWidget(s_widget, *position)
        self.InitWindow()

    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)

    def update_color_for_zones(self):
        pass


class Widget1(QWidget):
    def __init__(self, stage_coefficients, zones: dict,result_model, parent=None):
        QWidget.__init__(self, parent=parent)
        self.stage_coefficients = stage_coefficients
        self.zones = zones
        self.zone_ = None
        self.model_run = True
        self.result_model = result_model
        self.result_flows = {}
        self.divided_n = True
        self.one_way_flows = []
        lay = QVBoxLayout(self)
        btn_start = QPushButton("Start")
        btn_start.clicked.connect(self.start_model)
        lay.addWidget(btn_start)

    def get_flows_list(self):
        flows = []
        for stage_name, stage_coefficient in self.stage_coefficients.items():
            current_stages = names_of_the_coefficients_of_the_connections_reverse[stage_name]
            flow = Flow(source=current_stages[0],
                        s_factor=stage_coefficient,
                        d_factor="",
                        dynamic=False,
                        dic_target=[DictStage(stage_name=current_stages[1], value="1")],
                        induction=True if "S" in current_stages[0] else False,
                        dic_ind=[DictStage(stage_name="I", value="1")] if "S" in current_stages[0] else None)
            flows.append(flow)
        return flows

    def get_stage_list(self):
        stages_of_zones = []
        number_of_stages = len(self.stage_coefficients) + 1
        num_zone = 0
        for zone in self.zones.values():
            stages = []
            for stage_name, stage_value in zone.stages_value.items():
                # stages.append(Stage(f"{stage_name}{num_zone + 1}", str(stage_value)))
                stages.append(Stage(f"{stage_name}", str(stage_value)))
            stages_of_zones.append(stages)
            num_zone += 1
        result_list_stages = []
        for num_stage in range(number_of_stages):
            for num_zone in range(len(self.zones)):
                result_list_stages.append(stages_of_zones[num_zone][num_stage])
        return result_list_stages

    def create_model(self):
        load_file_model("post.json")
        is_values_of_the_stages_are_suitable = True
        is_zone_values_are_suitable = True
        for stage_coefficient_value in self.stage_coefficients.keys():
            if stage_coefficient_value == 0:
                is_values_of_the_stages_are_suitable = False

        if len(self.zones) <= 0:
            is_zone_values_are_suitable = False

        if is_values_of_the_stages_are_suitable and is_zone_values_are_suitable:
            model = Model(model_name="RDDS",
                          stages=self.get_stage_list(),
                          flows=self.get_flows_list())
            data = convert_model_to_json(model=model)
            #create_json_file(data, "post")
            #load_file_model("post.json")
        print(2)

    def model_step(self):
        """
        Change model state after one step
        :return: None
        """

        new_state = dict(self.zone_.stages_value)
        self.population_size = sum(float(self.zone_.stages_value[st]) for st in self.zone_.stages_value)
        flows = self.get_flows_list()
        for fl in flows:
            change, fl_value = fl.get_change(self.zone_.stages_value, self.population_size, self.step, self.divided_n)
            self.result_flows[str(fl)].append(fl_value)
            for st in change:
                new_state[st] += change[st]
        for o_w_fl in self.one_way_flows:
            change = o_w_fl.get_change(self.model_state, self.population_size, self.step)
            if change == "to_zero":
                new_state[o_w_fl.stage] = 0
            else:
                new_state[o_w_fl.stage] += change
        # self.model_state = new_state
        return new_state


    def start_model(self):
        """
        Starts simulation before the stop rule occurs
        :param output_file: file to write result of modeling
        :return:
        """
        # запись заголовков в словарь
        self.result_model["step"] = []
        self.result_flows["step"] = []
        self.zone_ = self.zones["1"]
        for st in self.zone_.stages_value:
            self.result_model[st] = []

        for fl in self.get_flows_list():
            self.result_flows[str(fl)] = []

        self.step = 0
        while self.model_run:
            new_state = self.model_step()
            if new_state["S"]<0 or self.step == 1000:
                self.model_run = False

            # заполнение словаря
            self.result_model["step"].append(self.step)
            self.result_flows["step"].append(self.step)
            for st in self.zone_.stages_value:
                self.result_model[st].append(self.zone_.stages_value[st])

            self.zone_.stages_value = new_state
            self.step += 1
        print("Norm")


class WidgetCreatingModel(QWidget):
    def __init__(self, zones, stage_coefficients, parent=None):
        QWidget.__init__(self, parent=parent)
        self.zones = zones
        self.stage_coefficients = stage_coefficients
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
        self.update_stage_coefficients()
        layout_child_1_1.addLayout(layout_child_1_1_grid)
        btn = QPushButton("apply")
        btn.clicked.connect(self.show_info_about_status_of_checkboxes)
        layout_child_1_1.setAlignment(Qt.AlignCenter)
        layout_child_1_1.addWidget(btn)
        layout_child_1.addLayout(layout_child_1_1)
        # layout_child_1_2 = uic.loadUi('SEIRD`S.ui')
        layout_child_1_2 = uic.loadUi('SEIRD`S - Copy.ui')
        self.layout_child_1_2_frames = layout_child_1_2.findChildren(QFrame)
        self.layout_child_1_2_buttons = layout_child_1_2.findChildren(QPushButton)

        for button in self.layout_child_1_2_buttons:
            button.clicked.connect(lambda state, x=button.text(): self.ModelParametersDialog(x))

        self.WidgetSetModelParameters(self.checkbox_states, self.layout_child_1_2_frames)
        layout_child_1.addWidget(layout_child_1_2)
        layout_parent.addLayout(layout_child_1)

    def update_stage_coefficients(self):
        names_of_active_coefficients = []
        names_of_active_stages = []
        self.name_of_inactive_stages = []
        for stage_name, stage_value in self.checkbox_states.items():
            if stage_value:
                names_of_active_stages.append(stage_name)
                if stage_name not in self.name_of_inactive_stages:
                    for zone in self.zones.values():
                        zone.stages_value[stage_name] = 0
                    self.name_of_inactive_stages.append(stage_name)
            else:
                if stage_name in self.name_of_inactive_stages:
                    for zone in self.zones.values():
                        del zone.stages_value[stage_name]
                    self.name_of_inactive_stages.remove(stage_name)

        for stages_name, name_coefficient in names_of_the_coefficients_of_the_connections.items():
            if stages_name[0] in names_of_active_stages and \
                    stages_name[1] in names_of_active_stages and name_coefficient:
                post = True
                for n in names_of_active_coefficients:
                    if n[0] == name_coefficient[0]:
                        if name_coefficient[1] == 0:
                            n[1] = 0
                        post = False
                if post:
                    names_of_active_coefficients.append(name_coefficient)
        free_coefficients = []
        for name_coefficient in self.stage_coefficients.keys():
            if name_coefficient not in names_of_active_coefficients:
                free_coefficients.append(name_coefficient)
        for name_coefficient in free_coefficients:
            del self.stage_coefficients[name_coefficient]
        for name_coefficient in names_of_active_coefficients:
            if name_coefficient not in self.stage_coefficients:
                self.stage_coefficients[name_coefficient] = 0.0
        print(names_of_active_coefficients)

    def ModelParametersDialog(self, button_text):
        inputted_value, done = QInputDialog.getDouble(self, f'{button_text}', 'Введите параметр:')
        if done:
            post = False
            num = 0
            for name_coefficient in self.stage_coefficients.keys():
                if name_coefficient[0] == button_text:
                    post = True
                    num = name_coefficient[1]
                    break
            if post:
                self.stage_coefficients[(button_text, num)] = inputted_value
                print(self.stage_coefficients[(button_text, num)])

    def WidgetSetModelParameters(self, checkbox_states, layout_frames):
        layout_frames_names = []
        for frame in layout_frames:
            layout_frames_names.append(frame.objectName())

        # ugly? maybe. works? yes.
        if checkbox_states['E']:
            layout_frames[layout_frames_names.index("beta_frame")].show()
            layout_frames[layout_frames_names.index("E_frame")].show()
        else:
            layout_frames[layout_frames_names.index("beta_frame")].hide()
            layout_frames[layout_frames_names.index("E_frame")].hide()
        if checkbox_states['R']:
            layout_frames[layout_frames_names.index("xi_frame")].show()
            layout_frames[layout_frames_names.index("R_frame")].show()
        else:
            layout_frames[layout_frames_names.index("xi_frame")].hide()
            layout_frames[layout_frames_names.index("R_frame")].hide()
        if checkbox_states['D']:
            layout_frames[layout_frames_names.index("ID_frame")].show()
            layout_frames[layout_frames_names.index("I_solo_frame")].hide()
        else:
            layout_frames[layout_frames_names.index("ID_frame")].hide()
            layout_frames[layout_frames_names.index("I_solo_frame")].show()
        if checkbox_states['`S']:
            layout_frames[layout_frames_names.index(
                "idk_frame")].show()  # я не ебу какие эти греческие буковы. надо поменять и в дизайнере и здесь
            layout_frames[layout_frames_names.index("newS_frame")].show()
        else:
            layout_frames[layout_frames_names.index("idk_frame")].hide()
            layout_frames[layout_frames_names.index("newS_frame")].hide()

    def update_info_about_status_of_checkboxes(self, state):
        for stage_name, stage_widget in self.stages_widgets.items():
            self.checkbox_states[stage_name] = True if stage_widget.checkState() == Qt.Checked else False

    def show_info_about_status_of_checkboxes(self):
        self.update_stage_coefficients()
        self.WidgetSetModelParameters(self.checkbox_states, self.layout_child_1_2_frames)


def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
