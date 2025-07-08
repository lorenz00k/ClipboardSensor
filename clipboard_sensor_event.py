#!/Users/fullName/venvs/clipboard_env_py312/bin/python

import objc
from Foundation import NSObject
from Cocoa import NSPasteboard, NSNotificationCenter, NSDefaultRunLoopMode, NSRunLoop, NSDate
import re
import sys
import time # For timestamping debug output, not for delays

# Define your censorship dictionary (case-insensitive)
censorship_dict = {
    "preName": "preName",
    "LastName": "lastName",
    "fullName": "Name",
    "MATR": "Matrik.",
    # Add more terms to censor here
}

def censor_text(text):
    """Replace defined keywords in the text (case-insensitive)."""
    if not text:
        return "" # Handle empty text
    
    modified_text = text
    for keyword, replacement in censorship_dict.items():
        if re.search(re.escape(keyword), text, flags=re.IGNORECASE):
            print(f"🔍 Found match: '{keyword}' → '{replacement}'")
        modified_text = re.sub(re.escape(keyword), replacement, modified_text, flags=re.IGNORECASE)
    return modified_text

class PasteboardObserver(NSObject):
    """
    An Objective-C-compatible class to observe macOS clipboard changes.
    """
    
    def init(self):
        """Initialize the observer and store initial state."""
        self = objc.super(PasteboardObserver, self).init()
        if self is None:
            return None

        self.pasteboard = NSPasteboard.generalPasteboard()
        self.last_change_count = self.pasteboard.changeCount()
        self.current_text_content = ""  # Track last known clipboard content to avoid self-triggering

        print(f"[{time.strftime('%H:%M:%S')}] Initial clipboard change count: {self.last_change_count}")
        return self

    def pasteboardChanged_(self, notification):
        """
        Called whenever NSPasteboardDidChangeNotification is triggered.
        """
        current_change_count = self.pasteboard.changeCount()

        if current_change_count != self.last_change_count:
            print(f"[{time.strftime('%H:%M:%S')}] Clipboard change detected (count: {current_change_count}).")

            pb_types = self.pasteboard.types()

            if NSPasteboard.NSPasteboardTypeString in pb_types:
                new_text = self.pasteboard.stringForType_(NSPasteboard.NSPasteboardTypeString)

                if new_text:
                    print(f"[{time.strftime('%H:%M:%S')}] New clipboard content: '{new_text}'")

                    censored_text = censor_text(new_text)

                    if censored_text != new_text:
                        # Avoid loops: store content before modifying clipboard
                        self.current_text_content = new_text
                        self.last_change_count = self.pasteboard.changeCount()

                        self.pasteboard.clearContents()
                        self.pasteboard.setString_forType_(censored_text, NSPasteboard.NSPasteboardTypeString)

                        print(f"[{time.strftime('%H:%M:%S')}] Clipboard updated: '{censored_text}'")
                    else:
                        print(f"[{time.strftime('%H:%M:%S')}] No censorship needed.")
                        self.current_text_content = new_text
            else:
                print(f"[{time.strftime('%H:%M:%S')}] Clipboard does not contain string content (types: {pb_types})")

            # Always update change count
            self.last_change_count = current_change_count


# Main execution
if __name__ == '__main__':
    print("Clipboard Watcher (macOS, Event-Based) started. Press Ctrl+C to stop.")

    observer = PasteboardObserver.alloc().init()
    notification_center = NSNotificationCenter.defaultCenter()

    notification_center.addObserver_selector_name_object_(
        observer,
        "pasteboardChanged:",  # Name of the method to call
        "NSPasteboardDidChangeNotification",
        NSPasteboard.generalPasteboard()
    )

    try:
        try:
            while True:
                NSRunLoop.currentRunLoop().runMode_beforeDate_(
                    NSDefaultRunLoopMode, 
                    NSDate.dateWithTimeIntervalSinceNow_(0.1)
                )
        except KeyboardInterrupt:
            print(f"\n[{time.strftime('%H:%M:%S')}] Clipboard Watcher stopped by user.")
            notification_center.removeObserver_(observer)
            sys.exit(0)
    except KeyboardInterrupt:
        print(f"\n[{time.strftime('%H:%M:%S')}] Clipboard Watcher stopped.")
        notification_center.removeObserver_(observer)
        sys.exit(0)
