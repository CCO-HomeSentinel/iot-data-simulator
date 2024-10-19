from domain.sensor import Sensor
from datetime import datetime
import random

class GasSensor(Sensor):
    def __init__(self, sensor_id: int, timestamp: datetime, config_name: str):
        super().__init__(sensor_id, timestamp, config_name)
        self.previous_value = random.uniform(0, 60)

    def generate_value(self, room: str):
        room_weight = self.config["room_type_probabilities"].get(room, 0)
        
        # Define os horários de almoço e jantar
        hour = self.timestamp.hour
        is_lunch_time = 11 <= hour < 14
        is_dinner_time = 19 <= hour < 21
        
        # Variação leve no valor
        variation = random.uniform(-5, 5) 
        new_value = self.previous_value + variation

        # Probabilidades para almoço e jantar
        lunch_prob = self.config["food_time_probabilities"]["lunch"]
        dinner_prob = self.config["food_time_probabilities"]["dinner"]

        # Aumenta a probabilidade de anomalia durante o almoço ou jantar
        if is_lunch_time and random.random() < lunch_prob:
            new_value += 5
        elif is_dinner_time and random.random() < dinner_prob:
            new_value += 5

        if random.random() > room_weight:
            new_value = max(0, min(new_value, 60))  
        else:
            new_value += 10  

        new_value = max(0, min(new_value, 1000000))
        
        # Atualiza o valor do sensor
        self.value = new_value

        # Atualiza o valor anterior para a próxima leitura
        self.previous_value = self.value

        return self.value