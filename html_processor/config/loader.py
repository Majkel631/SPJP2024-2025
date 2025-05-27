import json
import os

def load_config(config_path):
    from utils.logger import log_info

    log_info(f"Loading configuration from: {config_path}")
    if not os.path.exists(config_path):
        raise FileNotFoundError("Config file does not exist")

    with open(config_path, 'r') as f:
        config = json.load(f)

    required_keys = ['input_dir', 'output_dir', 'overwrite_output']
    for key in required_keys:
        if key not in config:
            raise ValueError(f"Missing required config key: {key}")

    config.setdefault('generate_report_plot', False)
    config.setdefault('analysis_options', {})

    return config
