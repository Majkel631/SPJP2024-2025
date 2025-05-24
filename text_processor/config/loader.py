import json
import os

def load_config(config_path):
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")
    with open(config_path, "r") as f:
        config = json.load(f)

    if "input_dir" not in config or "output_dir" not in config or "transformations" not in config:
        raise ValueError("Missing required configuration keys.")

    config["generate_report_plot"] = bool(config.get("generate_report_plot", False))

    if not isinstance(config["generate_report_plot"], bool):
        raise ValueError("generate_report_plot must be a boolean")

    return config
