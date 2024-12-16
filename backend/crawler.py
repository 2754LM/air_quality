import csv
import requests
import os

class AirQualityFetcher:
    def __init__(self, province_id_file="data/province_id.csv", key="48818d97c7ef4245986eb0e924302b46"):
        """
        province_id_file (str): 省份ID路径。
        key (str): 和风天气key。
        """
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.province_id_file = os.path.join(self.base_dir, province_id_file)
        self.province_id = self._load_province_id()
        self.key = key

    def _load_province_id(self):
        """加载省份ID"""
        with open(self.province_id_file, 'r', encoding='gbk') as f:
            csv_reader = csv.reader(f)
            return {rows[0]: rows[1] for rows in csv_reader}

    def _get_air_quality(self, province):
        """获取指定省份的空气质量数据"""
        if province not in self.province_id:
            return f"{province} 不在可选列表中。"
        location = self.province_id[province]
        url = f"https://devapi.qweather.com/v7/air/5d?location={location}&key={self.key}"
        try:
            response = requests.get(url, timeout=10)
        except requests.exceptions.RequestException as e:
            print(f"请求超时: {province} - {str(e)}")
            return None
        if response.status_code != 200:
            print(f"请求失败: {province} - {response.status_code} - {response.text}")
            return None
        data = response.json().get("daily")
        return data

    def save_air_quality(self, province):
        """保存指定省份的空气质量数据到省份名.csv文件"""
        data = self._get_air_quality(province)
        if data == []:
            return
        file_path = os.path.join(self.base_dir, 'data/raw', f'{province}.csv')
        with open(file_path, 'w', encoding='gbk', newline='') as f:
            csv_write = csv.writer(f)
            csv_write.writerow(['日期', '空气质量指数', '空气质量指数等级', '空气质量指数级别', '主要污染物'])
            for i in data:
                csv_write.writerow([i["fxDate"], i["aqi"], i["level"], i["category"], i["primary"]])

    def save_all_air_quality(self):
        """保存所有省份的空气质量数据到air_quality.csv文件"""
        file_path = os.path.join(self.base_dir, 'data/raw', 'air_quality.csv')
        with open(file_path, 'w', encoding='gbk', newline='') as f:
            csv_write = csv.writer(f)
            for province in self.province_id:
                data = self._get_air_quality(province)
                if data is None:
                    continue
                csv_write.writerow([province])
                csv_write.writerow(['日期', '空气质量指数', '空气质量指数等级', '空气质量指数级别', '主要污染物'])
                for i in data:
                    csv_write.writerow([i["fxDate"], i["aqi"], i["level"], i["category"], i["primary"]])