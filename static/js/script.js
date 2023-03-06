const dropdown = document.getElementById("timezone-dropdown");
// gets the timezone referenced in the the HTML, set by the flask server
let currentTimezone = document.currentScript.getAttribute("data-timezone");


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

// reloads the page every 30 seconds to detect whether or not the pi is live
setTimeout(() => location.reload(), 30000);