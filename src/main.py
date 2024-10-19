from service.generator_service import DataGenerator
from service.file_service import File
from config.config import get_config
from datetime import datetime

def main():
    config = get_config(config_name="config")
    start_date_str = config["start_date"]
    end_date_str = config["end_date"]

    start_date = datetime.strptime(start_date_str, '%Y-%m-%d %H:%M:%S')
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d %H:%M:%S')

    generator = DataGenerator()
    generator.generate_data(start_date, end_date)

    File().convert_to_json()

if __name__ == "__main__":
    main()
