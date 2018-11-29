"""
@ Authors     : Bram van Dartel
@ Description : MijnAfvalwijzer Test Script - It queries mijnafvalwijzer.nl.
"""
from datetime import datetime, timedelta
import requests
import logging
import json

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = 'mijnafvalwijzer'
DOMAIN = 'mijnafvalwijzer'
ICON = 'mdi:delete-empty'
SENSOR_PREFIX = 'trash_'

CONST_POSTCODE = "postcode"
CONST_HUISNUMMER = "huisnummer"
CONST_TOEVOEGING = "toevoeging"

SCAN_INTERVAL = timedelta(seconds=30)
MIN_TIME_BETWEEN_UPDATES = timedelta(seconds=900)

url = ("http://json.mijnafvalwijzer.nl/?method=postcodecheck& \
        postcode=5685HE&street=&huisnummer=16& \
        platform=phone&langs=nl&")

response = requests.get(url)
json_obj = response.json()
json_data = json_obj['data']['ophaaldagen']['data']
json_data_next = json_obj['data']['ophaaldagenNext']['data']
trashTotal = [{1: 'today'}, {2: 'tomorrow'}]
countType = len(trashTotal) + 1
trashType = {}
devices = []

for item in json_data or json_data_next:
    name = item["nameType"]
    if name not in trashType:
        trash = {}
        trashType[name] = item["nameType"]
        trash[countType] = item["nameType"]
        countType += 1
        trashTotal.append(trash)

print("trashTotal:",trashTotal)

today = datetime.today().strftime("%Y-%m-%d")
dateConvert = datetime.strptime(today, "%Y-%m-%d") + timedelta(days=1)
tomorrow = datetime.strftime(dateConvert, "%Y-%m-%d")

today = '2018-11-29'
trash = {}
trashType = {}
trashToday = {}
trashTomorrow = {}
tschedule = []

for name in trashTotal:
    for item in json_data or json_data_next:
        name = item["nameType"]
        dateFormat = datetime.strptime(item['date'], "%Y-%m-%d")
        dateConvert = dateFormat.strftime("%Y-%m-%d")

        if name not in trashType:
            if item['date'] == today:
                trashToday = {}
                trashType[name] = today
                trashToday['name_type'] = "today"
                trashToday['pickup_date'] = item['nameType']
                tschedule.append(trashToday)

            if item['date'] == tomorrow:
                trashTomorrow = {}
                trashType[name] = "tomorrow"
                trashTomorrow['name_type'] = "tomorrow"
                trashTomorrow['pickup_date'] = item['nameType']
                tschedule.append(trashTomorrow)

            if item['date'] >= today:
                trash = {}
                trashType[name] = item["nameType"]
                trash['name_type'] = item['nameType']
                trash['pickup_date'] = dateConvert
                tschedule.append(trash)

#if trashToday['name_type'] = "today":
#    trashToday['pickup_date'] = item['nameType']

if len(trashToday) == 0:
    trashToday = {}
    trashType[name] = "today"
    trashToday['name_type'] = "today"
    trashToday['pickup_date'] = "None"
    tschedule.append(trashToday)

if len(trashTomorrow) == 0:
    trashTomorrow = {}
    trashType[name] = "tomorrow"
    trashTomorrow['name_type'] = "tomorrow"
    trashTomorrow['pickup_date'] = "None"
    tschedule.append(trashTomorrow)

for item in json_data or json_data_next:
    name = item["nameType"]
    if name not in trashType:
        trash = {}
        trashType[name] = item["nameType"]
        trash['name_type'] = item['nameType']
        trash['pickup_date'] = "None"
        tschedule.append(trash)

print(tschedule)



#list = ['350882 348521 350166\r\n']
#id = 348522
#if id not in [int(y) for x in list for y in x.split()]:
#    list.append(id)
#print (list)
