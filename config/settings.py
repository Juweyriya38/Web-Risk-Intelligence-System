import yaml
import os

# Get the directory where this file is located
CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS_PATH = os.path.join(CONFIG_DIR, "settings.yaml")

def load_settings():
    with open(SETTINGS_PATH, 'r') as f:
        return yaml.safe_load(f)

SETTINGS = load_settings()
