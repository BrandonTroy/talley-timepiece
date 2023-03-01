from flask import Flask, render_template, request, redirect, url_for
from json import dumps, loads


# create and initialize app
app = Flask(__name__)
app.timezone = 'America/New_York'
with open('timezones.json') as file:
    app.timezones = loads(file.read())
app.alarms = []


# index page
@app.route('/')
def index():
    return render_template('index.html', timezones=app.timezones, default=app.timezone)


# request url to update the timezone, redirects to index
@app.route('/update-timezone', methods=['POST'])
def update_timezone():
    app.timezone = request.json['timezone']
    print("TIMEZONE UPDATED TO:" , app.timezone)
    return redirect('/')


# request url to add a new alarm, redirects to index
@app.route('/add-alarm', methods=['POST'])
def add_alarm():
    # add alarm
    print("ALARM ADDED:", request.args['alarm'])
    return redirect('/')


# request url to update an alarm, redirects to index
@app.route('/update-alarm', methods=['POST'])
def update_alarm():
    # update alarm
    print("ALARM UPDATED:", request.args['alarm'])
    return redirect('/')


# request url to remove an alarm, redirects to index
@app.route('/remove-alarm', methods=['POST'])
def remove_alarm():
    # remove alarm
    print("ALARM REMOVED:", request.args['alarm'])
    return redirect('/')


# api used to fetch data from server
@app.route('/api')
def api():
    return dumps({
        'timezone': app.timezone,
        'alarms': app.alarms
    })