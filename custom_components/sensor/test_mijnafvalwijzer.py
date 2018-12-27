"""
@ Authors     : Bram van Dartel
@ Description : MijnAfvalwijzer Test Script - It queries mijnafvalwijzer.nl.
"""
from datetime import datetime, timedelta, date
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
json_data = (json_obj['data']['ophaaldagen']['data'] + json_obj['data']['ophaaldagenNext']['data'])

trashTotal = [{1: 'today'}, {2: 'tomorrow'}, {3: 'next'} ]
countType = len(trashTotal) + 1
trashType = {}
devices = []

for item in json_data:
    name = item["nameType"]
    if name not in trashType:
        trash = {}
        trashType[name] = item["nameType"]
        trash[countType] = item["nameType"]
        countType += 1
        trashTotal.append(trash)

#print("trashTotal:",trashTotal)

today = datetime.today().strftime("%Y-%m-%d")
dateConvert = datetime.strptime(today, "%Y-%m-%d") + timedelta(days=1)
tomorrow = datetime.strftime(dateConvert, "%Y-%m-%d")

today = '2018-07-06'
trash = {}
trashType = {}
trashToday = {}
trashTomorrow = {}
trashInDays = {}
tschedule = []

def d(s):
    [year, month, day] = map(int, s.split('-'))
    return date(year, month, day)
def days(start, end):
    return (d(end) - d(start)).days

for name in trashTotal:
    for item in json_data:
        name = item["nameType"]
        dateFormat = datetime.strptime(item['date'], "%Y-%m-%d")
        dateConvert = dateFormat.strftime("%Y-%m-%d")

        if name not in trashType:
            if item['date'] == today:
                trashToday = {}
                trashType[name] = today
                trashToday['key'] = "today"
                trashToday['value'] = item['nameType']
                tschedule.append(trashToday)

            if item['date'] == tomorrow:
                trashTomorrow = {}
                trashType[name] = "tomorrow"
                trashTomorrow['key'] = "tomorrow"
                trashTomorrow['value'] = item['nameType']
                tschedule.append(trashTomorrow)

            if item['date'] >= today:
                trash = {}
                trashType[name] = item["nameType"]
                trash['key'] = item['nameType']
                trash['value'] = dateConvert
                tschedule.append(trash)

            if item['date'] > today:
                if len(trashInDays) == 0:
                    trashType[name] = "next"
                    trashInDays['key'] = 'next'
                    trashInDays['value'] = (days(today, dateConvert))
                    tschedule.append(trashInDays)


#if trashToday['key'] = "today":
#    trashToday['value'] = item['nameType']

if len(trashToday) == 0:
   trashToday = {}
   trashType[name] = "today"
   trashToday['key'] = "today"
   trashToday['value'] = "None"
   tschedule.append(trashToday)

if len(trashTomorrow) == 0:
   trashTomorrow = {}
   trashType[name] = "tomorrow"
   trashTomorrow['key'] = "tomorrow"
   trashTomorrow['value'] = "None"
   tschedule.append(trashTomorrow)

for item in json_data:
     name = item["nameType"]
     if name not in trashType:
         trash = {}
         trashType[name] = item["nameType"]
         trash['key'] = item['nameType']
         trash['value'] = "None"
         tschedule.append(trash)

print(tschedule)



#list = ['350882 348521 350166\r\n']
#id = 348522
#if id not in [int(y) for x in list for y in x.split()]:
#    list.append(id)
#print (list)
