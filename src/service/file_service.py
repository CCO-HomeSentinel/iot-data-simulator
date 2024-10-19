import pandas as pd
import os

class File:
    def __init__(self):
        self.path_to_convert = "output"

    def convert_to_json(self):
        for filename in os.listdir(self.path_to_convert):
            if filename.endswith(".csv"):
                csv_file_path = os.path.join(self.path_to_convert, filename)

                try:
                    data = pd.read_csv(csv_file_path)
                    json_file_path = os.path.join(self.path_to_convert, filename.replace('.csv', '.json'))
                    data.to_json(json_file_path, orient='records', lines=True)
                except Exception as e:
                    print(f"Error converting {csv_file_path} to JSON: {e}")
        
        print("Conversion finished.")