import os
import sys
from typing import Dict, Any

import yaml

class ConfigStore:
    def __init__(self, config_data: Dict[str, Any]):
        self.config_data = config_data

    def get(self, param: str, default=None):
        path = param.split(".")[:-1]
        leaf = param.split(".")[-1]
        cur_section = self.config_data
        for entity in path:
            if not entity in cur_section:
                return default
            cur_section = cur_section[entity]
        if leaf not in cur_section:
            return default
        return cur_section[leaf]


if not os.path.isfile(os.environ.get("UPDATEAPI_CONFIG","")):
    print("ERROR: no configuration is available")
    sys.exit(-1)

with open(os.environ.get("UPDATEAPI_CONFIG")) as f:
    config = ConfigStore(yaml.safe_load(f))
