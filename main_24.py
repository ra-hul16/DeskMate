import tkinter as tk
import math
import cv2
import pytesseract
import numpy as np
from tkinter import Tk, filedialog
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
# Create main application window
root = tk.Tk()
root.title("Desktop Assistant")
root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")  # Full-screen transparent window
root.overrideredirect(True)  # Removes window borders
root.wm_attributes("-transparentcolor", "#f0f0f0")  # Set transparency color
root.wm_attributes("-topmost", True)  # Keep the window on top
root.config(bg="#f0f0f0")  # Transparent background

# Constants for circle layout
RADIUS = 150
FEATURES = [                                                                                    
    {"name": "Copy-Paste", "symbol": "📋", "function": lambda: clipboard_tracker()},
    {"name": "Text Extraction", "symbol": "🔍", "function": lambda: google_lens_clone()},
    {"name": "QR Scanner", "symbol": "🕵️", "function": lambda: scan_qr_from_image()},
    {"name": "To-Do List", "symbol": "🔄", "function": lambda: to_do_list()},
    {"name": "Task Reminder", "symbol": "⏑", "function": lambda: task_reminder()}
]

# Store feature icons
icons = []

# Define functionality for each feature
import cv2
import pytesseract
import numpy as np
from tkinter import Tk, filedialog
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions

def google_lens_clone():
    """
    A function that integrates both object detection using MobileNetV2
    and text extraction using Tesseract OCR, all within a single function.
    """
    # Set up Tesseract OCR path (update this to your Tesseract installation path)
    pytesseract.pytesseract.tesseract_cmd = r'C:\Users\User\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

    # Open file dialog to select an image file
    root = Tk()
    root.withdraw()  # Hide the main Tkinter window
    file_path = filedialog.askopenfilename(
        title="Select an Image File",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
    )
    if not file_path:
        print("No file selected!")
        return
    
    # Load the selected image
    image = cv2.imread(file_path)
    
    if image is None:
        print("Error: Could not read the image. Ensure the file is valid.")
        return

    # Detect objects in the image using MobileNetV2
    print("Detecting objects...")
    model = MobileNetV2(weights="imagenet")
    
    # Preprocess the image
    resized_image = cv2.resize(image, (224, 224))  # Resize to match model input size
    img_array = preprocess_input(np.expand_dims(resized_image, axis=0))
    
    # Make predictions
    predictions = model.predict(img_array)
    labels = decode_predictions(predictions, top=3)  # Decode top-3 predictions
    
    print("Objects detected:")
    for label in labels[0]:
        print(f"Object: {label[1]}, Confidence: {label[2]:.2f}")
    
    # Extract text from the image using Tesseract OCR
    print("Extracting text...")
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Convert image to grayscale for better OCR results
    
    # Perform OCR
    text = pytesseract.image_to_string(gray_image)
    
    print("Extracted Text:")
    print(text)

import pyperclip
import time
import json
import os

def clipboard_tracker():
    """Track clipboard content and maintain history in a persistent manner."""
    HISTORY_FILE = "clipboard_history.json"
    MAX_ITEMS = 100  # Maximum items to store in the history

    # Load clipboard history from a JSON file
    def load_history():
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r") as file:
                return json.load(file)
        return []

    # Save clipboard history to a JSON file
    def save_history(history):
        with open(HISTORY_FILE, "w") as file:
            json.dump(history, file, indent=4)

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

# Call the function to start clipboard tracking
clipboard_tracker()

import cv2
import tkinter as tk
from tkinter import filedialog
from pyzbar.pyzbar import decode
import threading


def scan_qr_from_image():
    """Scan QR code from an image file selected via a dialog box."""
    print("Initializing Tkinter...")
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    print("Opening file dialog...")

    # This will call the file dialog in the main thread using root.after()
    image_path = filedialog.askopenfilename(
        title="Select an Image File",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff")]
    )
    root.destroy()  # Destroy Tkinter after use

    if not image_path:
        print("No file selected.")
        return

    print(f"File selected: {image_path}")

    # Decode QR code from the selected image
    try:
        img = cv2.imread(image_path)
        decoded_objects = decode(img)
        if decoded_objects:
            for obj in decoded_objects:
                print(f"Data in QR Code: {obj.data.decode('utf-8')}")
        else:
            print("No QR code found in the image.")
    except Exception as e:
        print(f"Error reading image: {e}")


# Function to display feature icons
def toggle_features():
    global icons
    if icons:  # If icons are visible, remove them
        for icon in icons:
            icon.destroy()
        icons = []
    else:  # Display icons in a circular layout
        # Get the current position of the main circle icon
        center_x = canvas.winfo_x() + 50  # Adding half width (50) to get center
        center_y = canvas.winfo_y() + 50  # Adding half height (50) to get center

        for i, feature in enumerate(FEATURES):
            angle = math.radians((360 / len(FEATURES)) * i)
            x = center_x + RADIUS * math.cos(angle)
            y = center_y + RADIUS * math.sin(angle)

            # Frame for each feature (symbol + name)
            frame = tk.Frame(root, bg="white", highlightbackground="black", highlightthickness=1)
            frame.place(x=x-50, y=y-50, width=100, height=70)

            # Hover effects
            def on_enter(event, f=frame):
                f.config(bg="#d1e7ff")  # Light blue background on hover

            def on_leave(event, f=frame):
                f.config(bg="white")  # Revert to white background

            frame.bind("<Enter>", on_enter)
            frame.bind("<Leave>", on_leave)

            # Click functionality for each feature
            def on_click(event, func=feature["function"]):
                func()

            frame.bind("<Button-1>", on_click)  # Bind left click to function

            # Symbol
            lbl_symbol = tk.Label(frame, text=feature["symbol"], font=("Arial", 18), bg="white")
            lbl_symbol.pack(pady=(5, 0))

            # Name
            lbl_name = tk.Label(frame, text=feature["name"], font=("Arial", 10), bg="white")
            lbl_name.pack()

            # Ensure labels also respond to hover and click
            lbl_symbol.bind("<Enter>", on_enter)
            lbl_symbol.bind("<Leave>", on_leave)
            lbl_symbol.bind("<Button-1>", on_click)
            lbl_name.bind("<Enter>", on_enter)
            lbl_name.bind("<Leave>", on_leave)
            lbl_name.bind("<Button-1>", on_click)

            icons.append(frame)

# Function to drag the main circle icon
def on_drag_start(event):
    event.widget.startX = event.x
    event.widget.startY = event.y

def on_drag_motion(event):
    x = root.winfo_pointerx() - event.widget.startX
    y = root.winfo_pointery() - event.widget.startY
    canvas.place(x=x, y=y)

# Create canvas for the main circle button
canvas = tk.Canvas(root, width=100, height=100, bg="#f0f0f0", highlightthickness=0)
canvas.place(x=300, y=300)  # Default position of the icon

# Draw the circular button on the canvas
circle = canvas.create_oval(0, 0, 100, 100, fill="black", outline="")

# Bind click and drag events to the canvas
canvas.bind("<Button-1>", lambda event: toggle_features())
canvas.bind("<ButtonPress-3>", on_drag_start)  # Right mouse button to start dragging
canvas.bind("<B3-Motion>", on_drag_motion)  # Drag with right mouse button

# Run the application
root.mainloop()