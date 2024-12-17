import csv
import requests
import os
class AQIFetcher:
    '''查单一城市当前情况调这个，初始化类的时候会清空'''
    def __init__(self):
        self.CityCodeUrl = "https://air.cnemc.cn:18007/CityData/GetCitiesByPid?pid="
        self.CityReportUrl = "https://air.cnemc.cn:18007/CityData/GetAQIDataPublishLiveInfo?cityCode="
        with open(os.path.join(os.path.dirname(__file__), '../data/raw/CityReport.csv'), mode="w", newline="", encoding="utf-8") as f:
            pass
    def CityIDFetch(self, start=1, end=31):
        CityId = []
        for pid in range(start, end + 1):
            response = requests.get(self.CityCodeUrl + str(pid))
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    for entry in data:
                        city_info = {
                            "Id": entry.get("Id", ""),
                            "CityCode": entry.get("CityCode", ""),
                            "CityName": entry.get("CityName", ""),
                            "ProvinceId": entry.get("ProvinceId", ""),
                            "CityJC": entry.get("CityJC", ""),
                        }
                        CityId.append(city_info)

        with open(os.path.join(os.path.dirname(__file__), '../data/CityInfo.csv'), mode="w", newline="", encoding="utf-8") as file:
            headers = ["Id", "CityCode", "CityName", "ProvinceId", "CityJC"]
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(CityId)
    def getCityCode(self, CityName='北京市'):
        '''获取城市的城市ID'''
        with open(os.path.join(os.path.dirname(__file__), '../data/CityInfo.csv'), mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['CityName'] == CityName:
                    return row["CityCode"]
        return None
    def CityAQIQuery(self, CityCode):
        '''根据城市ID查询当前空气质量，存到../data/raw/CityReport.csv'''
        response = requests.get(self.CityReportUrl + str(CityCode))
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, dict):
                city_info = {
                    "Id": data.get("Id", ""),
                    "CityCode": data.get("CityCode", ""),
                    "Area": data.get("Area", ""),
                    "CO": data.get("CO", ""),
                    "NO2": data.get("NO2", ""),
                    "O3": data.get("O3", ""),
                    "PM10": data.get("PM10", ""),
                    "PM2_5": data.get("PM2_5", ""),
                    "SO2": data.get("SO2", ""),
                    "AQI": data.get("AQI", ""),
                    "PrimaryPollutant": data.get("PrimaryPollutant", ""),
                    "Quality": data.get("Quality", ""),
                    "Measure": data.get("Measure", ""),
                    "Unheathful": data.get("Unheathful", ""),
                }
                file_exists = os.path.exists("data/CityReport.csv")
                with open(os.path.join(os.path.dirname(__file__), '../data/raw/CityReport.csv'), mode="a", newline="", encoding="utf-8") as file:
                    headers = [
                        "Id",
                        "CityCode",
                        "Area",
                        "CO",
                        "NO2",
                        "O3",
                        "PM10",
                        "PM2_5",
                        "SO2",
                        "AQI",
                        "PrimaryPollutant",
                        "Quality",
                        "Measure",
                        "Unheathful",
                    ]
                    writer = csv.DictWriter(file, fieldnames=headers)
                    if not file_exists or file.tell() == 0:
                        writer.writeheader()
                    writer.writerow(city_info)


if __name__ == '__main__':
    fetcher = AQIFetcher()
    id = fetcher.getCityCode('南京市')
    fetcher.CityAQIQuery(id)