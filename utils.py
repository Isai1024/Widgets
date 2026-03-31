import os
import json

CONFIG_FILE = "data/config.json"

def load_config():
    if not os.path.exists(CONFIG_FILE): return {}
    try:
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
            f.close()
            return data
    except Exception as e:
        print(f"Error loading config base widget: {e}")

def save_config(data):
    try:
        with open(CONFIG_FILE, "w") as f: json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving config: {e}")