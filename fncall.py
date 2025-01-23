import tkinter as tk
import math

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
    {"name": "Copy-Paste", "symbol": "📋", "function": lambda: copy_paste()},
    {"name": "Text Extraction", "symbol": "🔍", "function": lambda: text_extraction()},
    {"name": "QR Scanner", "symbol": "🕵️", "function": lambda: qr_scanner()},
    {"name": "To-Do List", "symbol": "🔄", "function": lambda: to_do_list()},
    {"name": "Task Reminder", "symbol": "⏑", "function": lambda: task_reminder()}
]

# Store feature icons
icons = []

# Define functionality for each feature
def copy_paste():
    print("Copy-Paste is selected")

def text_extraction():
    print("Text Extraction is selected")

def qr_scanner():
    print("QR Scanner is selected")

def to_do_list():
    print("To-Do List is selected")

def task_reminder():
    print("Task Reminder is selected")

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
