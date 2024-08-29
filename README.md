# Sound Detector

This script detects sound after a period of silence using the computer's microphone.

## Installation

1. Ensure you have Python 3.7+ installed.
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the script with default settings:
```
python main.py
```

Or customize the threshold and silence duration:
```
python main.py --threshold 1500 --silence 10
```

- `--threshold`: Sound detection threshold (default: 1000)
- `--silence`: Duration of silence before detection in seconds (default: 5)