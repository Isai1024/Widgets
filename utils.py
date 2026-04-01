import os
import json

CONFIG_FILE = "data/config.json"

def load_config(config_file=CONFIG_FILE):
    if not os.path.exists(config_file): return {}
    try:
        with open(config_file, "r") as f:
            data = json.load(f)
            f.close()
            return data
    except Exception as e:
        print(f"Error loading config base widget: {e}")

def save_config(data, config_file=CONFIG_FILE):
    try:
        with open(config_file, "w") as f: json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving config: {e}")