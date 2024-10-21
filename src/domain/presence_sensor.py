from domain.sensor import Sensor
from datetime import datetime
import random

class PresenceSensor(Sensor):
    def __init__(self, sensor_id: int, timestamp: datetime, config_name: str):
        super().__init__(sensor_id, timestamp, config_name)

    def generate_value(self, is_metropoles: bool, type_residence: str, room: str):
        """
        Gera o valor da leitura do sensor com base nas probabilidades de localização, tipo de residência, cômodo e horário.
        """
        total_weight = 0

        if is_metropoles:
            total_weight += self.config["region_probabilities"]["metropolises"]
        else:
            total_weight += self.config["region_probabilities"]["rural"]


        total_weight += self.config["residence_type_probabilities"].get(type_residence, 0)


        total_weight += self.config["room_type_probabilities"].get(room, 0)

        total_weight += self._get_time_probability()

        final_probability = min(total_weight, 1.0)
        self.value = 1 if random.random() < final_probability else 0
    
    def _get_time_probability(self):
        """Determina o peso extra baseado no horário do dia"""
        hour = self.timestamp.hour
        if 0 <= hour < 6:
            return self.config["time_probabilities"]["madrugada"]
        elif 6 <= hour < 12:
            return self.config["time_probabilities"]["manha"]
        elif 12 <= hour < 18:
            return self.config["time_probabilities"]["tarde"]
        else:
            return self.config["time_probabilities"]["noite"]
