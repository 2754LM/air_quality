import json
import os
from backend.crawler.province_fetcher import AirQualityFetcher

def pollutants_all(update=False):
    if update:
        cur = AirQualityFetcher()
        cur.save_all_air_quality()

    file_path = os.path.join(os.path.dirname(__file__), '../data/raw/air_quality.csv')
    with open(file_path, 'r', encoding='utf-8') as f:
        data = f.readlines()

    res = {}
    city = ""
    flag = False

    for line in data:
        tmp = line.strip().split(',')
        if len(tmp) == 1:
            city = tmp[0]
        elif tmp[0] == '日期':
            flag = True
        elif flag:
            flag = False
            pollutants = tmp[4] 
            res[city] = pollutants 
    with open(os.path.join(os.path.dirname(__file__), '../data/processed/pollutants_all.json'), 'w', encoding='utf-8') as f:
        json.dump(res, f, ensure_ascii=False, indent=4)


