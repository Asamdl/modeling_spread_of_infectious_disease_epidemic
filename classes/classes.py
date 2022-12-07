from typing import List


class DictStage:
    def __init__(self, stage_name: str = None, value: str = None):
        self.stage_name = stage_name if stage_name is not None else ""
        self.value = value if value is not None else ""


class Settings:
    def __init__(self, check_period=100, braking_dist=20, threshold=0.0001, limit_step="1000", max_step=10000,
                 stop_mode="a", divided_n=True):
        self.check_period = check_period
        self.braking_dist = braking_dist
        self.threshold = threshold
        self.limit_step = limit_step
        self.max_step = max_step
        self.stop_mode = stop_mode
        self.divided_n = divided_n

    def get_dict_settings(self):
        data = dict()
        data["check_period"] = self.check_period
        data["braking_dist"] = self.braking_dist
        data["threshold"] = self.threshold
        data["limit_step"] = self.limit_step
        data["max_step"] = self.max_step
        data["stop_mode"] = self.stop_mode
        data["divided_n"] = self.divided_n
        return data


class Stage:
    def __init__(self, name: str = None, start_num: str = None):
        self.name = name if name is not None else ""
        self.start_num = start_num if start_num is not None else ""


class Flow:
    def __init__(self, source: str = None, s_factor: str = None, d_factor: str = None, dynamic: bool = None,
                 dic_target: list[DictStage] = None, induction: bool = None,
                 dic_ind: list[DictStage] = None):
        self.source = source if source is not None else ""
        self.s_factor = s_factor if s_factor is not None else ""
        self.d_factor = d_factor if d_factor is not None else ""
        self.dynamic = dynamic if dynamic is not None else None
        self.dic_target = dic_target if dic_target is not None else []
        self.induction = induction if induction is not None else None
        self.dic_ind = dic_ind if dic_ind is not None else []

    def get_dict_target(self) -> dict:
        data = dict()
        for dict_stage in self.dic_target:
            data[dict_stage.stage_name] = dict_stage.value
        return data

    def get_dict_ind(self) -> dict:
        data = dict()
        for dict_stage in self.dic_ind:
            data[dict_stage.stage_name] = dict_stage.value
        return data


class Model:
    def __init__(self, model_name: str = None, description: str = None, stages: list[Stage] = None,
                 flows: list[Flow] = None, ow_flows: list = None, d_factors: list = None, settings: Settings = None,
                 associated_result_files: str = None):
        self.model_name = model_name if model_name is not None else ""
        self.description = description if description is not None else ""
        self.stages = stages if stages is not None else []
        self.flows = flows if flows is not None else []
        self.ow_flows = ow_flows if ow_flows is not None else []
        self.d_factors = d_factors if d_factors is not None else []
        self.settings = settings if settings is not None else Settings()
        self.associated_result_files = associated_result_files if associated_result_files is not None else ""

    def get_list_stages(self) -> list:
        result = []
        if len(self.stages) != 0:
            for stage in self.stages:
                data = dict()
                data["name"] = stage.name
                data["start_num"] = stage.start_num
                result.append(data)
            return result
        return []

    def get_list_flows(self) -> list:
        if len(self.flows) != 0:
            result = []
            for flow in self.flows:
                data = dict()
                data["source"] = flow.source
                data["sfactor"] = flow.s_factor
                data["dfactor"] = flow.d_factor
                data["dynamic"] = flow.dynamic
                data["dic_target"] = flow.get_dict_target()
                data["induction"] = flow.induction
                data["dic_ind"] = flow.get_dict_ind()
                result.append(data)
            return result
        return []

    def get_list_ow_flows(self) -> list:
        if len(self.ow_flows) != 0:
            return []
        return []

    def get_list_d_factors(self) -> list:
        if len(self.d_factors) != 0:
            return []
        return []

    def get_dict_settings(self):
        return self.settings.get_dict_settings()
