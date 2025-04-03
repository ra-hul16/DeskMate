import cv2
from pyzbar.pyzbar import decode
import tkinter as tk
from tkinter import filedialog


def scan_qr_from_image():
    """Scan QR code from an image file selected via a dialog box."""
    print("Initializing Tkinter...")
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    print("Opening file dialog...")
    
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

def scan_qr_from_camera():
    """Scan QR code using the system camera."""
    cap = cv2.VideoCapture(0)  # 0 for default camera
    print("Press 'q' to quit the camera feed.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture video.")
            break

        decoded_objects = decode(frame)
        for obj in decoded_objects:
            data = obj.data.decode('utf-8')
            print(f"Data in QR Code: {data}")
            cv2.putText(frame, data, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("QR Code Scanner", frame)

        # Exit when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def main():
    print("QR Code Scanner")
    print("1. Scan QR code from an image file")
    print("2. Scan QR code using the camera")
    choice = input("Enter your choice (1 or 2): ")

    if choice == "1":
        scan_qr_from_image()
    elif choice == "2":
        scan_qr_from_camera()
    else:
        print("Invalid choice. Please enter 1 or 2.")


if __name__ == "__main__":
    main()