# -*- encoding: utf-8 -*-

import os
import yaml

_config = None

def read_config():
    global _config
    cur_path = os.path.dirname(os.path.abspath(__file__))

    config_file_path = f"{cur_path}/config.yaml"
    if _config is None:
        with open(config_file_path, "r") as file:
            _config = yaml.safe_load(file)
        # print(_config)
    return _config


def retry_later_msg():
    return "抱歉，请稍后再试。"