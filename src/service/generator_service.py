from service.database_service import Database
from domain.flood_sensor import FloodSensor
from domain.gas_sensor import GasSensor
from domain.humidity_sensor import HumiditySensor
from domain.light_sensor import LightSensor
from domain.presence_sensor import PresenceSensor
from domain.smoke_sensor import SmokeSensor
from domain.sound_sensor import SoundSensor
from domain.temperature_sensor import TemperatureSensor
from datetime import timedelta
import csv
import pandas as pd
import os

class DataGenerator:
    def __init__(self):
        self.db = Database()
        self.sensors_class = self._get_sensors_class()

    def generate_data(self, start_date, end_date):
        sensors = self._get_sensors()

        df_cidades_populosas = pd.read_csv("src/assets/regiao_populosa_sp.csv")
        ids_cidades_populosas = df_cidades_populosas["id"].tolist()

        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)

        for sensor in sensors:
            sensor_info = self.sensors_class[sensor["tipo_sensor"].lower()]
            sensor_class = sensor_info["class"]
            interval = sensor_info["interval"]
            city_id = sensor["cidade_id"]
            config_name = sensor_info["config"]

            is_metropoles = city_id in ids_cidades_populosas

            params = eval(sensor_info["params"]) if sensor_info["params"] else []

            if isinstance(params, str):
                params = (params,)  
            elif not isinstance(params, tuple):
                params = tuple(params)  

            sensor_instance = sensor_class(sensor["id"], start_date, config_name)

            with open(f"{output_dir}/{sensor['tipo_sensor'].lower()}_sensor_data.csv", mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["sensor_id", "timestamp", "value"])

                current_time = start_date
                while current_time < end_date:
                    sensor_instance.timestamp = current_time
                    sensor_instance.generate_value(*params)

                    writer.writerow([sensor_instance.sensor_id, current_time.isoformat(), sensor_instance.value])

                    current_time += timedelta(seconds=interval)

    def _get_sensors(self):
        self.db.open_conn()
        sensors = self.db.search(
            table_name="sensor s",
            columns=["s.id", "ms.tipo as tipo_sensor", "tc.nome as tipo_comodo", "e.cidade_id", "tr.nome as tipo_residencia"],
            join="""JOIN modelo_sensor ms ON ms.id = s.modelo_sensor_id 
            JOIN comodo_monitorado cm ON s.comodo_monitorado_id = cm.id 
            JOIN tipo_comodo tc ON tc.id = cm.tipo_comodo_id 
            JOIN residencia r ON r.id = cm.residencia_id  
            JOIN endereco e ON e.id = r.endereco_id  
            JOIN tipo_residencia tr ON tr.id = r.tipo_residencia_id""",
            limit=5
        )
        self.db.close_conn()

        return sensors

    def _get_sensors_class(self):
        return {
            "inundacao": {
                "class": FloodSensor,
                "interval": 30,
                "params": "(is_metropoles)",
                "config": "config_flood_sensor"
            },
            "gas": {
                "class": GasSensor,
                "interval": 5,
                "params": "(sensor['tipo_comodo'])",
                "config": "config_gas_sensor"
            },
            "umidade": {
                "class": HumiditySensor,
                "interval": 10,
                "params": "(sensor['tipo_comodo'])",
                "config": "config_humidity_sensor"
            },
            "luminosidade": {
                "class": LightSensor,
                "interval": 5,
                "params": "(sensor['tipo_comodo'])",
                "config": "config_light_sensor"
            },
            "movimento": {
                "class": PresenceSensor,
                "interval": 5,
                "params": "(is_metropoles, sensor['tipo_residencia'], sensor['tipo_comodo'])",
                "config": "config_presence_sensor"
            },
            "fumaca": {
                "class": SmokeSensor,
                "interval": 5,
                "params": "(sensor['tipo_comodo'])",
                "config": "config_smoke_sensor"
            },
            "som": {
                "class": SoundSensor,
                "interval": 5,
                "params": "(sensor['tipo_comodo'])",
                "config": "config_sound_sensor"
            },
            "temperatura": {
                "class": TemperatureSensor,
                "interval": 10,
                "params": "(sensor['tipo_comodo'])",
                "config": "config_temperature_sensor"
            }
        }