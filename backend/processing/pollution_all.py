import json
import os
from backend.crawler.province_fetcher import AirQualityFetcher

def pollution_all():
    '''处理全国aqi'''
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
            res[city] = int(tmp[1])
    with open(os.path.join(os.path.dirname(__file__), '../data/processed/pollution_all.json'), 'w', encoding='utf-8') as f:
        json.dump(res, f, ensure_ascii=False, indent=4)
        
if __name__ == '__main__':
    pollution_all()