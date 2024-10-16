from datetime import datetime
from config.config import get_config

class Sensor:
    def __init__(self, sensor_id: int, timestamp: datetime, config_name: str):
        self.sensor_id = sensor_id
        self.timestamp = timestamp
        self.value = None
        self.config = get_config(config_name)

    def generate_value(self):
        raise NotImplementedError("Subclasses must implement this method")