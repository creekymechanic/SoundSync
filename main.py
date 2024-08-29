import sounddevice as sd
import numpy as np
import time
import argparse

def select_loopback_device():
    devices = sd.query_devices()
    print("Available audio devices:")
    for i, device in enumerate(devices):
        print(f"{i}: {device['name']} (inputs: {device['max_input_channels']}, outputs: {device['max_output_channels']})")
    device_id = int(input("Enter the number of the loopback or 'stereo mix' device: "))
    return device_id

def detect_sound(threshold=0.01, silence_duration=5, sample_rate=44100, block_size=1024):
    device_id = select_loopback_device()
    
    print(f"Listening for {silence_duration} seconds of silence...")
    silence_start = time.time()

    def audio_callback(indata, frames, time, status):
        nonlocal silence_start
        if status:
            print(status)
        volume = np.abs(indata[:, 0]).mean()
        if volume > threshold:
            if time.time() - silence_start >= silence_duration:
                print("Sound detected!")
                raise sd.CallbackStop()
        else:
            silence_start = time.time()

    with sd.InputStream(device=device_id, channels=1, samplerate=sample_rate, 
                        callback=audio_callback, blocksize=block_size):
        sd.sleep(int(silence_duration * 1000))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Detect sound in system audio output after a period of silence.")
    parser.add_argument("--threshold", type=float, default=0.01, help="Sound detection threshold")
    parser.add_argument("--silence", type=int, default=5, help="Duration of silence before detection (seconds)")
    args = parser.parse_args()
    
    detect_sound(args.threshold, args.silence)