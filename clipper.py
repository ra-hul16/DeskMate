import pyperclip
import time
import json
import os

HISTORY_FILE = "clipboard_history.json"
MAX_ITEMS = 100  # Maximum items to store in the history


def load_history():
    """Load clipboard history from a JSON file."""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as file:
            return json.load(file)
    return []


def save_history(history):
    """Save clipboard history to a JSON file."""
    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)


def clipboard_tracker():
    """Track clipboard content and maintain history."""
    clipboard_history = load_history()  # Load existing history
    print("Persistent Clipboard Tracker is running...")
    print("Press Ctrl+C to exit.\n")
    print(f"Loaded {len(clipboard_history)} items from history.\n")

    previous_clip = None

    try:
        while True:
            # Get current clipboard content
            current_clip = pyperclip.paste()

            # If clipboard content is new and not empty, add to history
            if current_clip != previous_clip and current_clip.strip():
                previous_clip = current_clip
                if current_clip not in clipboard_history:
                    clipboard_history.append(current_clip)

                    # If the history exceeds the max limit, remove the oldest item
                    if len(clipboard_history) > MAX_ITEMS:
                        clipboard_history.pop(0)

                    print(f"New clipboard item added: {current_clip}")
                    print(f"Total items tracked: {len(clipboard_history)}\n")

                    # Save updated history to file
                    save_history(clipboard_history)

            time.sleep(1)  # Check clipboard every second

    except KeyboardInterrupt:
        print("\nExiting Clipboard Tracker.")
        print("Final Clipboard History:")
        for i, item in enumerate(clipboard_history, 1):
            print(f"{i}: {item}")
        save_history(clipboard_history)  # Ensure history is saved on exit


if __name__ == "__main__":
    clipboard_tracker()
