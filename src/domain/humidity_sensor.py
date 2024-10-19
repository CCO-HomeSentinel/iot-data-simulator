from domain.sensor import Sensor
from datetime import datetime
import random

class HumiditySensor(Sensor):
    def __init__(self, sensor_id: int, timestamp: datetime, config_name: str):
        super().__init__(sensor_id, timestamp, config_name)
        self.previous_value = random.uniform(20, 65)

    def generate_value(self, room: str):
        room_weight = self.config["room_type_probabilities"].get(room, 0)
        
        # Variação leve no valor
        variation = random.uniform(-2, 2) 
        new_value = self.previous_value + variation

        if random.random() > room_weight:
            new_value = max(20, min(new_value, 65)) 
        else:
            new_value += 15

        new_value = max(0, min(new_value, 100))

        if new_value < 20:
            print(f"Alerta! Umidade abaixo do limite mínimo: {new_value}")
        elif new_value > 65:
            print(f"Alerta! Umidade acima do limite máximo: {new_value}")
        
        # Atualiza o valor do sensor
        self.value = new_value

        # Atualiza o valor anterior para a próxima leitura
        self.previous_value = self.value

        return self.value