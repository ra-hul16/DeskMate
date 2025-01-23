import tkinter as tk
from tkinter import messagebox

def open_to_do_list():
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

# Example usage (Test it independently)
if __name__ == "__main__":
    root = tk.Tk()
    root.title("To-Do List Example")
    root.geometry("200x100")

    open_button = tk.Button(root, text="Open To-Do List", command=open_to_do_list, width=20)
    open_button.pack(pady=20)

    root.mainloop()
