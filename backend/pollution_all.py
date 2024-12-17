import json
import os
from crawler import AirQualityFetcher

def pollution_all(update = False):
    if update:
        cur = AirQualityFetcher()
        cur.save_all_air_quality()
    with open(os.path.join(os.path.dirname(__file__), 'data/raw/air_quality.csv'), 'r', encoding='utf-8') as f:
        data = f.readlines()
    res = {}
    cnt = 0
    city = ""
    for line in data:
        if cnt == 0:
            city = line.strip()
        elif cnt == 2:
            tmp = line.strip().split(',')
            if(len(tmp) < 2):
                continue
            res[city] = int(tmp[1])
        cnt += 1
        if cnt == 7:
            cnt = 0
    with open(os.path.join(os.path.dirname(__file__), 'data/processed/pollution_all.json'), 'w', encoding='utf-8') as f:
        json.dump(res, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    print(pollution_all())