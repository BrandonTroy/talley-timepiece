from flask import Flask, render_template, request, redirect, url_for
from json import dumps, loads
from datetime import datetime
from os import listdir, fsencode, fsdecode


# create and initialize app
app = Flask(__name__)
app.timezone = 'America/New_York'
with open('timezones.json') as file:
    app.timezones = loads(file.read())
app.alarms = []
app.last_ping = datetime(1970, 1, 1)
app.get_last_ping = lambda: app.last_ping.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
app.alarm_sounds = list(map(fsdecode, listdir(fsencode("source/audio"))))
app.alarm_sound = "rooster.wav"
app.going_off = False
app.snooze = False
app.stop = False
app.is_snoozed = False


# index page
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', timezones=app.timezones, current_timezone=app.timezone, 
                            last_ping=app.get_last_ping(), sounds=app.alarm_sounds, current_sound=app.alarm_sound,
                            going_off=app.going_off, snoozed=app.snooze)


# request url to update the timezone, redirects to index
@app.route('/update-timezone', methods=['POST'])
def update_timezone():
    app.timezone = request.json['timezone']
    print('TIMEZONE UPDATED TO:', app.timezone)
    return ''


# request url to update alarms, redirects to index
@app.route('/update-alarms', methods=['POST'])
def update_alarm():
    app.alarms = [request.json['alarm1'], request.json['alarm2']]
    app.alarm_sound = request.json['sound']
    return ''


# recieves snooze command from web client
@app.route('/go_off', methods=['POST'])
def go_off():
    app.going_off = True
    app.snooze = False
    app.is_snoozed = False
    app.stop = False
    return ''


# recieves snooze command from web client
@app.route('/snooze', methods=['POST'])
def snooze():
    app.snooze = True
    app.is_snoozed = True
    return ''


# recieved snooze command from web client
@app.route('/stop', methods=['POST'])
def stop():
    app.stop = True
    app.snooze = False
    app.is_snoozed = False
    app.going_off = False
    return ''


# api used to fetch data from server
@app.route('/api', methods=['GET'])
def api():
    return dumps({
        'timezone': app.timezone,
        'alarms': app.alarms
    })


# api used to fetch data from server by web client
@app.route('/api/client', methods=['GET'])
def api_client():
    return dumps({
        'timezone': app.timezone,
        'alarms': app.alarms,
        'last_ping': app.get_last_ping(),
        'going_off': app.going_off,
        'snooze': app.is_snoozed,
    })


# api used to fetch data from server by pi client
@app.route('/api/pi', methods=['GET'])
def api_pi():
    app.last_ping = datetime.now()
    snooze, stop = app.snooze, app.stop
    app.snooze = app.stop = False
    return dumps({
        'timezone': app.timezone,
        'alarms': app.alarms,
        'sound': app.alarm_sound,
        # 'snooze': snooze,
        # 'stop': stop
    })