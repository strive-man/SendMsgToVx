import os
import math
import random
import requests

from datetime import date, datetime
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate

today = datetime.now()

# 微信公众测试号ID和SECRET
app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

# 可把os.environ结果替换成字符串在本地调试
user_ids = os.environ["USER_ID"].split(',')
template_ids = os.environ["TEMPLATE_ID"].split(',')
city = os.environ["CITY"].split(',')

# 获取天气和温度
def get_weather(city):
    url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
    res = requests.get(url).json()
    weather = res['data']['list'][0]
    return weather['weather'], math.floor(weather['temp'])

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
    wea, tem = get_weather(citys[i])
    cit, dat = get_city_date(citys[i])
    data = {
        "date": {"value": "今日日期：{}".format(dat), "color": get_random_color()},
        "city": {"value": "当前城市：{}".format(cit), "color": get_random_color()},
        "weather": {"value": "今日天气：{}".format(wea), "color": get_random_color()},
        "temperature": {"value": "当前温度：{}".format(tem), "color": get_random_color()},
        "love_days": {"value": "今天是你们在一起的第{}天".format(get_count(start_dates[i])), "color": get_random_color()},
        "birthday_left": {"value": "距离她的生日还有{}天".format(get_birthday(birthdays[i])), "color": get_random_color()},
        "solary": {"value": "距离发工资还有{}天".format(get_solary(solarys[i])), "color": get_random_color()},
        "words": {"value": get_words(), "color": get_random_color()}
    }
    if get_birthday(birthdays[i]) == 0:
        data["birthday_left"]['value'] = "今天是她的生日哦，快去一起甜蜜吧"
    if get_solary(solarys[i]) == 0:
        data["solary"]['value'] = "今天发工资啦，快去犒劳一下自己吧"
    res = wm.send_template(user_ids[i], template_ids[i], data)
    print(res)
