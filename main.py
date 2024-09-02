import os
import vlc
import time
import RPi.GPIO as GPIO

# Configuration
VIDEO_PATH = os.path.join(os.path.dirname(__file__), 'videos', 'portal_v8.mp4')  # Replace with the path to your video file
GPIO_PIN = 18  # Replace with the GPIO pin number you are using
SIGNAL_DURATION = 1  # Duration in seconds for which the signal will be HIGH

def setup_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_PIN, GPIO.OUT)
    GPIO.output(GPIO_PIN, GPIO.LOW)

def send_signal():
    GPIO.output(GPIO_PIN, GPIO.HIGH)
    time.sleep(SIGNAL_DURATION)
    GPIO.output(GPIO_PIN, GPIO.LOW)

def main():
    setup_gpio()
    
    instance = vlc.Instance()
    player = instance.media_player_new()
    media = instance.media_new(VIDEO_PATH)
    player.set_media(media)
    
    # Set the video to loop
    media.add_option('input-repeat=-1')
    
    player.play()
    print("Video playback started.")
    
    # Get video duration
    time.sleep(1)  # Wait for the player to initialize
    duration = player.get_length() / 1000  # Duration in seconds
    print(f"Video duration: {duration} seconds.")
    
    try:
        while True:
            time.sleep(duration)
            send_signal()
            print("Signal sent to ESP32.")
    except KeyboardInterrupt:
        print("Stopping playback and cleaning up GPIO.")
    finally:
        player.stop()
        GPIO.cleanup()

if __name__ == '__main__':
    main()
