from domain.sensor import Sensor
from datetime import datetime
import random

class LightSensor(Sensor):
    def __init__(self, sensor_id: int, timestamp: datetime, config_name: str):
        super().__init__(sensor_id, timestamp, config_name)

    def generate_value(self, room: str):
        """
        Gera o valor da leitura do sensor com base nas probabilidades de cômodo e horário.
        """
        hour = self.timestamp.hour  # Obtém a hora atual

        # Chama a função de validação de horário para determinar a luminosidade base
        luminosidade_base = self.validator_hour(hour)

        # Ajusta a luminosidade base com base no cômodo
        if not 0 <= hour < 6:
            luminosidade_base = self.adjust_by_room(luminosidade_base, room)
        
        self.value = luminosidade_base

    def validator_hour(self, hour):
        """
        Valida a hora e retorna a luminosidade base.
        """
        if 0 <= hour < 6:
            luminosidade_base = random.randint(5, 15)  # Madrugada
            adjustment = self.config["time_probabilities"]["madrugada"]
        elif 6 <= hour < 12:
            luminosidade_base = random.randint(40, 60)  # Manhã
            adjustment = self.config["time_probabilities"]["manha"]
        elif 12 <= hour < 18:
            luminosidade_base = random.randint(60, 75)  # Tarde
            adjustment = self.config["time_probabilities"]["tarde"]
        else:
            luminosidade_base = random.randint(20, 40)  # Noite
            adjustment = self.config["time_probabilities"]["noite"]

        # Ajustes de luminosidade com base em eventos aleatórios
        if 2 <= hour < 3 and random.random() < adjustment:  # Aumento aleatório durante a madrugada
            luminosidade_base = min(luminosidade_base + 5, 100)
        elif 12 <= hour < 18 and random.random() < adjustment:  # Diminuição aleatória durante a tarde
            luminosidade_base = max(luminosidade_base - 5, 0)

        return luminosidade_base

    def adjust_by_room(self, luminosidade_base, room):
        """
        Ajusta o valor da luminosidade base de acordo com o cômodo.
        """
        # Ajusta a luminosidade base com base no cômodo
        adjustment = self.config["room_type_probabilities"].get(room, 0)  # Se o cômodo não estiver definido, não ajusta
        luminosidade_final = luminosidade_base + adjustment

        # Garante que o valor final fique entre 0 e 100
        return max(0, min(luminosidade_final, 100))