import json
import os


def pollution_all():
    '''处理全国省份当前污染等级'''
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
            res[city] = tmp[1]
    with open(os.path.join(os.path.dirname(__file__), '../data/processed/pollution_all.json'), 'w', encoding='utf-8') as f:
        json.dump(res, f, ensure_ascii=False, indent=4)
        