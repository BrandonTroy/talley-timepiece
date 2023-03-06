# DEPRICATED: This file was designed to run the server from the rasberry pi itself,
# but it was decided that the server should be hosted virtually.


from flask import Flask, render_template, request, redirect, url_for
from werkzeug.serving import is_running_from_reloader
from datetime import datetime
from time import sleep
import pytz
import threading



app = Flask(__name__)
app.timezone = 'America/New_York'
app.alarms = []


# updates the time every second based on the timezone
def tick():
    while True:
        dt = datetime.now(pytz.timezone(app.timezone))
        print(dt.time().strftime("%I:%M:%S %p"))
        sleep(1)

app.time_update_thread = threading.Thread(target=tick, daemon=True)
if is_running_from_reloader():
    app.time_update_thread.start()



# index page
@app.route('/')
def index():
    return render_template('index.html')


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


# if __name__ == '__main__':
#     # debug=True allows for error messages in browser and debug prints in terminal
#     # hosts on local ip
#     app.run(debug=True)