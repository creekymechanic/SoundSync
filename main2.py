import cv2
import time
import RPi.GPIO as GPIO
import serial

# Configure GPIO
GPIO.setmode(GPIO.BCM)
ESP32_PIN = 18  # Change this to the GPIO pin connected to your ESP32
GPIO.setup(ESP32_PIN, GPIO.OUT)

# Configure serial communication with ESP32
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)  # Adjust port if needed

def play_video(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error opening video file")
        return
    
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    duration = frame_count / fps
    
    while True:
        start_time = time.time()
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            cv2.imshow('Video', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                return
        
        # Video loop detected
        print("Video loop detected")
        
        # Send signal to ESP32
        GPIO.output(ESP32_PIN, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(ESP32_PIN, GPIO.LOW)
        
        # Send serial command to ESP32 for WLED macro
        ser.write(b'M1\n')  # Adjust command as needed
        
        # Reset video to beginning
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        
        # Wait for the remaining duration if the loop finished early
        elapsed_time = time.time() - start_time
        if elapsed_time < duration:
            time.sleep(duration - elapsed_time)

try:
    video_path = 'path/to/your/video.mp4'  # Replace with your video file path
    play_video(video_path)
except KeyboardInterrupt:
    print("Script terminated by user")
finally:
    GPIO.cleanup()
    ser.close()
    cv2.destroyAllWindows()