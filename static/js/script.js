const dropdown = document.getElementById("timezone-dropdown");
let currentTimezone;


// api request to get recommended timezone based on ip address
fetch("https://worldtimeapi.org/api/ip/")
    .then(response => response.json())
    .then(json => {
        currentTimezone = json.timezone;
        updateTime();
        const option = document.createElement("option");
        option.value = currentTimezone;
        option.innerHTML = currentTimezone.replaceAll("_", " ") + " (Recommended)";
        dropdown.prepend(option);
        dropdown.value = currentTimezone;
    });


// updates the time on the page
function updateTime() {
    let time = new Date().toLocaleTimeString('en', {timeStyle: "medium", timeZone: currentTimezone});
    if (time.length == 10) time = "0" + time;
    document.getElementById("time").innerHTML = time;
}
setInterval(updateTime, 1000);


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
    })
});