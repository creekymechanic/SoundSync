import os
import time
import json
import socket
import subprocess
import RPi.GPIO as GPIO

# Configuration
VIDEO_PATH = os.path.join(os.path.dirname(__file__), 'videos', 'portal_v8.mp4')
GPIO_PIN = 18  # Replace with the GPIO pin number you are using
SIGNAL_DURATION = 1  # Duration in seconds for which the signal will be HIGH
SOCKET_PATH = '/tmp/mpvsocket'

def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_PIN, GPIO.OUT)
    GPIO.output(GPIO_PIN, GPIO.LOW)

def send_signal():
    GPIO.output(GPIO_PIN, GPIO.HIGH)
    time.sleep(SIGNAL_DURATION)
    GPIO.output(GPIO_PIN, GPIO.LOW)

def get_mpv_property(property_name):
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect(SOCKET_PATH)
    
    command = {"command": ["get_property", property_name]}
    sock.sendall(json.dumps(command).encode() + b'\n')
    
    response = sock.recv(1024).decode()
    sock.close()
    
    return json.loads(response)["data"]

def main():
    setup_gpio()

    # Start mpv with IPC socket and looping enabled
    mpv_command = [
        'mpv',
        '--input-ipc-server=' + SOCKET_PATH,
        '--loop-file=inf',
        '--fullscreen',
        VIDEO_PATH
    ]
    mpv_process = subprocess.Popen(mpv_command)

    print("Video playback started.")

    # Wait for mpv to initialize
    time.sleep(2)

    try:
        last_position = 0
        while True:
            current_position = get_mpv_property("playback-time")
            
            if current_position < last_position:
                send_signal()
                print("Video looped. Signal sent to ESP32.")
            
            last_position = current_position
            time.sleep(0.1)  # Check every 100ms

    except KeyboardInterrupt:
        print("Stopping playback and cleaning up GPIO.")
    finally:
        mpv_process.terminate()
        GPIO.cleanup()

if __name__ == '__main__':
    main()