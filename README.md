# Tally Timepiece

The Talley Timepiece is a 3D-printed remotely controllable alarm clock, developed for the NCSU First-Year Engineering Design Competition, earning a podium finish.

### Features
- Shows the current time and state of up to two different alarms on a physical display
- A configurable timezone (defaults based on current location)
- A choice of 3 different alarm sounds that are played by the device
- Snoozing alarms via a button on the device
- A grandfather-clock-style pendulum that ticks every second
- Fully controllable from a mobile device or PC using a web app

### Components

- **Raspberry Pi 3B**: the controller for the device, connected to peripherals and hosts the API so the web app can communicate with it.
- **API**: A Flask server running on the Raspberry Pi that exposes the timezone and alarms to be updated
- **UI**: A vanilla HTML/CSS/JS web app (hosted with Vercel) that shows connection status, and allows for viewing/updating of timezone and alarms on the clock
- **Peripherals**
    - **LCD Display**: 2x15 character display used to show the current time and alarm state
    - **GPIO Button**: used for the physical snooze/cancel button
    - **Speaker**: a portable USB speaker used to play the alarm sound
    - **Servo Motor**: used to swing the pendulum
