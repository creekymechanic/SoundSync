import os
import time
import json
import socket
import logging
import subprocess
import signal
import sys
import RPi.GPIO as GPIO

# Configuration
VIDEO_PATH = os.path.join(os.path.dirname(__file__), 'videos', 'portal_v8.mp4')
GPIO_PIN = 18  # Replace with the GPIO pin number you are using
SIGNAL_DURATION = 1  # Duration in seconds for which the signal will be HIGH
SOCKET_PATH = '/tmp/mpvsocket'

# Setup logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='soundsync.log',
                    filemode='a')
log = logging.getLogger('soundsync')

def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_PIN, GPIO.OUT)
    GPIO.output(GPIO_PIN, GPIO.LOW)

def send_signal():
    GPIO.output(GPIO_PIN, GPIO.HIGH)
    time.sleep(SIGNAL_DURATION)
    GPIO.output(GPIO_PIN, GPIO.LOW)

def get_mpv_property(property_name, max_retries=3, initial_delay=0.5):
    delay = initial_delay
    for attempt in range(max_retries):
        try:
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
                sock.settimeout(2.0)
                sock.connect(SOCKET_PATH)
                command = {"command": ["get_property", property_name]}
                sock.sendall(json.dumps(command).encode() + b'\n')
                response = sock.recv(1024).decode().strip()
            
            json_response = json.loads(response)
            if "data" in json_response:
                return json_response["data"]
            else:
                log.warning(f"Unexpected response format: {response}")
        except (json.JSONDecodeError, socket.error, KeyError) as e:
            log.error(f"Error on attempt {attempt + 1}: {e}")
            time.sleep(delay)
            delay *= 2  # Exponential backoff
    
    log.error(f"Failed to get property {property_name} after {max_retries} attempts")
    return None

def start_mpv():
    mpv_command = [
        'mpv',
        '--input-ipc-server=' + SOCKET_PATH,
        '--loop-file=inf',
        '--fullscreen',
        VIDEO_PATH
    ]
    return subprocess.Popen(mpv_command)

def restart_mpv():
    global mpv_process
    log.info("Restarting MPV...")
    if mpv_process:
        mpv_process.terminate()
        mpv_process.wait()
    mpv_process = start_mpv()
    time.sleep(2)  # Wait for MPV to initialize

def signal_handler(signum, frame):
    log.info("Received termination signal. Cleaning up...")
    if mpv_process:
        mpv_process.terminate()
    GPIO.cleanup()
    sys.exit(0)

def main():
    global mpv_process
    setup_gpio()
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    mpv_process = start_mpv()
    log.info("Video playback started.")

    # Wait for mpv to initialize and create the socket
    socket_created = False
    for _ in range(30):  # Try for 30 seconds
        if os.path.exists(SOCKET_PATH):
            socket_created = True
            break
        time.sleep(1)

    if not socket_created:
        log.error("Error: MPV socket not created. Check if MPV is running correctly.")
        mpv_process.terminate()
        GPIO.cleanup()
        return

    last_position = 0
    while True:
        try:
            current_position = get_mpv_property("playback-time")
            if current_position is not None:
                if current_position < last_position:
                    send_signal()
                    log.info(f"Video looped. Signal sent to ESP32. {current_position:.3f}")
                last_position = current_position
            else:
                log.warning("Failed to get current position. Restarting MPV.")
                restart_mpv()
        except Exception as e:
            log.error(f"Unexpected error: {e}")
            restart_mpv()
        time.sleep(0.1)  # Check every 100ms

if __name__ == '__main__':
    main()