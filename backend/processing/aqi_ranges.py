import json
import os

def api_ranges():
    '''统计全国省份当前污染等级数量'''
    with open(os.path.join(os.path.dirname(__file__) ,'pollution_all.json'), 'r', encoding='utf-8') as f:
        data = json.load(f)

    ranges = [
        (0, 50, '优'),
        (51, 100, '良'),
        (101, 150, '轻微污染'),
        (151, 200, '轻度污染'),
        (201, 250, '中度重污染'),
        (251,300, '重度污染')
    ]

    categories = ['优', '良', '轻微污染', '轻度污染', '中度重污染', '重度污染']
    series_data = {category: 0 for category in categories}

    for city, aqi in data.items():
        aqi = int(aqi)
        for lower, upper, category in ranges:
            if lower <= aqi <= upper:
                series_data[category] += 1
                break

    result = {
        "title": "空气质量分档",
        "categories": categories,
        "value": list(series_data.values()),
        "seriesname": "城市数量"
    }

    with open(os.path.join(os.path.dirname(__file__),'api_ranges.json'), 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

