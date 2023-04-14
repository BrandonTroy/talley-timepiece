// gets the timezone referenced in the the HTML, set by the flask server
let currentTimezone = document.currentScript.getAttribute("data-timezone");
// gets the last time the server pinged the client, set by the flask server
let lastPing = document.currentScript.getAttribute("data-last-ping");


const dropdown = document.getElementById("timezone-dropdown");
const connectedStatus = document.getElementById("connected-status");
const disconnectedStatus = document.getElementById("disconnected-status");

const alarm1Time = document.getElementById("alarm-1-time");
// const alarm1Days = document.getElementById("alarm-1-days");
const alarm1Active = document.getElementById("alarm-1-active");
const alarm2Time = document.getElementById("alarm-2-time");
// const alarm2Days = document.getElementById("alarm-2-days");
const alarm2Active = document.getElementById("alarm-2-active");
const alarmSound = document.getElementById("alarm-sound-dropdown");

const buttons = document.querySelector(".buttons");
const snoozeButton = document.getElementById("snooze");
const stopButton = document.getElementById("stop");


// api request to get recommended timezone based on ip address
fetch("https://ipapi.co/timezone")
    .then(response => response.text())
    .then(timezone => {
        const option = document.createElement("option");
        option.value = timezone;
        option.innerHTML = timezone.replaceAll("_", " ") + " (Recommended)";
        dropdown.prepend(option);
    })
    // backup if first api request fails
    .catch(error => {
        fetch("https://worldtimeapi.org/api/ip/")
            .then(response => response.json())
            .then(json => {
                updateTime();
                const option = document.createElement("option");
                option.value = json.timezone;
                option.innerHTML = json.timezone.replaceAll("_", " ") + " (Recommended)";
                dropdown.prepend(option);
            });
    });


// updates the time on the page
function updateTime() {
    let time = new Date().toLocaleTimeString('en', {timeStyle: "medium", timeZone: currentTimezone});
    document.getElementById("time").innerHTML = time;
}


// checks if the clients hasn't pinged the server in 10 seconds
function updateConnectionStatus() {
    if (new Date() - new Date(lastPing) > 10000) {
        disconnectedStatus.style.display = "flex";
        connectedStatus.style.display = "none";
    } else {
        connectedStatus.style.display = "flex";
        disconnectedStatus.style.display = "none";
    }
}


// syncs the client data with the server data
function syncToServer() {
    fetch("/api/client")
        .then(response => response.json())
        .then(json => {
            if (json.timezone != currentTimezone) {
                currentTimezone = json.timezone;
                dropdown.value = currentTimezone;
                updateTime();
            }

            lastPing = json.last_ping;
            updateConnectionStatus();
            
            if (json.alarms.length > 0) {
                alarm1Time.value = json.alarms[0][0];
                // alarm1Days.value = json.alarms[0][1];
                alarm1Active.checked = json.alarms[0][2];
            }
            if (json.alarms.length > 1) {
                alarm2Time.value = json.alarms[1][0];
                // alarm2Days.value = json.alarms[1][1];
                alarm2Active.checked = json.alarms[1][2];
            }

            if (json.going_off) {
                buttons.style.visibility = "visible";
            } else {
                buttons.style.visibility = "hidden";
            }
            if (json.snoozed) {
                snoozeButton.disabled = true;
            } else {
                snoozeButton.disabled = false;
            }
        });
}


// updates the server with the local alarm data
function sendAlarmData() {
    fetch("/update-alarms", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            alarm1: [
                alarm1Time.value,
                null,
                alarm1Active.checked
            ],
            alarm2: [
                alarm2Time.value,
                null,
                alarm2Active.checked
            ],
            sound: alarmSound.value
        })
    });
}

alarm1Time.addEventListener("change", sendAlarmData);
// alarm1Days.addEventListener("change", sendAlarmData);
alarm1Active.addEventListener("change", sendAlarmData);
alarm2Time.addEventListener("change", sendAlarmData);
// alarm2Days.addEventListener("change", sendAlarmData);
alarm2Active.addEventListener("change", sendAlarmData);
alarmSound.addEventListener("change", sendAlarmData);


// updates the timezone when the dropdown is changed
dropdown.addEventListener("change", event => {
    currentTimezone = dropdown.value;
    updateTime();
    fetch("/update-timezone", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({timezone: currentTimezone})
    });
});


snoozeButton.addEventListener("click", event => {
    fetch("/snooze", { method: "POST" });
    snoozeButton.disabled = true;
});

stopButton.addEventListener("click", event => {
    fetch("/stop", { method: "POST" });
    buttons.style.visibility = "hidden";
});

if (document.currentScript.getAttribute("data-going-off") === "False") {
    buttons.style.visibility = "hidden";
}


// updates the displayed time every second
updateTime();
setInterval(updateTime, 250);

// updates client data every 2 seconds
syncToServer();
setInterval(syncToServer, 2000);