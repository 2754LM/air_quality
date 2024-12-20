import csv
import json
from datetime import datetime
import os
from collections import defaultdict
def process_aqi_byhour(province_name):
    aqi_byhour = defaultdict(lambda:{"time":[],"aqi":[]})
    
    file_path = os.path.join(os.path.dirname(__file__), f'../data/raw/{province_name}_history.csv')
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:

            date_time = row['日期']
            date,time=date_time.split("T")
            time=time.split("+")[0]
            aqi=int(row["空气质量指数"])
            
            aqi_byhour[date]["time"].append(time)
            aqi_byhour[date]["aqi"].append(aqi)

    with open(os.path.join(os.path.dirname(__file__), f'../data/processed/{province_name}_aqi_byhour.json'), 'w', encoding='utf-8') as f:
        json.dump(aqi_byhour, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    province_name = "广东"
    process_aqi_byhour(province_name)