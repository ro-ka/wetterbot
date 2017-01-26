import datetime
import time
from math import ceil
from subprocess import call
from threading import Timer
from forecastiopy import *

apikey = "b000faf5c496e99723a1d7ffddecb9ec"

call(['pico2wave', '--wave=empty.wav', '"   "'])
call(['pico2wave', '--lang=de-DE', '--wave=greeting.wav', 'Hallo.'])
call(['pico2wave', '--lang=de-DE', '--wave=currently.wav', ''])
call(['pico2wave', '--lang=de-DE', '--wave=hourly.wav', ''])

def sayIt():
    call(['aplay', 'empty.wav'])
    time.sleep(0.5)

    call(['aplay', 'greeting.wav'])
    call(['aplay', 'currently.wav'])
    call(['aplay', 'hourly.wav'])

def loadForecast():
    print("LOAD FORECAST")

    Timer(1800.0, loadForecast).start()

    fio = ForecastIO.ForecastIO(apikey,
            units=ForecastIO.ForecastIO.UNITS_SI,
            lang=ForecastIO.ForecastIO.LANG_GERMAN,
            latitude=53.5630217,
            longitude=10.0095132)

    prepare(fio)

def prepare(fio):
    if fio is None:
        return

    if fio.has_currently() is True:
        currently = FIOCurrently.FIOCurrently(fio)
        currently_summary = currently.summary + ' bei ' + temperatureToString(currently.temperature) + ' Grad.'
        text = '"Aktuell  ' + currently_summary.encode('utf-8') + '"'
        call(['pico2wave', '--lang=de-DE', '--wave=currently.wav', text])

    if fio.has_hourly() is True:
        hourly = FIOHourly.FIOHourly(fio)
        dataForDay = getDataByDay(hourly.data)
        temperatures = list(map(lambda timestep: timestep['temperature'], dataForDay))
        maxTemperature = max(temperatures)
        hourly_summary = hourly.summary + ' Maximal ' + temperatureToString(maxTemperature) + ' Grad.'
        text = '"Vorschau   ' + hourly_summary.encode('utf-8') + '"'
        call(['pico2wave', '--lang=de-DE', '--wave=hourly.wav', text])

def temperatureToString(temperature):
    return str(int(ceil(temperature)))

def addDayToData(timestep):
    timestep['day'] = datetime.date.fromtimestamp(timestep['time'])
    return timestep

def getDataByDay(allData):
    now = datetime.datetime.now()
    today = datetime.date.today()
    if now.hour < 15:
        day = today
    else:
        day = today + datetime.timedelta(days=1)

    allData = map(addDayToData, allData)
    return filter(lambda timestep: timestep['day'] == day, allData)
