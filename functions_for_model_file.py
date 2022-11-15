import json
from classes import *


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
