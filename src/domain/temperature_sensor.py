from domain.sensor import Sensor
from datetime import datetime
import random

class TemperatureSensor(Sensor):
    def __init__(self, sensor_id: int, timestamp: datetime, config_name: str):
        super().__init__(sensor_id, timestamp, config_name)
        self.previous_value = random.uniform(15, 35)  # Valor inicial da temperatura em uma faixa razoável

    def generate_value(self, room: str):
        room_weight = self.config["room_type_probabilities"].get(room, 0)
        
        # Definir médias de temperatura por período do dia
        hour = self.timestamp.hour
        if 0 <= hour < 6:
            temp_base = random.uniform(15, 20)  # Madrugada
        elif 6 <= hour < 12:
            temp_base = random.uniform(18, 25)  # Manhã
        elif 12 <= hour < 18:
            temp_base = random.uniform(25, 35)  # Tarde (mais quente)
        else:
            temp_base = random.uniform(20, 25)  # Noite

        # Variação suave no valor da temperatura
        variation = random.uniform(-1, 1)
        new_value = temp_base + variation

        # Aplicar a influência do cômodo
        if random.random() > room_weight:
            new_value = max(3, min(new_value, 44)) 
        else:
            new_value += 10  

        self.value = new_value

        # Mantém o valor anterior como base para a próxima leitura
        self.previous_value = new_value

        return new_value