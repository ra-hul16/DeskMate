import inspect
import webbrowser
import tkinter as tk
from tkinter import messagebox

def function_finder():
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
            search_url = f"https://www.google.com/search?q=python+{func_name}+function"
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

    # Run GUI
    root.mainloop()

# Call the function to start the Function Finder app
function_finder()