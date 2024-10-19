import csv
from domain.presence_sensor import PresenceSensor
from domain.light_sensor import LightSensor
from domain.sound_sensor import SoundSensor
from domain.flood_sensor import FloodSensor
from domain.gas_sensor import GasSensor
from domain.temperature_sensor import TemperatureSensor
from domain.humidity_sensor import HumiditySensor
from domain.smoke_sensor import SmokeSensor
from datetime import datetime, timedelta

def main():
    start_date = datetime(2023, 10, 14, 0, 0, 0)
    # Inicializando o sensor com a data de início
    sensor = SmokeSensor(1, start_date, "config_smoke_sensor")
    
    # Fim do dia (1 dia inteiro, 24 horas)
    end_date = start_date + timedelta(weeks=22)
    
    # Abrindo o arquivo CSV para escrever os resultados
    with open('sensor_data.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Escrevendo o cabeçalho do CSV
        writer.writerow(['timestamp', 'sensor_value'])
        
        # Inicia o loop para simular leituras de 5 em 5 segundos
        current_time = start_date
        while current_time < end_date:
            sensor.timestamp = current_time  # Atualiza o timestamp do sensor
            sensor.generate_value("Cozinha")
            
            # Escreve o timestamp e valor no CSV
            writer.writerow([current_time, sensor.value])
            
            # Incrementa o tempo em 5 segundos
            current_time += timedelta(seconds=5)

if __name__ == "__main__":
    main()
