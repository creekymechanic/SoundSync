# MPV Loop Detection Script

This script detects a loop within a video playing through MPVon a Raspberry Pi 4B, and sends a signal to an ESP32 to trigger a WLED macro. 

## Notes

I used a Raspberry Pi 4B to play the video, and an ESP32 to trigger the WLED macro. The ESP32 is connected to the GPIO pin of the Raspberry Pi, and the GPIO pin is connected to a relay that triggers the WLED macro. 

The script uses the `mpv` command-line tool to play the video, and the `mpv` input IPC server to detect the loop.


## Installation

1. Ensure you have Python 3.7+ installed.

2. 
    ```
    sudo apt-get install mpv
    ```

## Usage

Run the script:

(make sure you are in the same directory as the script)
```
python3 main.py
```
