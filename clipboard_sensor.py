#!/Users/fullName/venvs/clipboard_env/bin/python

import pyperclip
import re
import time

# Define keywords and their replacements
censorship_dict = {
    	"fullName": "fullName",
	"uAccount": "uAccount",
    	"preName": "preName", 
    	"LastName": "LastName",
    	"MATR": "MATR"
}

def censor_text(text):
    """Replace keywords in the text (case-insensitive)."""
    for word, replacement in censorship_dict.items():
        text = re.sub(re.escape(word), replacement, text, flags=re.IGNORECASE)
    return text

def clipboard_watcher():
    """Monitors the clipboard and censors text if needed."""
    last_text = pyperclip.paste()

    while True:
        current_text = pyperclip.paste()

        # Only act if the clipboard content has changed
        if current_text != last_text:
            print(current_text)
            censored_text = censor_text(current_text)  # Censor keywords

            # If the text was changed, update the clipboard
            if censored_text != current_text:
                pyperclip.copy(censored_text)
                print(f"Clipboard updated: {censored_text}")

            # Update the last seen text
            last_text = current_text
        
        # Sleep a bit to save resources
        time.sleep(1)

if __name__ == "__main__":
    print("Clipboard watcher started...")
    clipboard_watcher()

