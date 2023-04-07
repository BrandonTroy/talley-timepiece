from flask import Flask, render_template, request, redirect, url_for
from json import dumps, loads
from datetime import datetime


# create and initialize app
app = Flask(__name__)
app.timezone = 'America/New_York'
with open('timezones.json') as file:
    app.timezones = loads(file.read())
app.alarms = []
app.last_ping = datetime(1970, 1, 1)
app.get_last_ping = lambda: app.last_ping.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'


# index page
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', timezones=app.timezones, current_timezone=app.timezone, last_ping=app.get_last_ping())


# request url to update the timezone, redirects to index
@app.route('/update-timezone', methods=['POST'])
def update_timezone():
    app.timezone = request.json['timezone']
    print('TIMEZONE UPDATED TO:', app.timezone)
    
    return redirect('/')


# request url to update alarms, redirects to index
@app.route('/update-alarms', methods=['POST'])
def update_alarm():
    app.alarms = [request.json['alarm1'], request.json['alarm2']]
    return redirect('/')


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
        'last_ping': app.get_last_ping()
    })


# api used to fetch data from server by pi client
@app.route('/api/pi', methods=['GET'])
def api_pi():
    app.last_ping = datetime.now()
    return dumps({
        'timezone': app.timezone,
        'alarms': app.alarms
    })