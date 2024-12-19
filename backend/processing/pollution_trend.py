import csv
import json
import os

def pollution_trend(province_name):
    ''''某省份未来5天aqi'''
    path = os.getcwd()
    file_path = os.path.join(path, "backend", "data", "raw", f"{province_name}.csv")
    
    dates = []
    aqis = []
    levels = []
    level_details = []
    main_pollutants = []
    
    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            dates.append(row["日期"])
            aqis.append(int(row["空气质量指数"]))
            levels.append(row["空气质量指数等级"])
            level_details.append(row["空气质量指数级别"])
            main_pollutants.append(row["主要污染物"])

    data = {
        "dates": dates,
        "aqi": aqis,
        "level": levels,
        "level_detail": level_details,
        "main_pollutant": main_pollutants
    }

    savepath = os.path.join(path, "backend", "data", "processed", f"{province_name}.json")
    with open(savepath, mode="w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    province_name = "广东"
    pollution_trend(province_name)
