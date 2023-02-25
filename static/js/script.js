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
        dropdown.appendChild(option);
    });

// api request to get all timezones, then add them to the dropdown
// 100ms delay to ensure that the recommended timezone is added first
setTimeout(() => {
    fetch("https://worldtimeapi.org/api/timezone/")
        .then(response => response.json())
        .then(json => {
            json.forEach(timezone => {
                if (currentTimezone == timezone) return;
                const option = document.createElement("option");
                option.value = timezone;
                option.innerHTML = timezone.replaceAll("_", " ");
                dropdown.appendChild(option);
            })
        });
}, 100);

function updateTime() {
    let time = new Date().toLocaleTimeString('en', {timeStyle: "medium", timeZone: currentTimezone});
    if (time.length == 10) time = "0" + time;
    document.getElementById("time").innerHTML = time;
}
setInterval(updateTime, 1000);



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