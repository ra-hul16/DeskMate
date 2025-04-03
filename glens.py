from tkinter import Tk, filedialog
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input, decode_predictions
import cv2
import pytesseract
import numpy as np

# Set up Tesseract OCR path (update this to your Tesseract installation path)
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\User\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

def select_image_file():
    """
    Opens a file dialog to select an image file.
    """
    root = Tk()
    root.withdraw()  # Hide the main Tkinter window
    file_path = filedialog.askopenfilename(
        title="Select an Image File",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
    )
    if not file_path:
        print("No file selected!")
        exit()
    return file_path

def detect_objects(image):
    """
    Detect objects in the image using the MobileNetV2 model.
    """
    print("Detecting objects...")
    # Load the pre-trained MobileNetV2 model
    model = MobileNetV2(weights="imagenet")
    
    # Preprocess the image
    resized_image = cv2.resize(image, (224, 224))  # Resize to match model input size
    img_array = preprocess_input(np.expand_dims(resized_image, axis=0))
    
    # Make predictions
    predictions = model.predict(img_array)
    labels = decode_predictions(predictions, top=3)  # Decode top-3 predictions
    
    print("Objects detected:")
    for label in labels[0]:
        print(f"Object: {label[1]}, Confidence: {label[2]:.2f}")
    
def extract_text(image):
    """
    Extract text from the image using Tesseract OCR.
    """
    print("Extracting text...")
    # Convert image to grayscale for better OCR results
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Perform OCR
    text = pytesseract.image_to_string(gray_image)
    
    print("Extracted Text:")
    print(text)

def main():
    """
    Main function to execute the Google Lens clone.
    """
    print("Select an image file:")
    image_path = select_image_file()  # Open file dialog to select an image
    image = cv2.imread(image_path)  # Read the selected image
    
    if image is None:
        print("Error: Could not read the image. Ensure the file is valid.")
        exit()
    
    detect_objects(image)  # Detect objects in the image
    extract_text(image)  # Extract text from the image

if __name__ == "__main__":
    main()
