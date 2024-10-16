from domain.sensor import Sensor
from datetime import datetime
import random

class FloodSensor(Sensor):
    def __init__(self, sensor_id: int, timestamp: datetime, config_name: str):
        super().__init__(sensor_id, timestamp, config_name)

    def generate_value(self, is_metropoles: bool):
        """
        Gera o valor da leitura do sensor com base nas probabilidades de cômodo e horário.
        O valor do som varia de 0 a 100.
        """
        if is_metropoles:
            probability = self.config["region_probabilities"]["metropolises"]
        else:
            probability = self.config["region_probabilities"]["rural"]
        
        self.value = 1 if random.random() < probability else 0

