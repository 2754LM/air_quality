import csv
import datetime
import requests
import os

class AirQualityFetcher:
    '''查省份历史调这个'''
    # 免费key48818d97c7ef4245986eb0e924302b46
    # 付费key = "f9c84f861f284023b5d949cdf3579dc3"
    def __init__(self, province_id_file="data/province_id.csv", key="f9c84f861f284023b5d949cdf3579dc3"):
        """
        province_id_file (str): 省份ID路径。
        key (str): 和风天气key。
        """
        self.base_dir = os.path.dirname(__file__)
        self.province_id_file = os.path.join(self.base_dir, province_id_file)
        self.province_id = self._load_province_id()
        self.key = key

    def _load_province_id(self):
        """加载省份ID"""
        with open(self.province_id_file, 'r', encoding='utf-8') as f:
            csv_reader = csv.reader(f)
            return {rows[0]: rows[1] for rows in csv_reader}

    def _get_air_quality_history(self, province):
        """获取指定省份的前10天逐小时空气质量数据(付费api)"""
        location = self.province_id[province]
        today = datetime.datetime.now()
        history_data = []
        for i in range(1, 11):
            day_before = today - datetime.timedelta(days=i)
            format_day = day_before.strftime('%Y%m%d')
            print(format_day)
            url = f"https://api.qweather.com/v7/historical/air?location={location}&date={format_day}&key={self.key}"
            try:
                response = requests.get(url, timeout=10)
            except requests.exceptions.RequestException as e:
                print(e)
                return []
            history_data =  response.json().get("airHourly", []) + history_data
        return history_data
    def _get_air_quality_future(self, province):
        """获取指定省份的未来5天逐天空气质量数据"""
        location = self.province_id[province]
        # 要用免费的把apihost改成devapi.qweather.com
        url = f"https://api.qweather.com/v7/air/5d?location={location}&key={self.key}"
        try:
            response = requests.get(url, timeout=10)
        except requests.exceptions.RequestException as e:
            print(e)
            return []
        future_data = response.json().get("daily", [])
        return future_data

    def save_air_quality(self, province):
        """保存指定省份未来5天的空气质量数据到省份名.csv文件"""
        data = self._get_air_quality_future(province)
        if data == []:
            return
        file_path = os.path.join(self.base_dir, 'data/raw', f'{province}.csv')
        with open(file_path, 'w', encoding='utf-8', newline='') as f:
            csv_write = csv.writer(f)
            csv_write.writerow(['日期', '空气质量指数', '空气质量指数等级', '空气质量指数级别', '主要污染物'])
            for i in data:
                csv_write.writerow([i["fxDate"], i["aqi"], i["level"], i["category"], i["primary"]])

    def save_all_air_quality(self):
        """保存所有省份未来5天的空气质量数据到air_quality.csv文件"""
        file_path = os.path.join(self.base_dir, 'data/raw', 'air_quality.csv')
        with open(file_path, 'w', encoding='utf-8', newline='') as f:
            csv_write = csv.writer(f)
            for province in self.province_id:
                data = self._get_air_quality_future(province)
                if data == []:
                    continue
                csv_write.writerow([province])
                csv_write.writerow(['日期', '空气质量指数', '空气质量指数等级', '空气质量指数级别', '主要污染物'])
                for i in data:
                    csv_write.writerow([i["fxDate"], i["aqi"], i["level"], i["category"], i["primary"]])

    def save_air_quality_history(self, province):
        """保存指定省份的前10天空气质量数据到省份名_history.csv文件"""
        data = self._get_air_quality_history(province)
        if data == []:
            return
        file_path = os.path.join(self.base_dir, 'data/raw', f'{province}_history.csv')
        with open(file_path, 'w', encoding='utf-8', newline='') as f:
            csv_write = csv.writer(f)
            csv_write.writerow(['日期', '空气质量指数', '空气质量指数等级', '空气质量指数级别', '主要污染物',
                                'pm10', 'pm2p5', 'no2', 'so2', 'co', 'o3'])
            for i in data:
                csv_write.writerow([i["pubTime"], i["aqi"], i["level"], i["category"], i["primary"],
                                   i["pm10"], i["pm2p5"], i["no2"], i["so2"], i["co"], i["o3"]])
    # 尽量不使用！一次一块钱。
    # def save_all_air_quality_history(self):
    #     """保存所有省份的前10天空气质量数据到air_quality_history.csv文件"""
    #     file_path = os.path.join(self.base_dir, 'data/raw', 'air_quality_history.csv')
    #     with open(file_path, 'w', encoding='utf-8', newline='') as f:
    #         csv_write = csv.writer(f)
    #         for province in self.province_id:
    #             data = self._get_air_quality_history(province)
    #             if data == []:
    #                 continue
    #             csv_write.writerow([province])
    #             csv_write.writerow(['日期', '空气质量指数', '空气质量指数等级', '空气质量指数级别', '主要污染物',
    #                                 'pm10', 'pm2p5', 'no2', 'so2', 'co', 'o3'])
    #             for i in data:
    #                 csv_write.writerow([i["pubTime"], i["aqi"], i["level"], i["category"], i["primary"],
    #                                 i["pm10"], i["pm2p5"], i["no2"], i["so2"], i["co"], i["o3"]])


class AQIFetcher:
    '''查单一城市当前情况调这个'''
    def __init__(self):
        self.CityCodeUrl = "https://air.cnemc.cn:18007/CityData/GetCitiesByPid?pid="
        self.CityReportUrl = "https://air.cnemc.cn:18007/CityData/GetAQIDataPublishLiveInfo?cityCode="

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

        with open(os.path.join(os.path.dirname(__file__), 'data/CityInfo.csv'), mode="w", newline="", encoding="utf-8") as file:
            headers = ["Id", "CityCode", "CityName", "ProvinceId", "CityJC"]
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(CityId)
    def getCityCode(self, CityName='北京市'):
        '''获取城市的城市ID'''
        with open(os.path.join(os.path.dirname(__file__), 'data/CityInfo.csv'), mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['CityName'] == CityName:
                    return row["CityCode"]
        return None
    def CityAQIQuery(self, CityCode):
        '''根据城市ID查询当前空气质量，存到data/raw/CityReport.csv'''
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
                with open(os.path.join(os.path.dirname(__file__), 'data/raw/CityReport.csv'), mode="a", newline="", encoding="utf-8") as file:
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
    # 示例
    a = AirQualityFetcher()
    # a.save_air_quality('广东')
    
    
    fetcher = AQIFetcher()
    # id = fetcher.getCityCode('南京市')
    # fetcher.CityAQIQuery(id)
    
    