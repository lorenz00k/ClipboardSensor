# Clipboard Watcher

A lightweight Python script that monitors the clipboard and automatically censors sensitive personal data — replacing it with placeholder text in real time.

## Purpose

Whenever you copy text containing sensitive information (e.g. your full name, student ID, or account name), this script detects it and replaces it in the clipboard before you paste it anywhere. Useful when working with documents, emails, or chat apps where you want to avoid accidentally sharing personal data.

## Requirements

- Linux (Ubuntu recommended)
- Python 3
- `xclip` (for clipboard access on Linux)

## Setup (Linux)

**1. Install system dependency**
```bash
sudo apt install xclip
```

**2. Create a virtual environment**
```bash
python3 -m venv ~/venvs/clipboard_env
source ~/venvs/clipboard_env/bin/activate
```

**3. Install Python dependency**
```bash
pip install pyperclip
```

**4. Run the script**
```bash
python3 clipboard_watcher.py
```

The script will now run in the background and monitor your clipboard.

## Configuration

Edit the `censorship_dict` in `clipboard_watcher.py` to define which words should be replaced and what they should be replaced with:

```python
censorship_dict = {
    "John Doe":   "fullName",
    "jdoe42":     "uAccount",
    "John":       "preName",
    "Doe":        "LastName",
    "12345678":   "MATR"
}
```

## Auto-start on Boot (optional)

To run the script automatically on login, add it to your crontab:

```bash
crontab -e
```

Add this line (adjust paths as needed):
```
@reboot /home/yourUsername/venvs/clipboard_env/bin/python /path/to/clipboard_watcher.py
```

## Setup (macOS)

**1. Create a virtual environment**
```bash
python3 -m venv ~/venvs/clipboard_env
source ~/venvs/clipboard_env/bin/activate
```

**2. Install Python dependency**
```bash
pip install pyperclip
```

> No `xclip` needed — macOS has built-in clipboard access.

**3. Run the script**
```bash
python3 clipboard_watcher.py
```

## Auto-start on Boot (macOS)

On macOS, use **launchd** instead of crontab:

**1. Create a plist file**
```bash
nano ~/Library/LaunchAgents/com.user.clipboardwatcher.plist
```

**2. Insert the following content** (adjust paths):
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.user.clipboardwatcher</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/yourUsername/venvs/clipboard_env/bin/python</string>
        <string>/Users/yourUsername/path/to/clipboard_watcher.py</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
```

**3. Enable the service**
```bash
launchctl load ~/Library/LaunchAgents/com.user.clipboardwatcher.plist
```

## Notes

- Images or non-text clipboard content are safely ignored (no crash)
- The replacement is case-insensitive
- The script only modifies the clipboard if a match is found