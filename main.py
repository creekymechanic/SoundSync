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

    # Wait for mpv to initialize and create the socket
    socket_created = False
    for _ in range(30):  # Try for 30 seconds
        if os.path.exists(SOCKET_PATH):
            socket_created = True
            break
        time.sleep(1)

    if not socket_created:
        print("Error: MPV socket not created. Check if MPV is running correctly.")
        mpv_process.terminate()
        GPIO.cleanup()
        return

    try:
        last_position = 0
        while True:
            try:
                current_position = get_mpv_property("playback-time")
                
                if current_position < last_position:
                    send_signal()
                    print("Video looped. Signal sent to ESP32.")
                
                last_position = current_position
            except (json.JSONDecodeError, socket.error) as e:
                print(f"Error communicating with MPV: {e}")
                time.sleep(1)  # Wait a bit before retrying
            
            time.sleep(0.1)  # Check every 100ms

    except KeyboardInterrupt:
        print("Stopping playback and cleaning up GPIO.")
    finally:
        mpv_process.terminate()
        GPIO.cleanup()

if __name__ == '__main__':
    main()