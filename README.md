# Clock

- refactored server.py to app.py
- added database.txt to store last set timezone
- refactored app.py to read and write current timezone from database
- changed script.js to not autmoatically set the recommended timezone as the default but instead use a variable passed from the HTML
- TODO: add funtionality to set and update alarms
- TODO: refactor timezone selector to have button for 'auto-locate' instead of putting recommendation as first selection
- TODO: make dedicated database that stores current timezone, separate from vercel because it vercel creates multiple serverless instaces of the app so there are multiple possible values the website can display OR change to single instance hosting solution