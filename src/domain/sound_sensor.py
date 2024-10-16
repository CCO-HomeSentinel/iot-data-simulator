from domain.sensor import Sensor
from datetime import datetime
import random

class SoundSensor(Sensor):
    def __init__(self, sensor_id: int, timestamp: datetime, config_name: str):
        super().__init__(sensor_id, timestamp, config_name)

    def generate_value(self, room: str):
        """
        Gera o valor da leitura do sensor com base nas probabilidades de cômodo e horário.
        O valor do som varia de 0 a 100.
        """
        hour = self.timestamp.hour  # Obtém a hora atual

        # Chama a função de validação de horário para determinar o som base
        sound_base = self.hour_validator(hour)

        # Ajusta o som base com base no cômodo
        if not 0 <= hour < 6:
            sound_base = self.adjust_by_room(sound_base, room)

        self.value = sound_base

    def hour_validator(self, hour):
        """
        Valida a hora e retorna o som base.
        """
        if 0 <= hour < 6:
            sound_base = random.randint(0, 10)  # Madrugada
            adjustment = self.config["time_probabilities"]["madrugada"]
        elif 6 <= hour < 12:
            sound_base = random.randint(20, 40)  # Manhã
            adjustment = self.config["time_probabilities"]["manha"]
        elif 12 <= hour < 18:
            sound_base = random.randint(40, 70)  # Tarde
            adjustment = self.config["time_probabilities"]["tarde"]
        else:
            sound_base = random.randint(10, 30)  # Noite
            adjustment = self.config["time_probabilities"]["noite"]

        # Ajustes de som com base em eventos aleatórios
        if 2 <= hour < 3 and random.random() < abs(adjustment):  # Aumento aleatório durante a madrugada
            sound_base = min(sound_base + 10, 100)
        elif 12 <= hour < 18 and random.random() < abs(adjustment):  # Diminuição aleatória durante a tarde
            sound_base = max(sound_base - 10, 0)

        return sound_base

    def adjust_by_room(self, sound_base, room):
        """
        Ajusta o valor do som base de acordo com o cômodo.
        """
        adjustment = self.config["room_type_probabilities"].get(room, 0)  
        sound_final = sound_base + adjustment

        return max(0, min(sound_final, 100))
