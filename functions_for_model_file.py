import json

from classes.classes import Model, Stage, Flow, DictStage, Settings


def load_file_model(self):
    try:
        with open(self.filename, "r", encoding="utf-8-sig") as file:
            common_dic = json.load(file)
        filename = self.filename
        model = Model()
        list_stage=[]
        list_dfactor=[]
        list_flow=[]
        list_owflow=[]
        self.take_default()
        self.filename = filename
        self.description = common_dic["Description"]
        self.model_name = common_dic["Model_name"]

        for st in common_dic["Stages"]:
            list_stage.append(Stage(st['name'], st['start_num']))
        for df in common_dic["Dfactors"]:
            pass
            #list_dfactor.append(DFactorContent(parent_w=self, **df))
        for fl in common_dic["Flows"]:
            list_flow.append(Flow(source=fl['source'],
                                  s_factor=fl['sfactor'],
                                  d_factor=fl['dfactor'],
                                  dynamic=fl['dynamic'],
                                  dic_target=[],
                                  induction=fl['induction'],
                                  dic_ind=[]))
        for ow_fl in common_dic["Ow_flows"]:
            pass
            #list_owflow.append(OWFlowContent(list_factor=self.list_dfactor, parent_w=self, **ow_fl))
        for res in common_dic["Associated result files"]:
            pass
            # if not path.exists(res["filename"]):
            #     msg = self.get_message_text(["Not_exist_result", res["filename"], ""])
            #     self.show_message(msg, "Warning_save_title")
            #     logger.warning("Not exist result {0}".format(res["filename"]))
            # else:
            #     if not res["filename"] in [r.f_path + r.file_result for r in self.list_result]:
            #         self.list_result.append(Result(parent_w=self, delimiter=self.user_settings.file_delimiter,
            #                                        floating_point=self.user_settings.floating_point,
            #                                        **res))
            #     else:
            #         msg = self.get_message_text(["Exist_result", res["filename"], ""])
            #         self.show_message(msg, "Warning_save_title")
            #         logger.warning("Exist result {0}".format(res["filename"]))
            # # self.list_result.append(ResultContent(user_settings=self.user_settings, **res))

        self.settings = Settings(**common_dic["Settings"])
        self.full_update()
        self.update_settings_model()
        self.add_recent_file()
        self.set_all_enabled(True)
        self.model_open = True
        self.full_update()

        return True

    except json.decoder.JSONDecodeError:
        #logger.debug("json.decoder.JSONDecodeError")
        info = ["Incorrect_model_file", self.filename, ""]
        msg = self.get_message_text(info)
        title = "Warning_title"
        self.show_message(msg, title)

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
