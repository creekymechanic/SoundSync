import soundcard as sc
import numpy as np
import time
import argparse

def detect_sound(threshold=0.01, silence_duration=5, sample_rate=44100, block_size=1024):
    default_speaker = sc.default_speaker()

    print(f"Listening for {silence_duration} seconds of silence...")

    silence_start = time.time()
    with default_speaker.recorder(samplerate=sample_rate, channels=1) as mic:
        while True:
            data = mic.record(numframes=block_size)
            volume = np.abs(data).mean()
            
            if volume > threshold:
                if time.time() - silence_start >= silence_duration:
                    print("Sound detected!")
                    break
            else:
                silence_start = time.time()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Detect sound in system audio output after a period of silence.")
    parser.add_argument("--threshold", type=float, default=0.01, help="Sound detection threshold")
    parser.add_argument("--silence", type=int, default=5, help="Duration of silence before detection (seconds)")
    args = parser.parse_args()

    detect_sound(args.threshold, args.silence)