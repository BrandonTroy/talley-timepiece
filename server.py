from flask import Flask, render_template, request, redirect, url_for


# create and initialize app
app = Flask(__name__)
app.timezone = 'America/New_York'
app.alarms = []


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




if __name__ == '__main__':
    # debug=True allows for error messages in browser and debug prints in terminal
    # hosts on local ip
    app.run(debug=True)

    # hosts on public ip
    # app.run('0.0.0.0', port=80, debug=True)