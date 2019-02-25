"""
@ Authors     : Bram van Dartel
@ Description : MijnAfvalwijzer Test Script - It queries mijnafvalwijzer.nl.
"""
from datetime import datetime, timedelta, date
import requests
import sys
from requests.exceptions import ConnectionError
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

# TESTDATA
url = ("http://json.mijnafvalwijzer.nl/?method=postcodecheck&postcode=5685HE&street=&huisnummer=16&platform=phone&langs=nl&")
url = ("http://json.mijnafvalwijzer.nl/?method=postcodecheck&postcode=5146EF&street=&huisnummer=1&platform=phone&langs=nl&")

try:
    response = requests.get(url, timeout=10)
except ConnectionError as e:
    print ('\nNo response from server:', url)
    sys.exit(1)

json_obj = response.json()
json_data = (json_obj['data']['ophaaldagen']['data'] + json_obj['data']['ophaaldagenNext']['data'])
today = datetime.today().strftime("%Y-%m-%d")
dateConvert = datetime.strptime(today, "%Y-%m-%d") + timedelta(days=1)
tomorrow = datetime.strftime(dateConvert, "%Y-%m-%d")

today = '2019-01-08'
tomorrow = '2019-01-09'

print ('Today set to:', today)
print ('Tomorrow set to:', tomorrow)

# Remove unused elements from json object
for x in json_data:
    if 'type' in x:
        del x['type']

# Select Trash
size=len(json_data)
uniqueNames = []
trashSchedule = []

for i in range(0,size,1):
    if(json_data[i]['nameType'] not in uniqueNames):
         if json_data[i]['date'] >= today:
           uniqueNames.append(json_data[i]['nameType'])
           trashSchedule.append(json_data[i])


# Append Today data
trashToday = {}
multiTrashToday = []
today_out = [x for x in trashSchedule if x['date'] == today]

if len(today_out) == 0:
    trashToday['nameType'] = 'today'
    trashToday['date'] = 'None'
    trashSchedule.append(trashToday)
else:
    for x in today_out:
        trashToday['nameType'] = 'today'
        multiTrashToday.append(x['nameType'])
    trashSchedule.append(trashToday)
    trashToday['date'] = ', '.join(multiTrashToday)


# Append Tomorrow data
trashTomorrow = {}
multiTrashTomorrow = []
tomorrow_out = [x for x in trashSchedule if x['date'] == tomorrow]

if len(tomorrow_out) == 0:
    trashTomorrow['nameType'] = 'tomorrow'
    trashTomorrow['date'] = 'None'
    trashSchedule.append(trashTomorrow)
else:
    for x in tomorrow_out:
        trashTomorrow['nameType'] = 'tomorrow'
        multiTrashTomorrow.append(x['nameType'])
    trashSchedule.append(trashTomorrow)
    trashTomorrow['date'] = ', '.join(multiTrashTomorrow)


# Append next pickup in days
trashNext = {}
next_out = [x for x in trashSchedule if x['date'] > today]

def d(s):
    [year, month, day] = map(int, s.split('-'))
    return date(year, month, day)
def days(start, end):
    return (d(end) - d(start)).days

if len(next_out) == 0:
   trashNext['nameType'] = 'days'
   trashNext['date'] = 'None'
   trashSchedule.append(trashNext)
else:
    dateFormat = datetime.strptime(next_out[0]['date'], "%Y-%m-%d")
    dateConvert = dateFormat.strftime("%Y-%m-%d")
    if len(trashNext) == 0:
        trashNext['nameType'] = 'days'
        trashNext['date'] = (days(today, dateConvert))
        trashSchedule.append(trashNext)

print(trashToday)
print(trashTomorrow)
print(trashSchedule)
