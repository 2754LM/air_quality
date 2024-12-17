import json
import os
from collections import Counter

from backend.processing import pollutants_all

def pollutants_count():
    '''统计全国省份主要污染物数量'''
    pollutants_all.pollutants_all();
    file_path = os.path.join(os.path.dirname(__file__), '../data/processed/pollutants_all.json')

    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    pollutant_counter = Counter()

    for city, pollutants in data.items():
        for pollutant in pollutants:
            if pollutant != "NA":
                pollutant_counter[pollutant] += 1

    output_path = os.path.join(os.path.dirname(__file__), '../data/processed/pollutant_statistics.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(pollutant_counter, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    pollutants_count()