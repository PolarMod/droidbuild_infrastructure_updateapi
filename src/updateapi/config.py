from typing import Dict, Any

class ConfigStore:
    def __init__(self, config_data: Dict[str, Any]):
        self.config_data = config_data

    def get(self, param: str, default=None):
        path = param.split(".")[:-1]
        leaf = param.split(".")[-1]
        for entity in path:
            cur_section = cur_section[entity]
            if not entity in cur_section:
                return default
        if leaf not in cur_section:
            return default
        return cur_section[leaf]
