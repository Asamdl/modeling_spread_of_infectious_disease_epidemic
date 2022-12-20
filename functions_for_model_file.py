import json

from classes.classes import *


def load_file_model(filename):
    try:
        with open(filename, "r", encoding="utf-8-sig") as file:
            common_dic = json.load(file)
        list_stage = []
        list_dfactor = []
        list_flow = []
        list_owflow = []

        for st in common_dic["Stages"]:
            list_stage.append(Stage(**st))
        for df in common_dic["Dfactors"]:
            list_dfactor.append(DFactor(**df))
        for fl in common_dic["Flows"]:
            list_flow.append(Flow(**fl))
        for ow_fl in common_dic["Ow_flows"]:
            list_owflow.append(OWFlow(**ow_fl))
        print(2)

        check = True
        info = []
        element = ""
        title = "Model_check_title"
        stages = []
        flows = []
        ow_flows = []
        dfactors = []

        try:
            element = "Stage"
            if len(list_stage) < 1:
                info.append(["Num_stages", "", ""])
                check = False
            else:
                set_stage = set([st.name for st in list_stage])
                if len(set_stage) < len(list_stage):
                    info.append(["Identical_stage_name", "", ""])
                    check = False
                el_i = 1
                for st in list_stage:
                    dis_stage, check_add, info_add = st.get_stage(el_i)
                    if check_add:
                        stages.append(dis_stage)
                    else:
                        check = False
                        info += info_add
                    el_i += 1

                if all(st.num == 0 for st in stages):
                    info.append(["Zero_start_num", "", ""])
                    check = False
        except:
            pass

        # добавление и проверка потоков
        #     element = "Flow"
        #     el_i = 1
        #     if len(self.list_flow) < 1:
        #         info.append(["Num_flows", "", ""])
        #         check = False
        #     else:
        #         # сумма коэффициентов для каждой стадии как источника
        #         source_f_sum = {st.name: 0 for st in self.list_stage}
        #
        #         for fl in self.list_flow:
        #             flow, check_add, info_add = fl.get_flow(el_i)
        #             if check_add:
        #                 flows.append(flow)
        #
        #                 # добавляет к сумме коэффициентов стадий как источников
        #                 if not fl.dynamic:
        #                     source_f_sum[fl.source] += input_to_num(fl.sfactor)
        #
        #                 for tar in flow.target:
        #                     if not tar in [st.name for st in stages]:
        #                         info.append(["Not_exist_flow_target", el_i, tar])
        #                         check = False
        #                 if flow.induction:
        #                     for ind_s in flow.inducing_stages:
        #                         if not ind_s in [st.name for st in stages]:
        #                             info.append(["Not_exist_flow_istage", el_i, ind_s])
        #                             check = False
        #             else:
        #                 check = False
        #                 info += info_add
        #             el_i += 1
        #
        #         for source in source_f_sum:
        #             if source_f_sum[source] >= 1 and not self.settings.divided_n:
        #                 info.append(["Large_sum_factor_stage_as_source", source, ""])
        #                 logger.warning("Large sum factor stage as source: {}".format(source))
        #                 check = False
        #
        #     # добавление и проверка однонаправленных потоков
        #     element = "Ow_flow"
        #     el_i = 1
        #     for o_fl in self.list_owflow:
        #         ow_flow, check_add, info_add = o_fl.get_ow_flow(el_i)
        #         if check_add:
        #             ow_flows.append(ow_flow)
        #         else:
        #             check = False
        #             info += info_add
        #         el_i += 1
        #
        # except Exception as e:
        #     msg = traceback.format_exc() + "Last element: {0} No.{1}"
        #     logger.error(msg.format(element, el_i))
        #     emsg = ErrorMessage(message=msg.format(element, el_i), parent_w=self)
        #     emsg.exec_()
        #     raise SystemExit(1)
        #
        # if self.settings.stop_mode == "m":
        #     check_add, info_add = self.settings.check_limit_step()
        #     if not check_add:
        #         check = False
        #         info += info_add
        #
        # if not check:
        #     message = ""
        #     for i in info:
        #         message += self.get_message_text(i) + "\n"
        #     title = self.lang_parser.get(self.user_settings.language.upper(), title, fallback=title)
        #     msg_window = Message(message, title, self)
        #     msg_window.exec_()
        #     self.model = None
        # else:
        #     self.model = EpidemicModel(stages, flows, ow_flows, dict(vars(self.settings)))

        return True

    except json.decoder.JSONDecodeError:
        pass

        return False


def create_json_file(data: dict, name_file: str = "file", path_to_directory: str = ""):
    if len(name_file) > 0:
        if ".json" not in name_file:
            name_file += ".json"
    if len(path_to_directory) > 0:
        if "/" != path_to_directory[-1]:
            path_to_directory += "/"
    with open(f"{path_to_directory}{name_file}", "w") as write_file:
        json.dump(data, write_file, indent=4)


def convert_model_to_json(model: Model) -> dict:
    data = dict()
    data["Model_name"] = model.model_name
    data["Description"] = model.description
    data["Stages"] = model.get_list_stages()
    data["Flows"] = model.get_list_flows()
    data["Ow_flows"] = model.get_list_ow_flows()
    data["Dfactors"] = model.get_list_d_factors()
    data["Settings"] = model.get_dict_settings()
    data["Associated result files"] = model.associated_result_files
    return data


def creating_model_file():
    obj = Model(model_name="two_office",
                description="",
                stages=[Stage(name="S1", start_num="1000"),
                        Stage(name="S2", start_num="500")],
                flows=[Flow(source="S1",
                            s_factor="0.1",
                            d_factor="",
                            dynamic=False,
                            dic_target=[DictStage(stage_name="I1",
                                                  value="1")],
                            induction=True,
                            dic_ind=[DictStage(stage_name="I1",
                                               value="1"),
                                     DictStage(stage_name="I2",
                                               value="0.01")
                                     ]),
                       Flow(source="I1",
                            s_factor="0.01",
                            d_factor="",
                            dynamic=False,
                            dic_target=[DictStage(stage_name="R1",
                                                  value="1")],
                            induction=False,
                            dic_ind=[]
                            )])
    data = convert_model_to_json(model=obj)
    create_json_file(data, "test1")
