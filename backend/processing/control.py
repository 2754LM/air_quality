from asyncio import sleep
from backend.crawler.province_fetcher import AirQualityFetcher
from backend.processing import aqi_ranges, pollutants_all, pollution_all,pollutants_statistics,pollution_trend


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
            sleep(1) #测试用
            # fetcher.save_air_quality_history(province)
        else:
            fetcher.save_air_quality(province)
            pollution_trend.pollution_trend(province)
        