import csv
import datetime
import requests
import os

class AirQualityFetcher:
    '''查省份历史调这个'''
    # 免费key48818d97c7ef4245986eb0e924302b46
    # 付费key = "f9c84f861f284023b5d949cdf3579dc3"
    def __init__(self, province_id_file="../data/province_id.csv", key="f9c84f861f284023b5d949cdf3579dc3"):
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
        file_path = os.path.join(self.base_dir, '../data/raw', f'{province}.csv')
        with open(file_path, 'w', encoding='utf-8', newline='') as f:
            csv_write = csv.writer(f)
            csv_write.writerow(['日期', '空气质量指数', '空气质量指数等级', '空气质量指数级别', '主要污染物'])
            for i in data:
                csv_write.writerow([i["fxDate"], i["aqi"], i["level"], i["category"], i["primary"]])

    def save_all_air_quality(self):
        """保存所有省份未来5天的空气质量数据到air_quality.csv文件"""
        file_path = os.path.join(self.base_dir, '../data/raw', 'air_quality.csv')
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



if __name__ == '__main__':
    # 示例
    a = AirQualityFetcher()
    # a.save_air_quality('上海')
    # a.save_all_air_quality()
    
    