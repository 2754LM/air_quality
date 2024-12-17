import csv
import json
import os

def pollution_trend(province_name):
    path = os.getcwd()
    file_path = os.path.join(path, "backend","data","raw", "广东.csv")
    
    data = []
    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
                data.append({
                    "date": row["日期"],
                    "aqi": int(row["空气质量指数"]),
                    "level": row["空气质量指数等级"],
                    "level_detail": row["空气质量指数级别"],
                    "main_pollutant": row["主要污染物"],
                })


    savepath =   os.path.join(path, "backend","data","processed", "广东.json")
    with open(savepath, mode="w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    province_name = "广东"
    pollution_trend(province_name)
