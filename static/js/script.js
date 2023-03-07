// gets the timezone referenced in the the HTML, set by the flask server
let currentTimezone = document.currentScript.getAttribute("data-timezone");
// gets the last time the server pinged the client, set by the flask server
let lastPing = document.currentScript.getAttribute("data-last-ping");


const dropdown = document.getElementById("timezone-dropdown");
const connectedStatus = document.getElementById("connected-status");
const disconnectedStatus = document.getElementById("disconnected-status");


// api request to get recommended timezone based on ip address
// TODO: refactor to no longer add a new option to the dropdown, but be a button that sets the timezone
fetch("https://worldtimeapi.org/api/ip/")
    .then(response => response.json())
    .then(json => {
        updateTime();
        const option = document.createElement("option");
        option.value = json.timezone;
        option.innerHTML = json.timezone.replaceAll("_", " ") + " (Recommended)";
        dropdown.prepend(option);
        // dropdown.value = currentTimezone;
    });


// updates the time on the page
function updateTime() {
    let time = new Date().toLocaleTimeString('en', {timeStyle: "medium", timeZone: currentTimezone});
    if (time.length == 10) time = "0" + time;
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
            
            // TODO: update alarms
        });
}




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


// updates the displayed time every second
setInterval(updateTime, 1000);
// updates client data every 5 seconds
setInterval(syncToServer, 5000);
updateConnectionStatus();