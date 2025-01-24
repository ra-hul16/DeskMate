import tkinter as tk
import math
import cv2
import pytesseract
import numpy as np
from tkinter import filedialog, messagebox
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
import pyperclip
import time
import json
import os
from pyzbar.pyzbar import decode
import threading

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

# Track the current running thread and stop flag
current_thread = None
current_feature = None
stop_flags = {}

# Function to stop current feature gracefully
def stop_current_feature():
    global current_thread, current_feature
    if current_feature:
        stop_flags[current_feature['name']] = True  # Set stop flag for current feature
        print(f"Stopping {current_feature['name']} feature.")
        current_feature = None
        current_thread = None

# Define functionality for each feature with graceful termination using stop flags
def google_lens_clone():
    global current_feature, current_thread
    stop_current_feature()  # Stop any running feature
    stop_flags['Text Extraction'] = False  # Reset stop flag

    # Open file dialog to select an image file
    file_path = filedialog.askopenfilename(
        title="Select an Image File",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
    )
    if not file_path:
        return
    
    try:
        image = cv2.imread(file_path)
        if image is None:
            raise ValueError("Could not read the image. Ensure the file is valid.")
        
        # Object Detection using MobileNetV2
        model = MobileNetV2(weights="imagenet")
        resized_image = cv2.resize(image, (224, 224))  # Resize to match model input size
        img_array = preprocess_input(np.expand_dims(resized_image, axis=0))
        predictions = model.predict(img_array)
        labels = decode_predictions(predictions, top=3)
        
        print("Objects detected:")
        for label in labels[0]:
            print(f"Object: {label[1]}, Confidence: {label[2]:.2f}")
        
        # Text extraction using Tesseract OCR
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(gray_image)
        print("Extracted Text:")
        print(text)
        
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def clipboard_tracker():
    global current_feature, current_thread
    stop_current_feature()  # Stop any running feature
    stop_flags['Copy-Paste'] = False  # Reset stop flag

    HISTORY_FILE = "clipboard_history.json"
    MAX_ITEMS = 100  # Maximum items to store in the history

    def load_history():
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r") as file:
                return json.load(file)
        return []

    def save_history(history):
        with open(HISTORY_FILE, "w") as file:
            json.dump(history, file, indent=4)

    clipboard_history = load_history()
    print("Clipboard Tracker started...")
    previous_clip = None

    try:
        while not stop_flags.get('Copy-Paste', False):
            current_clip = pyperclip.paste()

            if current_clip != previous_clip and current_clip.strip():
                previous_clip = current_clip
                if current_clip not in clipboard_history:
                    clipboard_history.append(current_clip)

                    # If the history exceeds the max limit, remove the oldest item
                    if len(clipboard_history) > MAX_ITEMS:
                        clipboard_history.pop(0)

                    print(f"New clipboard item added: {current_clip}")
                    save_history(clipboard_history)

            time.sleep(1)

    except Exception as e:
        messagebox.showerror("Error", f"Error in clipboard tracking: {e}")
    except KeyboardInterrupt:
        print("Clipboard Tracker stopped.")
        save_history(clipboard_history)
import tkinter as tk
from tkinter import messagebox

import tkinter as tk
from tkinter import messagebox

def to_do_list():
    def manage_to_do_list():
        # Create a new window for the To-Do List
        to_do_window = tk.Toplevel()
        to_do_window.title("To-Do List")
        to_do_window.geometry("400x500")
        to_do_window.resizable(False, False)

        # Listbox to display tasks
        task_listbox = tk.Listbox(to_do_window, font=("Arial", 14), width=30, height=15, selectmode=tk.SINGLE)
        task_listbox.pack(pady=20)

        # Entry widget for adding tasks
        task_entry = tk.Entry(to_do_window, font=("Arial", 14), width=25)
        task_entry.pack(pady=10)

        # Function to add a task
        def add_task():
            task = task_entry.get()
            if task.strip():  # Ensure the task is not empty
                task_listbox.insert(tk.END, task)
                task_entry.delete(0, tk.END)  # Clear the entry after adding
            else:
                messagebox.showwarning("Invalid Input", "Task cannot be empty!")

        # Function to remove a selected task
        def remove_task():
            try:
                selected_task_index = task_listbox.curselection()[0]
                task_listbox.delete(selected_task_index)
            except IndexError:
                messagebox.showwarning("No Selection", "Please select a task to remove!")

        # Function to clear all tasks
        def clear_tasks():
            if messagebox.askyesno("Confirmation", "Are you sure you want to clear all tasks?"):
                task_listbox.delete(0, tk.END)

        # Buttons for managing tasks
        button_frame = tk.Frame(to_do_window)
        button_frame.pack(pady=20)

        add_button = tk.Button(button_frame, text="Add Task", font=("Arial", 12), command=add_task, width=10)
        add_button.grid(row=0, column=0, padx=5)

        remove_button = tk.Button(button_frame, text="Remove Task", font=("Arial", 12), command=remove_task, width=10)
        remove_button.grid(row=0, column=1, padx=5)

        clear_button = tk.Button(button_frame, text="Clear All", font=("Arial", 12), command=clear_tasks, width=10)
        clear_button.grid(row=0, column=2, padx=5)

        # Close button
        close_button = tk.Button(to_do_window, text="Close", font=("Arial", 12), command=to_do_window.destroy, width=10)
        close_button.pack(pady=10)

    # Initialize root window
    root = tk.Tk()
    root.title("To-Do List Example")
    root.geometry("200x100")

    open_button = tk.Button(root, text="Open To-Do List", command=manage_to_do_list, width=20)
    open_button.pack(pady=20)

    root.mainloop()
def scan_qr_from_image():
    global current_feature, current_thread
    stop_current_feature()  # Stop any running feature
    stop_flags['QR Scanner'] = False  # Reset stop flag

    file_path = filedialog.askopenfilename(
        title="Select an Image File",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff")]
    )
    if not file_path:
        return

    try:
        img = cv2.imread(file_path)
        decoded_objects = decode(img)
        if decoded_objects:
            for obj in decoded_objects:
                print(f"Data in QR Code: {obj.data.decode('utf-8')}")
        else:
            print("No QR code found.")
    except Exception as e:
        messagebox.showerror("Error", f"Error reading image: {e}")

# Function to display feature icons
def toggle_features():
    global icons, current_thread, current_feature

    if icons:
        for icon in icons:
            icon.destroy()
        icons = []
    
    center_x = canvas.winfo_x() + 50
    center_y = canvas.winfo_y() + 50

    for i, feature in enumerate(FEATURES):
        angle = math.radians((360 / len(FEATURES)) * i)
        x = center_x + RADIUS * math.cos(angle)
        y = center_y + RADIUS * math.sin(angle)

        frame = tk.Frame(root, bg="white", highlightbackground="black", highlightthickness=1)
        frame.place(x=x-50, y=y-50, width=100, height=70)

        def on_enter(event, f=frame):
            f.config(bg="#d1e7ff")

        def on_leave(event, f=frame):
            f.config(bg="white")

        frame.bind("<Enter>", on_enter)
        frame.bind("<Leave>", on_leave)

        def on_click(event, func=feature["function"], f=frame, name=feature["name"]):
            global current_thread, current_feature
            # If the feature is already running, do nothing
            if current_feature and current_feature["name"] == name:
                return

            # Stop the current feature and start the new one
            stop_current_feature()
            current_feature = feature
            current_thread = threading.Thread(target=func)
            current_thread.start()

        frame.bind("<Button-1>", on_click)

        lbl_symbol = tk.Label(frame, text=feature["symbol"], font=("Arial", 18), bg="white")
        lbl_symbol.pack(pady=(5, 0))

        lbl_name = tk.Label(frame, text=feature["name"], font=("Arial", 10), bg="white")
        lbl_name.pack()

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
canvas.place(x=300, y=300)

# Draw the circular button on the canvas
circle = canvas.create_oval(0, 0, 100, 100, fill="black", outline="")

# Bind click and drag events to the canvas
canvas.bind("<Button-1>", lambda event: toggle_features())
canvas.bind("<ButtonPress-3>", on_drag_start)  # Right mouse button to start dragging
canvas.bind("<B3-Motion>", on_drag_motion)  # Drag with right mouse button

# Run the application
root.mainloop()
