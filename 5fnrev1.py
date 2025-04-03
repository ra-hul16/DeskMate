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
    {"name": "To-Do List", "symbol": "🎯", "function": lambda: to_do_list()},
    {"name": "Task Reminder", "symbol": "🕑", "function": lambda: task_reminder()}
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
import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
import numpy as np
import pytesseract

import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import numpy as np
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
import pytesseract


def google_lens_clone():
    def process_image():
        # Stop any running feature (if applicable, placeholder here)
        stop_flags = {'Text Extraction': False}  # Reset stop flag

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

            # Display object detection results in a text widget
            results_text = "🖼️ **Objects Detected**:\n\n"
            for label in labels[0]:
                results_text += f"- **{label[1]}** with confidence **{label[2]:.2f}**\n"

            # Text extraction using Tesseract OCR
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            text = pytesseract.image_to_string(gray_image)
            results_text += "\n✍️ **Extracted Text**:\n\n" + (text if text.strip() else "No text detected.")

            # Show results in the GUI
            results_box.delete(1.0, tk.END)
            results_box.insert(tk.END, results_text)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # Create the GUI application
    root = tk.Tk()
    root.title("Text Extraction")
    root.geometry("700x500")
    root.configure(bg="#f4f6f9")

    # Title label
    title_label = tk.Label(
        root,
        text="Google Lens Clone",
        font=("Helvetica", 18, "bold"),
        fg="white",
        bg="#2c3e50",
        padx=10,
        pady=10
    )
    title_label.pack(fill="x")

    # Instruction label
    instruction_label = tk.Label(
        root,
        text="Upload an image to detect objects and extract text.",
        font=("Helvetica", 12),
        fg="#34495e",
        bg="#f4f6f9",
        pady=5
    )
    instruction_label.pack()

    # Add a button to trigger the function
    select_button = tk.Button(
        root,
        text="Select Image and Process",
        font=("Helvetica", 12, "bold"),
        bg="#3498db",
        fg="white",
        activebackground="#2980b9",
        activeforeground="white",
        padx=10,
        pady=5,
        relief="raised",
        command=process_image
    )
    select_button.pack(pady=10)

    # Add a text widget to display results
    results_box = tk.Text(
        root,
        wrap=tk.WORD,
        width=80,
        height=20,
        font=("Courier", 10),
        bg="#ecf0f1",
        fg="#2c3e50",
        relief="sunken",
        borderwidth=2
    )
    results_box.pack(pady=10)

    # Run the GUI application
    root.mainloop()


import tkinter as tk
from tkinter import messagebox
import os
import json
import pyperclip
import time
import threading

import tkinter as tk
from tkinter import messagebox, ttk
import os
import json
import pyperclip
import time
import threading


def clipboard_tracker():
    stop_flags = {'Copy-Paste': False}  # Reset stop flag
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

    def start_tracking():
        stop_flags['Copy-Paste'] = False
        clipboard_history = load_history()
        previous_clip = None

        def track_clipboard():
            nonlocal previous_clip
            try:
                while not stop_flags['Copy-Paste']:
                    current_clip = pyperclip.paste()

                    if current_clip != previous_clip and current_clip.strip():
                        previous_clip = current_clip
                        if current_clip not in clipboard_history:
                            clipboard_history.append(current_clip)

                            # If the history exceeds the max limit, remove the oldest item
                            if len(clipboard_history) > MAX_ITEMS:
                                clipboard_history.pop(0)

                            save_history(clipboard_history)

                            # Display the new item as a separate styled label
                            item_label = tk.Label(
                                scrollable_frame,
                                text=current_clip,
                                wraplength=500,
                                justify="left",
                                anchor="w",
                                bg="#fef5e7",
                                fg="#2c3e50",
                                font=("Arial", 10, "italic"),
                                padx=10,
                                pady=5,
                                relief="groove",
                                borderwidth=2,
                            )
                            item_label.pack(fill="x", pady=2, padx=5)

                            # Automatically scroll to the bottom
                            canvas.yview_moveto(1.0)

                    time.sleep(1)

            except Exception as e:
                messagebox.showerror("Error", f"Error in clipboard tracking: {e}")

        # Run the tracking in a separate thread
        tracking_thread = threading.Thread(target=track_clipboard, daemon=True)
        tracking_thread.start()

    def stop_tracking():
        stop_flags['Copy-Paste'] = True
        messagebox.showinfo("Stopped", "Clipboard tracking stopped.")

    def load_existing_history():
        history = load_history()

        # Clear existing items in the scrollable frame
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        # Display each clipboard item separately
        for item in history:
            item_label = tk.Label(
                scrollable_frame,
                text=item,
                wraplength=500,
                justify="left",
                anchor="w",
                bg="#fef5e7",
                fg="#2c3e50",
                font=("Arial", 10, "italic"),
                padx=10,
                pady=5,
                relief="groove",
                borderwidth=2,
            )
            item_label.pack(fill="x", pady=2, padx=5)

    # Create the GUI
    root = tk.Tk()
    root.title("Clipboard Tracker")
    root.geometry("600x500")
    root.configure(bg="#ecf0f1")

    # Title label
    title_label = tk.Label(
        root,
        text="Clipboard Tracker",
        font=("Helvetica", 18, "bold"),
        bg="#ecf0f1",
        fg="#2980b9",
        pady=10,
    )
    title_label.pack()

    # Add buttons with styled appearance
    button_frame = tk.Frame(root, bg="#ecf0f1")
    button_frame.pack(pady=10)

    start_button = tk.Button(
        button_frame,
        text="Start Tracking",
        command=start_tracking,
        bg="#2ecc71",
        fg="white",
        font=("Arial", 12, "bold"),
        activebackground="#27ae60",
        activeforeground="white",
        relief="raised",
        borderwidth=2,
        padx=10,
    )
    start_button.grid(row=0, column=0, padx=10)

    stop_button = tk.Button(
        button_frame,
        text="Stop Tracking",
        command=stop_tracking,
        bg="#e74c3c",
        fg="white",
        font=("Arial", 12, "bold"),
        activebackground="#c0392b",
        activeforeground="white",
        relief="raised",
        borderwidth=2,
        padx=10,
    )
    stop_button.grid(row=0, column=1, padx=10)

    load_button = tk.Button(
        button_frame,
        text="Load History",
        command=load_existing_history,
        bg="#3498db",
        fg="white",
        font=("Arial", 12, "bold"),
        activebackground="#2980b9",
        activeforeground="white",
        relief="raised",
        borderwidth=2,
        padx=10,
    )
    load_button.grid(row=0, column=2, padx=10)

    # Scrollable frame for displaying clipboard history
    scrollable_frame_container = tk.Frame(root, bg="#ecf0f1")
    scrollable_frame_container.pack(fill="both", expand=True, pady=10, padx=10)

    # Create a canvas for the scrollable frame
    canvas = tk.Canvas(scrollable_frame_container, bg="#ecf0f1", highlightthickness=0)
    scrollbar = ttk.Scrollbar(scrollable_frame_container, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#ecf0f1")

    # Configure scrolling
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Pack canvas and scrollbar
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Start the GUI main loop
    root.mainloop()



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
import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
from pyzbar.pyzbar import decode

def scan_qr_from_image():
    def select_image():
        # Open file dialog to select an image file
        file_path = filedialog.askopenfilename(
            title="Select an Image File",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff")]
        )
        
        if not file_path:
            return
        
        try:
            # Read the image using OpenCV
            img = cv2.imread(file_path)
            decoded_objects = decode(img)

            if decoded_objects:
                results_text = "Data in QR Code:\n"
                for obj in decoded_objects:
                    results_text += f"{obj.data.decode('utf-8')}\n"
            else:
                results_text = "No QR code found in the image."
            
            # Display results in the results box
            results_box.delete(1.0, tk.END)
            results_box.insert(tk.END, results_text)

        except Exception as e:
            messagebox.showerror("Error", f"Error reading image: {e}")

    # Create the GUI application
    root = tk.Tk()
    root.title("QR Code Scanner from Image")
    root.geometry("500x400")
    root.configure(bg="#f5f5f5")

    # Title label
    title_label = tk.Label(
        root,
        text="QR Code Scanner",
        font=("Helvetica", 18, "bold"),
        fg="#2c3e50",
        bg="#f5f5f5",
        pady=10
    )
    title_label.pack()

    # Button to select image
    select_button = tk.Button(
        root,
        text="Select Image to Scan",
        font=("Helvetica", 12, "bold"),
        bg="#3498db",
        fg="white",
        activebackground="#2980b9",
        activeforeground="white",
        command=select_image,
        padx=10,
        pady=5
    )
    select_button.pack(pady=10)

    # Text box to show QR code result
    results_box = tk.Text(root, wrap=tk.WORD, width=60, height=10, font=("Arial", 12))
    results_box.pack(pady=20)

    # Run the GUI application
    root.mainloop()



# Function to display feature icons
def toggle_features():
    global icons, current_thread, current_feature

    # If icons are visible, hide them
    if icons:
        for icon in icons:
            icon.destroy()
        icons = []  # Clear the icons list
    
    else:
        # If icons are hidden, show them
        center_x = canvas.winfo_x() + 50
        center_y = canvas.winfo_y() + 50

        for i, feature in enumerate(FEATURES):
            angle = math.radians((360 / len(FEATURES)) * i)
            x = center_x + RADIUS * math.cos(angle)
            y = center_y + RADIUS * math.sin(angle)

            frame = tk.Frame(root, bg="white", highlightbackground="black", highlightthickness=1)
            frame.place(x=x-50, y=y-50, width=100, height=70)

            def on_enter(event, f=frame):
                f.config(bg="#000000")

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

            icons.append(frame)  # Add the frame to the icons list

# Add an Off button to stop the application


import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import time
import threading

def task_reminder():
    def set_reminder():
        task = task_entry.get()
        task_time = time_entry.get()

        if not task.strip() or not task_time.strip():
            messagebox.showwarning("Invalid Input", "Both Task and Time are required.")
            return

        try:
            task_time_obj = datetime.strptime(task_time, "%H:%M")
            current_time = datetime.now().strftime("%H:%M")

            # Add the task to the listbox
            tasks_listbox.insert(tk.END, f"{task} at {task_time}")

            # Convert the task time into a datetime object for comparison
            task_time_obj = task_time_obj.replace(year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)

            def remind():
                while True:
                    current_time_obj = datetime.now()
                    if current_time_obj >= task_time_obj:
                        messagebox.showinfo("Task Reminder", f"Time to do: {task}")
                        break
                    time.sleep(30)  # Check every 30 seconds

            reminder_thread = threading.Thread(target=remind)
            reminder_thread.daemon = True  # Run in the background
            reminder_thread.start()

            task_entry.delete(0, tk.END)
            time_entry.delete(0, tk.END)

        except ValueError:
            messagebox.showwarning("Invalid Time Format", "Please enter the time in HH:MM format.")

    # Create the GUI application
    root = tk.Tk()
    root.title("Task Reminder")
    root.geometry("400x400")
    root.configure(bg="#f7f7f7")

    # Title label
    title_label = tk.Label(
        root,
        text="Task Reminder",
        font=("Helvetica", 18, "bold"),
        fg="#2c3e50",
        bg="#f7f7f7",
        pady=10
    )
    title_label.pack()

    # Task input
    task_label = tk.Label(root, text="Task:", font=("Helvetica", 12), fg="#34495e", bg="#f7f7f7")
    task_label.pack(pady=5)
    task_entry = tk.Entry(root, font=("Helvetica", 14), width=25)
    task_entry.pack(pady=5)

    # Time input (HH:MM)
    time_label = tk.Label(root, text="Time (HH:MM):", font=("Helvetica", 12), fg="#34495e", bg="#f7f7f7")
    time_label.pack(pady=5)
    time_entry = tk.Entry(root, font=("Helvetica", 14), width=25)
    time_entry.pack(pady=5)

    # Set reminder button
    set_button = tk.Button(
        root,
        text="Set Reminder",
        font=("Helvetica", 12, "bold"),
        bg="#3498db",
        fg="white",
        activebackground="#2980b9",
        activeforeground="white",
        padx=10,
        pady=5,
        relief="raised",
        command=set_reminder
    )
    set_button.pack(pady=10)

    # Listbox to display tasks
    tasks_listbox = tk.Listbox(root, font=("Arial", 12), width=40, height=10)
    tasks_listbox.pack(pady=20)

    # Run the GUI application
    root.mainloop()


def turn_off_assistant():
    global current_thread, current_feature
    # Stop any running features
    if current_feature:
        stop_flags[current_feature['name']] = True
        print(f"Stopping {current_feature['name']} feature.")
    if current_thread and current_thread.is_alive():
        current_thread.join()  # Wait for the thread to finish
    
    # Exit the application
    root.destroy()
    print("Desktop Assistant turned off.")

# Create the Off button
off_button = tk.Button(
    root,
    text="Off",
    font=("Arial", 12),
    bg="red",
    fg="white",
    command=turn_off_assistant,
    width=10
)
off_button.place(x=10, y=10)  # Adjust position as needed

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