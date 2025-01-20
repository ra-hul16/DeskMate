import sys
import os
import pyttsx3
import keyboard
import pytesseract
import pyperclip
import qrcode
import webbrowser
from datetime import datetime
from PyQt5 import QtCore, QtGui, QtWidgets

class DesktopAssistant(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.task_list = []

    def init_ui(self):
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.resize(100, 100)

        self.circle_icon = QtWidgets.QPushButton(self)
        self.circle_icon.setGeometry(QtCore.QRect(0, 0, 100, 100))
        self.circle_icon.setStyleSheet("border-radius: 50px; background-color: #3498db;")
        self.circle_icon.clicked.connect(self.display_menu)

    def display_menu(self):
        menu = QtWidgets.QMenu(self)
        menu.addAction("Copy-Paste (20x)", self.copy_paste)
        menu.addAction("AI Voice Assistant", self.voice_assistant)
        menu.addAction("Keyboard Shortcut", self.keyboard_shortcut)
        menu.addAction("Terminal Shortcut", self.open_terminal)
        menu.addAction("Text Extraction", self.text_extraction)
        menu.addAction("QR Scanner", self.qr_scanner)
        menu.addAction("Grammar Correcter", self.grammar_corrector)
        menu.addAction("Personalized Newsfeed", self.personalized_newsfeed)
        menu.addAction("To Do List", self.to_do_list)
        menu.addAction("Task Reminder", self.task_reminder)
        menu.exec_(QtGui.QCursor.pos())

    def copy_paste(self):
        copied_text = pyperclip.paste()
        for _ in range(20):
            pyperclip.copy(copied_text)
            print(f"Pasted: {copied_text}")

    def voice_assistant(self):
        engine = pyttsx3.init()
        engine.say("Hello, I am your desktop assistant!")
        engine.runAndWait()

    def keyboard_shortcut(self):
        print("Press Ctrl+Alt+S to activate.")
        keyboard.add_hotkey('ctrl+alt+s', lambda: print("Shortcut activated"))

    def open_terminal(self):
        os.system("start cmd")

    def text_extraction(self):
        # Assuming an image for demonstration
        path_to_image = "sample_image.png"
        text = pytesseract.image_to_string(path_to_image)
        print(f"Extracted text: {text}")

    def qr_scanner(self):
        qr_code_data = "https://example.com"
        img = qrcode.make(qr_code_data)
        img.show()

    def grammar_corrector(self):
        input_text = "This is a simpl test for grammar corrector."
        corrected_text = input_text.replace("simpl", "simple")  # Simplified example
        print(f"Corrected text: {corrected_text}")

    def personalized_newsfeed(self):
        webbrowser.open("https://news.google.com")

    def to_do_list(self):
        print("Current To-Do List:")
        for task in self.task_list:
            print(f"- {task}")
        new_task = input("Add a new task: ")
        if new_task:
            self.task_list.append(new_task)

    def task_reminder(self):
        reminder = input("Set a reminder (HH:MM format): ")
        now = datetime.now().strftime("%H:%M")
        while now != reminder:
            now = datetime.now().strftime("%H:%M")
        print("Reminder: Time to check your tasks!")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    assistant = DesktopAssistant()
    assistant.show()
    sys.exit(app.exec_())
