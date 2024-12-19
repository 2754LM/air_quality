from asyncio import sleep
import datetime
import os
from backend.crawler.province_fetcher import AirQualityFetcher
from backend.processing import aqi_byhour, aqi_ranges, maxaqi_time, pollutants_all, pollution_all,pollutants_statistics,pollution_trend
def check_latest_all():
    file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', 'air_quality.csv')
    if os.path.exists(file_path) == False:
        return False
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        if len(lines) < 215:
            return False
        time = lines[2].split(',')[0]
        formatted_date = datetime.datetime.now().strftime('%Y-%m-%d')
        if(formatted_date != time):
            return False
        return True

        

def check_latest_history(province):
    file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', f'{province}_history.csv')
    if os.path.exists(file_path) == False:
        return False
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        if len(lines) < 240:
            return False
        time = lines[1].split(',')[0][0:10]
        formatted_date = (datetime.datetime.now() - datetime.timedelta(days=10)).strftime('%Y-%m-%d')
        if(formatted_date != time):
            return False
        return True

def check_latest_trend(province):
    file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', f'{province}.csv')
    if os.path.exists(file_path) == False:
        return False
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        if len(lines) < 5:
            return False
        time = lines[1].split(',')[0]
        formatted_date = datetime.datetime.now().strftime('%Y-%m-%d')
        print(formatted_date)
        print(time)
        if(formatted_date != time):
            return False
        return True

def check_latest(province = 'all', history='false'):
    if province == 'all':
        return check_latest_all()
    else:
        if history == 'true':
            return check_latest_history(province)
        else:
            return check_latest_trend(province)

def update_data(province = 'all', history='false'):
    fetcher = AirQualityFetcher()
    if province == 'all':
        # sleep(1) #测试用
        fetcher.save_all_air_quality()
        # 全国aqi
        pollution_all.pollution_all()
        # 全国aqi分档
        aqi_ranges.aqi_ranges()
        # 全国主要污染物
        pollutants_all.pollutants_all()
        # 全国主要污染物统计
        pollutants_statistics.pollutants_statistics()
    else:
        if history == 'true':
            fetcher.save_air_quality_history(province)
            maxaqi_time.process_aqi_data_simple(province)
            aqi_byhour.process_aqi_byhour(province)
        else:
            fetcher.save_air_quality(province)
            pollution_trend.pollution_trend(province)
        