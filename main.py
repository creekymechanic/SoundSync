import sounddevice as sd
import numpy as np
import time

def is_silent(data, threshold):
    return np.max(np.abs(data)) < threshold

def monitor_audio_output(threshold=0.01, sample_rate=44100, block_duration=0.05, silence_duration=5):
    def audio_callback(indata, frames, time, status):
        if status:
            print(status)
        nonlocal silent_time, start_time
        if is_silent(indata, threshold):
            silent_time = time.time() - start_time
            if silent_time >= silence_duration:
                print(f"Silence detected for {silence_duration} seconds. Sound occurred!")
                raise sd.CallbackStop()
        else:
            start_time = time.time()
            silent_time = 0

    silent_time = 0
    start_time = time.time()

    print("Monitoring audio output...")
    with sd.InputStream(callback=audio_callback, channels=1, samplerate=sample_rate, blocksize=int(sample_rate * block_duration)):
        sd.sleep(int(silence_duration * 1000))

if __name__ == "__main__":
    monitor_audio_output()