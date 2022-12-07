class CZoneParameters:
    def __init__(self, name: str, stages_value: dict = None):
        self.name = name
        self.stages_value = stages_value
        self.set_init_stages()
        self.connections = dict()

    def set_connection(self, friendly_zone: str, value: float):
        self.connections[friendly_zone] = value


    def set_stage_value(self, stage: str, value: int):
        if self.stages_value is None:
            self.stages_value = dict()
        self.stages_value[stage] = value

    def set_init_stages(self):
        stages = ["S", "I"]
        def_value = 0
        for stage in stages:
            self.set_stage_value(stage, def_value)
