import csv
import json
from datetime import datetime
import os
from collections import defaultdict


def process_aqi_type(province_name):
    data = defaultdict(dict)
    file_path = os.path.join(os.path.dirname(
        __file__), f'../data/raw/{province_name}_history.csv')
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:

            datetime = row["日期"]
            date, time = datetime.split("T")
            hour = time.split("+")[0]

            data[date][hour] = {
                "PM10": int(row["pm10"]) if row["pm10"] else None,
                "PM2.5": int(row["pm2p5"]) if row["pm2p5"] else None,
                "NO2": int(row["no2"]) if row["no2"] else None,
                "SO2": int(row["so2"]) if row["so2"] else None,
                "CO": float(row["co"]) if row["co"] else None,
                "O3": int(row["o3"]) if row["o3"] else None,
            }

    with open(os.path.join(os.path.dirname(__file__), f'../data/processed/{province_name}_aqitype.json'), 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    province_name = "广东"
    process_aqi_type(province_name)
