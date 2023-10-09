import os
import math
import random
import requests

from datetime import date, datetime
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate

today = datetime.now()

# 微信公众测试号ID和SECRET
app_id = "wx66f369b9638bd494"
app_secret = "dc346cfa8031a5ef62e32cda7261b422"

# 可把os.environ结果替换成字符串在本地调试
user_ids = ["o7w3O6USLeyB3Qsi5O3PXpKeN8sQ"]
template_ids = ["Y6ROHAGcxktlDFLyLcZrSK-O9IRP0gnZpF77qxCtDXs"]

# 获取天气和温度
def get_weather():
    url = "https://restapi.amap.com/v3/weather/weatherInfo?key=eb9899a07a99342537eed8848e19c51e&city=120000&extensions=base"
    res = requests.get(url).json()
    weather = res['lives'][0]['weather']
    tem = res['lives'][0]['temperature']
    print(weather)
    print(tem)
    return weather
def get_tem():
    url = "https://restapi.amap.com/v3/weather/weatherInfo?key=eb9899a07a99342537eed8848e19c51e&city=120000&extensions=base"
    res1 = requests.get(url).json()
    tem = res1['lives'][0]['temperature']
    return tem

# math.floor("tem")

# 当前城市、日期
def get_city_date(city):
    return city, today.date().strftime("%Y-%m-%d")


# 每日一句
def get_words():
    words = requests.get("https://api.shadiao.pro/chp")
    if words.status_code != 200:
        return get_words()
    return words.json()['data']['text']


# 字体随机颜色
def get_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)
wm = WeChatMessage(client)

for i in range(len(user_ids)):
    wea = get_weather()
    tem = get_tem()
    cit, dat = get_city_date("天津")
    data = {
        "date": {"value": "{}".format(dat), "color": get_random_color()},
        "city": {"value": "{}".format(cit), "color": get_random_color()},
        "weather": {"value": "{}".format(wea), "color": get_random_color()},
        "temperature": {"value": "{}℃".format(tem), "color": get_random_color()},
        "":{},
        "words": {"value": get_words(), "color": get_random_color()}
    }
    print(data)
    res = wm.send_template(user_ids[i], template_ids[i], data)
    print(res)

