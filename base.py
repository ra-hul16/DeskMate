from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt, QPropertyAnimation, QPoint
from PyQt5.QtGui import QColor
import sys
import math


class DeskMate(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Main window settings
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setGeometry(500, 300, 400, 400)
        self.setStyleSheet("background: transparent;")

        # Main Circle Button
        self.circle_btn = QPushButton(self)
        self.circle_btn.setGeometry(170, 170, 60, 60)  # Centered in the window
        self.circle_btn.setStyleSheet("""
            QPushButton {
                background: qradialgradient(
                    cx:0.5, cy:0.5, radius:0.5,
                    fx:0.5, fy:0.5,
                    stop:0 #4facfe, stop:1 #00f2fe
                );
                border: 2px solid white;
                border-radius: 30px;
            }
            QPushButton:hover {
                background: qradialgradient(
                    cx:0.5, cy:0.5, radius:0.5,
                    fx:0.5, fy:0.5,
                    stop:0 #00c6ff, stop:1 #0072ff
                );
            }
        """)
        self.circle_btn.clicked.connect(self.toggle_features)

        # Add shadow effect to the main circle
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setOffset(0, 0)
        shadow.setColor(QColor(0, 242, 254, 180))
        self.circle_btn.setGraphicsEffect(shadow)

        # Feature buttons
        self.features = [
            "Copy-Paste", "AI Assistant", "Shortcuts", "Terminal",
            "Text Extraction", "QR Scanner", "Grammar Check",
            "Newsfeed", "To-Do List", "Reminder"
        ]

        self.feature_buttons = []
        for feature in self.features:
            btn = QPushButton(self)
            btn.setGeometry(190, 190, 40, 40)  # Start hidden inside the main circle
            btn.setStyleSheet(f"""
                QPushButton {{
                    background: qradialgradient(
                        cx:0.5, cy:0.5, radius:0.5,
                        fx:0.5, fy:0.5,
                        stop:0 #ffd700, stop:1 #ffa500
                    );
                    border: 2px solid white;
                    border-radius: 20px;
                }}
                QPushButton:hover {{
                    background: qradialgradient(
                        cx:0.5, cy:0.5, radius:0.5,
                        fx:0.5, fy:0.5,
                        stop:0 #ffcc33, stop:1 #ff8800
                    );
                }}
            """)
            btn.setText(feature[:2])  # Optional: Use the first two letters for the label
            btn.setVisible(False)
            self.feature_buttons.append(btn)

        self.expanded = False  # To track whether features are expanded

        # Off Button
        self.off_btn = QPushButton("Off", self)
        self.off_btn.setGeometry(180, 350, 50, 30)  # Below the main circle
        self.off_btn.setStyleSheet("""
            QPushButton {
                background: #ff5555;
                color: white;
                border: 1px solid white;
                border-radius: 10px;
            }
            QPushButton:hover {
                background: #ff0000;
            }
        """)
        self.off_btn.clicked.connect(self.close_program)

    def toggle_features(self):
        if self.expanded:
            self.collapse_features()
        else:
            self.expand_features()

    def expand_features(self):
        # Positions for the smaller circles in a circular layout
        center_x, center_y = 200, 200  # Center of the main button
        radius = 120  # Distance from the main button
        num_features = len(self.feature_buttons)

        for i, btn in enumerate(self.feature_buttons):
            angle = (360 / num_features) * i  # Divide features evenly in a circle
            angle_rad = math.radians(angle)  # Convert to radians

            # Target position for the feature button
            target_x = center_x + radius * math.cos(angle_rad) - 20  # Adjust for button size
            target_y = center_y + radius * math.sin(angle_rad) - 20  # Adjust for button size

            # Animate the feature button to its target position
            btn.setVisible(True)
            anim = QPropertyAnimation(btn, b"pos")
            anim.setDuration(500)
            anim.setStartValue(QPoint(center_x - 20, center_y - 20))
            anim.setEndValue(QPoint(int(target_x), int(target_y)))
            anim.start()

        self.expanded = True

    def collapse_features(self):
        # Animate all feature buttons back to the center of the main button
        center_x, center_y = 200, 200  # Center of the main button
        for btn in self.feature_buttons:
            anim = QPropertyAnimation(btn, b"pos")
            anim.setDuration(500)
            anim.setEndValue(QPoint(center_x - 20, center_y - 20))
            anim.start()

            # Hide the button after the animation
            anim.finished.connect(lambda: btn.setVisible(False))

        self.expanded = False

    def close_program(self):
        QApplication.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    deskmate = DeskMate()
    deskmate.show()
    sys.exit(app.exec_())
