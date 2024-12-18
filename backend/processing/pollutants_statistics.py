import json
import os
from collections import Counter

def pollutant_statistics():
    with open(os.path.join(os.path.dirname(__file__) ,'../data/processed/pollutants_all.json'), 'r', encoding='utf-8') as f:
        data = json.load(f)

    pollutants = [value for value in data.values() if value != "NA"]
    pollutant_counts = Counter(pollutants)


    result = {
        "title": "全国主要污染物统计",
        "categories": list(pollutant_counts.keys()),
        "value": list(pollutant_counts.values()),
        "seriesname": "省份数量"
    }

    with open(os.path.join(os.path.dirname(__file__),'../data/processed/pollutant_statistics.json'), 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)
    
    
