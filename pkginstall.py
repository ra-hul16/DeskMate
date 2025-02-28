import webbrowser
import tkinter as tk
from tkinter import messagebox
from googlesearch import search  # Import Google search module

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
    """Redirects user to the official download page of the package, or the top Google result if not found."""
    package_name = entry.get().strip().lower()  # Get user input
    
    if not package_name:
        messagebox.showwarning("Input Error", "Please enter a package name.")
        return
    
    if package_name in PACKAGE_URLS:
        url = PACKAGE_URLS[package_name]
        messagebox.showinfo("Redirecting", f"Opening {package_name} download page...")
        webbrowser.open(url)
    else:
        # If package is not found, fetch the first result from Google
        messagebox.showinfo("Searching", f"Package '{package_name}' not found. Searching for the best result...")
        
        try:
            search_query = f"{package_name} download"
            top_result = next(search(search_query, num=1, stop=1, pause=2))  # Get the first Google result
            messagebox.showinfo("Redirecting", f"Opening top result: {top_result}")
            webbrowser.open(top_result)
        except Exception as e:
            messagebox.showerror("Error", f"Could not fetch search results. Please try again manually.\nError: {e}")
            webbrowser.open(f"https://www.google.com/search?q={package_name}+download")  # Open Google search page as fallback

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

# Run the Tkinter event loop
root.mainloop()
