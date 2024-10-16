import json

def get_config(config_name):
    with open(f'src/assets/{config_name}.json', 'r') as f:
        return json.load(f)