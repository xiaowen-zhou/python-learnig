#!/usr/bin/python3
# -*- coding: utf-8 -*-
# __author__ = "xiaowen.zhou"

import openpyxl
import requests
import datetime
import re
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(filename)s:%(lineno)d] %(levelname)s %(message)s')
logging.disable(logging.INFO)

urls = 'https://restapi.amap.com/v3/weather/weatherInfo'
file_path = r'D:\python\learn\AMap_adcode_citycode_2020_4_10.xlsx'



def get_city_code(file,city_input):
    wb = openpyxl.load_workbook(file)
    sheet = wb['Sheet1']
    city_codes = []
    city_name = []
    code = []
    for cell in list(sheet.columns)[1]:
        city_codes.append(cell.value)
    city_codes.pop(0)
    for cell in list(sheet.columns)[0]:
        city_name.append(cell.value)
    city_name.pop(0)
    city = dict(zip(city_codes,city_name))
    for value in city.values():
        if city_input in value:
            for a in range(0, len(city)):
                if list(city.values())[a] == value:
                    code.append(list(city.keys())[a])
    code = list(set(code))
    if len(code) == 0:
        print('你要查找的地区不存在')
    logging.info(code)
    return code


def get_city_weather(city_code, key='06713a1927dbeaf7dd9338dfb232a8ed', extensions='base', output='JSON'):
    url = 'https://restapi.amap.com/v3/weather/weatherInfo'
    param = {"city": city_code,
             "key": key,
             "extensions": extensions,
             "output": output}
    response = requests.get(url, params=param)
    response.raise_for_status()
    logging.debug(response.json())
    return response.json()


def get_live_weather(weather_info):
    city = weather_info['lives'][0]
    city_name = city['province'] + '-' + city['city']
    city_weather = city['weather']
    city_temp = city['temperature']
    logging.debug(city)
    print("%s" % city_name)
    print("今日%s 天气:%s 温度:%s" % (datetime.date.today(),city_weather, city_temp))
    return city


def get_forecast_weather(weather_info):
    city = weather_info['forecasts'][0]['casts']
    city_weather = city[1]['dayweather']
    city_temp = city[1]['daytemp']
    date = city[1]['date']
    logging.debug(city)
    print("明日%s 天气:%s 温度:%s" % (date, city_weather, city_temp))
    return city


if __name__ == '__main__':
    input_city = ''
    while input_city != 'exit':
        print('天气查询系统！请输入你想要查询的地区(输入exit退出)：')
        input_city = input()
        codes = get_city_code(file_path,input_city)
        for city_code in codes:
            forecast_weather_info = get_city_weather(city_code, extensions='all')
            live_weather_info = get_city_weather(city_code)
            try:
                get_live_weather(live_weather_info)
                get_forecast_weather(forecast_weather_info)
            except Exception as e:
                pass

