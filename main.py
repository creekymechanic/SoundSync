import pyaudio
import numpy as np
import time
import argparse

def detect_sound(threshold=1000, silence_duration=5):
    chunk = 1024
    format = pyaudio.paInt16
    channels = 1
    rate = 44100

    p = pyaudio.PyAudio()
    stream = p.open(format=format,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)

    print(f"Listening for {silence_duration} seconds of silence...")

    silence_start = time.time()
    while True:
        data = np.frombuffer(stream.read(chunk), dtype=np.int16)
        if np.abs(data).mean() > threshold:
            if time.time() - silence_start >= silence_duration:
                print("Sound detected!")
                break
        else:
            silence_start = time.time()

    stream.stop_stream()
    stream.close()
    p.terminate()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Detect sound after a period of silence.")
    parser.add_argument("--threshold", type=int, default=1000, help="Sound detection threshold")
    parser.add_argument("--silence", type=int, default=5, help="Duration of silence before detection (seconds)")
    args = parser.parse_args()

    detect_sound(args.threshold, args.silence)