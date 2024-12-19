import csv
import json
from datetime import datetime
import os
def process_aqi_data_simple(province_name):
    daily_max_aqi = {}
    
    file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', f'{province_name}_history.csv')
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:

            date_time = row['日期']
            date = datetime.fromisoformat(date_time).strftime('%Y-%m-%d')  
            time = datetime.fromisoformat(date_time).strftime('%H:%M')    

            aqi = int(row['空气质量指数'])

            if date not in daily_max_aqi or aqi > daily_max_aqi[date]['aqi']:
                daily_max_aqi[date] = {
                    'maxaqi_time': time,
                    'aqi': aqi
                }

    with open(os.path.join(os.path.dirname(__file__), '..', 'data', 'processed', f'{province_name}_maxaqi_time.json'), 'w', encoding='utf-8') as f:
        json.dump(daily_max_aqi, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    province_name = "广东"
    process_aqi_data_simple(province_name)