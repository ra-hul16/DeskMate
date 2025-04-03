import os
import time
import pyperclip  # For clipboard management
import threading
from tkinter import Tk, filedialog
from PIL import Image
import pytesseract  # For OCR

# Global list to store copied texts
clipboard_history = []

# --- Features ---
def text_extraction():
    print("Feature: Text Extraction")
    try:
        # Open file dialog to select an image
        print("Please select an image file...")
        Tk().withdraw()  # Hide the main Tkinter window
        file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.tiff")]
        )

        if not file_path:
            print("No file selected. Returning to main menu.")
            return

        print(f"Selected file: {file_path}")
        
        # Perform OCR on the selected image
        image = Image.open(file_path)
        extracted_text = pytesseract.image_to_string(image)
        
        # Display the extracted text
        print("Extracted Text:")
        print(extracted_text.strip())

    except Exception as e:
        print(f"An error occurred: {e}")
from tkinter import Tk, filedialog
from PIL import Image
import pytesseract

def text_extraction():
    print("Feature: Text Extraction")
    try:
        # Open file dialog to select an image
        print("Please select an image file...")
        Tk().withdraw()  # Prevents the root window from appearing
        file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.tiff")]
        )

        if not file_path:
            print("No file selected. Returning to main menu.")
            return

        print(f"Selected file: {file_path}")
        
        # Perform OCR on the selected image
        image = Image.open(file_path)
        extracted_text = pytesseract.image_to_string(image)
        
        # Display the extracted text
        print("Extracted Text:")
        print(extracted_text.strip())

    except Exception as e:
        print(f"An error occurred: {e}")

def qr_scanner():
    print("Feature: QR Scanner")
    qr_code = input("Enter the QR code content: ")
    print(f"Scanned QR Code: {qr_code}")

def clipboard_manager():
    print("Feature: Clipboard Manager")
    print("Clipboard History (Last 20):")
    for i, item in enumerate(clipboard_history[-20:], 1):
        print(f"{i}. {item}")

def to_do_list():
    print("Feature: To-Do List")
    todo_list = []
    while True:
        print("\n1. Add Task\n2. View Tasks\n3. Remove Task\n4. Exit To-Do List")
        choice = input("Select an option: ")
        if choice == "1":
            task = input("Enter a task: ")
            todo_list.append(task)
            print("Task added!")
        elif choice == "2":
            print("Your To-Do List:")
            for i, task in enumerate(todo_list, 1):
                print(f"{i}. {task}")
        elif choice == "3":
            task_num = int(input("Enter the task number to remove: "))
            if 1 <= task_num <= len(todo_list):
                removed_task = todo_list.pop(task_num - 1)
                print(f"Removed Task: {removed_task}")
            else:
                print("Invalid task number!")
        elif choice == "4":
            print("Exiting To-Do List...")
            break
        else:
            print("Invalid choice! Try again.")

def task_reminder():
    print("Feature: Task Reminder")
    task = input("Enter the task: ")
    time_minutes = int(input("Set a reminder (in minutes): "))
    print(f"Reminder set for '{task}' in {time_minutes} minutes!")
    time.sleep(time_minutes * 60)
    print(f"Reminder: {task}")

def monitor_clipboard():
    """Monitor clipboard for changes and store history."""
    last_clipboard = ""
    while True:
        try:
            current_clipboard = pyperclip.paste()
            if current_clipboard != last_clipboard:
                clipboard_history.append(current_clipboard)
                if len(clipboard_history) > 20:  # Keep history to the last 20 entries
                    clipboard_history.pop(0)
                last_clipboard = current_clipboard
        except Exception as e:
            pass
        time.sleep(1)

# --- Main Menu ---
def main_menu():
    while True:
        print("\nMini Desktop Assistant")
        print("1. Text Extraction")
        print("2. QR Scanner")
        print("3. Clipboard Manager")
        print("4. To-Do List")
        print("5. Task Reminder")
        print("6. Exit")

        choice = input("Select a feature (1-6): ")
        if choice == "1":
            text_extraction()
        elif choice == "2":
            qr_scanner()
        elif choice == "3":
            clipboard_manager()
        elif choice == "4":
            to_do_list()
        elif choice == "5":
            task_reminder()
        elif choice == "6":
            print("Exiting Mini Desktop Assistant. Goodbye!")
            break
        else:
            print("Invalid choice! Please select a valid option.")

# --- Start Clipboard Monitoring in Background ---
clipboard_thread = threading.Thread(target=monitor_clipboard, daemon=True)
clipboard_thread.start()

# --- Start the Main Menu ---
if __name__ == "__main__":
    main_menu()
