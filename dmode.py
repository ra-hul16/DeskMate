import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
import webbrowser
import psutil
import time
import threading
import random
import os
import tkinter as tk
from tkinter import messagebox
import time
import threading
from tkinter import PhotoImage
import random
import ctypes
from ctypes import wintypes
import subprocess
import inspect
class DeveloperHelperApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Developer Mode")
        self.geometry("800x500")
        self.configure(bg="#1e1e2f")
        self.attributes('-alpha', 0.95)  # Transparency
        self.create_widgets()

    def create_widgets(self):
        # Container frame for floating box
        container = tk.Frame(self, bg="#252540", bd=2, relief="groove")
        container.place(x=20, y=20, width=200, height=460)

        # Navigation buttons in the floating box
        button_colors = {'bg': '#3e3e5c', 'fg': '#ffffff', 'activebackground': '#5e5e7f'}
        btn_package_installer = tk.Button(container, text="Package Installer", command=self.package_installer, **button_colors)
        btn_package_installer.pack(pady=10, fill='x')
        
        btn_function_finder = tk.Button(container, text="Function Finder", command=self.function_finder, **button_colors)
        btn_function_finder.pack(pady=10, fill='x')
        
        btn_break_reminder = tk.Button(container, text="Break Reminder", command=self.break_reminder, **button_colors)
        btn_break_reminder.pack(pady=10, fill='x')
        
        btn_code_snippet = tk.Button(container, text="Edit Environment Variable", command=self.edit_sysenv, **button_colors)
        btn_code_snippet.pack(pady=10, fill='x')
        
        btn_system_info = tk.Button(container, text="Moniter Setup", command=self.moniter_setup, **button_colors)
        btn_system_info.pack(pady=10, fill='x')
        
        btn_motivation = tk.Button(container, text="Motivation Booster", command=self.motivation_booster, **button_colors)
        btn_motivation.pack(pady=10, fill='x')

        btn_open_cmd = tk.Button(container, text="Open Command Prompt", command=self.open_cmd, **button_colors)
        btn_open_cmd.pack(pady=10, fill='x')

    # 1. Package Installer Redirector
    def package_installer(self):
        """Creates a GUI to redirect users to official package download pages."""

    # Dictionary of common software packages and their official download pages
        PACKAGE_URLS = {
            "python": "https://www.python.org/downloads/",
            "java": "https://www.oracle.com/java/technologies/javase-downloads.html",
            "nodejs": "https://nodejs.org/en/download/",
            "mysql": "https://dev.mysql.com/downloads/",
            "postgresql": "https://www.postgresql.org/download/",
            "mongodb": "https://www.mongodb.com/try/download/community",
            "git": "https://git-scm.com/downloads",
            "docker": "https://www.docker.com/get-started/",
            "vscode": "https://code.visualstudio.com/download",
            "chrome": "https://www.google.com/chrome/",
            "firefox": "https://www.mozilla.org/en-US/firefox/new/",
            "notepad++": "https://notepad-plus-plus.org/downloads/",
            "virtualbox": "https://www.virtualbox.org/wiki/Downloads",
            "intellij": "https://www.jetbrains.com/idea/download/",
            "androidstudio": "https://developer.android.com/studio",
        }

        def open_package_website():
            """Redirects user to the official download page of the package or searches on Google."""
            package_name = entry.get().strip().lower()

            if not package_name:
                messagebox.showwarning("Input Error", "Please enter a package name.")
                return

            if package_name in PACKAGE_URLS:
                url = PACKAGE_URLS[package_name]
                messagebox.showinfo("Redirecting", f"Opening {package_name} download page...")
                webbrowser.open(url)
            else:
                # If package is not found, search on Google
                messagebox.showinfo("Searching", f"Package '{package_name}' not found. Searching on Google...")
                url = f'https://pypi.org/project/{package_name}/'
                webbrowser.open(url)
                # search_url = f"https://www.google.com/search?q={package_name}+download"
                # webbrowser.open(search_url)

        # Create GUI window
        root = tk.Tk()
        root.title("Package Installer Redirector")
        root.geometry("400x200")

        # Label
        label = tk.Label(root, text="Enter the package name:", font=("Arial", 12))
        label.pack(pady=10)

        # Input field
        entry = tk.Entry(root, width=40, font=("Arial", 12))
        entry.pack(pady=5)

        # Button to search for package
        download_button = tk.Button(root, text="Download", font=("Arial", 12), command=open_package_website)
        download_button.pack(pady=10)


    # 2. Python Function Finder
    def function_finder(self):
        """Creates a GUI to find the definition of a Python function."""

        def get_function_info():
            """Retrieves function definition and shows in a popup."""
            func_name = entry.get().strip()

            if not func_name:
                messagebox.showwarning("Input Error", "Please enter a function name.")
                return

            try:
                func_obj = eval(func_name)  # Get function object
                doc = inspect.getdoc(func_obj)  # Get documentation

                if doc:
                    messagebox.showinfo(f"Definition of '{func_name}'", doc)
                else:
                    messagebox.showinfo(f"Definition of '{func_name}'", "No documentation available.")
            except (NameError, SyntaxError):
                messagebox.showwarning("Not Found", f"Function '{func_name}' not found. Opening Google search...")
                
                #search_url = f"https://www.google.com/search?q=python+{func_name}+function"
                search_url = f'https://docs.python.org/3/search.html?q={func_name}'
                webbrowser.open(search_url)

        # Create GUI
        root = tk.Tk()
        root.title("Python Function Finder")
        root.geometry("400x200")

        # Label
        label = tk.Label(root, text="Enter a function name:", font=("Arial", 12))
        label.pack(pady=10)

        # Entry field
        entry = tk.Entry(root, width=30, font=("Arial", 12))
        entry.pack(pady=5)

        # Button
        search_button = tk.Button(root, text="Find Definition", font=("Arial", 12), command=get_function_info)
        search_button.pack(pady=10)


    # 3. Break Reminder
    def break_reminder(self):
        class LASTINPUTINFO(ctypes.Structure):
            _fields_ = [('cbSize', wintypes.UINT), ('dwTime', wintypes.DWORD)]

        def get_idle_duration():
            lii = LASTINPUTINFO()
            lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
            if ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii)):
                millis = ctypes.windll.kernel32.GetTickCount() - lii.dwTime
                return millis / 1000.0
            return 0.0

        # Break Reminder Application
        class BreakReminderApp(tk.Tk):
            def __init__(self):
                super().__init__()
                self.title("Break Reminder")
                self.geometry("500x400")
                self.configure(bg="#f0f0f0")
                self.reminder_interval = 60 * 60
                self.is_running = False
                self.start_time = time.time()
                self.total_screen_time = 0
                self.last_break_time = time.time()
                self.break_types = {
                    "Coffee Break ☕": ("Take a coffee break!", "coffee.png"),
                    "Stretch Muscles 🚶": ("Time to stretch your muscles!", "stretch.png"),
                    "Lunch Break 🍲": ("Enjoy your lunch!", "lunch.png"),
                    "Rest Eyes 👀": ("Give your eyes some rest!", "rest.png"),
                    "Hydrate 💧": ("Drink some water!", "water.png"),
                    "Screen Time Over ⏰": ("Take a break from the screen!", "screen.png")
                }
                self.selected_breaks = list(self.break_types.keys())
                self.create_widgets()

            def create_widgets(self):
                self.interval_label = tk.Label(self, text="Set Break Interval (minutes):", bg="#f0f0f0")
                self.interval_label.pack(pady=10)
                self.interval_entry = tk.Entry(self)
                self.interval_entry.insert(0, "60")
                self.interval_entry.pack(pady=5)

                self.checkbuttons = {}
                self.selected_breaks = []
                tk.Label(self, text="Select Break Types:", bg="#f0f0f0").pack(pady=5)
                for break_type in self.break_types.keys():
                    var = tk.BooleanVar(value=True)
                    chk = tk.Checkbutton(self, text=break_type, variable=var, bg="#f0f0f0")
                    chk.pack(anchor='w')
                    self.checkbuttons[break_type] = var

                self.start_button = tk.Button(self, text="Start Reminder", command=self.start_reminder, bg="#4caf50", fg="white")
                self.start_button.pack(pady=10)
                self.stop_button = tk.Button(self, text="Stop Reminder", command=self.stop_reminder, bg="#f44336", fg="white")
                self.stop_button.pack(pady=5)

                self.image_label = tk.Label(self)
                self.image_label.pack(pady=10)

                self.screen_time_label = tk.Label(self, text="", bg="#f0f0f0")
                self.screen_time_label.pack(pady=5)
                self.last_break_label = tk.Label(self, text="", bg="#f0f0f0")
                self.last_break_label.pack(pady=5)

                self.update_time_labels()

            def start_reminder(self):
                try:
                    interval_minutes = int(self.interval_entry.get())
                    self.reminder_interval = interval_minutes * 60
                    self.is_running = True
                    self.last_break_time = time.time()
                    self.selected_breaks = [k for k, v in self.checkbuttons.items() if v.get()]
                    if not self.selected_breaks:
                        messagebox.showerror("No Breaks Selected", "Please select at least one break type.")
                        return
                    threading.Thread(target=self.run_reminder, daemon=True).start()
                except ValueError:
                    messagebox.showerror("Invalid Input", "Please enter a valid number.")

            def stop_reminder(self):
                self.is_running = False

            def run_reminder(self):
                while self.is_running:
                    time.sleep(self.reminder_interval)
                    if not self.is_running:
                        break
                    self.show_reminder()

            def show_reminder(self):
                break_type = random.choice(self.selected_breaks)
                message, image_file = self.break_types[break_type]
                messagebox.showinfo("Break Reminder", message)
                self.total_screen_time += time.time() - self.last_break_time
                self.last_break_time = time.time()
                try:
                    photo = PhotoImage(file=image_file)
                    self.image_label.config(image=photo)
                    self.image_label.image = photo
                except Exception as e:
                    print(f"Error loading image: {e}")

            def update_time_labels(self):
                idle_time = get_idle_duration()
                screen_time = self.total_screen_time + (time.time() - self.start_time - idle_time)
                last_break = time.time() - self.last_break_time
                self.screen_time_label.config(text=f"Total Screen Time: {int(screen_time // 60)} min {int(screen_time % 60)} sec")
                self.last_break_label.config(text=f"Time Since Last Break: {int(last_break // 60)} min {int(last_break % 60)} sec")
                self.after(1000, self.update_time_labels)
        app = BreakReminderApp()

    # 4. Code Snippet Library
    def edit_sysenv(self):
        """Opens the Edit Environment Variables window."""
        subprocess.run([r"C:\Windows\System32\SystemPropertiesAdvanced.exe"])

    # 5. System Information
    def moniter_setup(self):
        #info += f"Disk Usage: {psutil.disk_usage(r'C:\\').percent}%"
        # info = f"CPU Usage: {psutil.cpu_percent()}%\n"
        # info += f"Memory Usage: {psutil.virtual_memory().percent}%\n"
        # info += f"Disk Usage: {psutil.disk_usage('C:\\').percent}%"
        # info = ""
        # info += f"CPU Usage: {psutil.cpu_percent()}%\n"
        # info += f"Memory Usage: {psutil.virtual_memory().percent}%\n"
        # info += f"Disk Usage: {psutil.disk_usage(r'C:\\').percent}%"
        subprocess.run(["start", "ms-settings:display"], shell=True)

    # 6. Motivation Booster
    def motivation_booster(self):
        quotes = [
            "Keep pushing forward!",
            "You can do it!",
            "Believe in yourself!",
            "Every step counts!",
            "Success is within reach!"
        ]
        messagebox.showinfo("Motivation Booster", random.choice(quotes))

    # 7. Open Command Prompt
    def open_cmd(self):
        os.system('start cmd')

if __name__ == '__main__':
    app = DeveloperHelperApp()
    app.mainloop()
