import sys
import os
from article_number_ocr_utils import extract_text_and_serial

"""
This script allows command-line testing of the OCR pipeline for article number recognition.

It accepts an image path as input, runs the article number detection using the extract_text_and_serial()
function (which may use Roboflow or a local model), and prints the full OCR result as well as
the best-matching article number.

Useful for manual testing and debugging outside the main application.
"""

# Check if an image path was passed as a command-line argument
if len(sys.argv) < 2:
    print("No image file provided. Please call this script with a file path.")
    sys.exit(1)

image_path = sys.argv[1]

# Verify that the provided file exists
if not os.path.exists(image_path):
    print(f"File not found: {image_path}")
    sys.exit(1)

# Call the OCR function to analyze the image
text, serial = extract_text_and_serial(image_path)

# Output the full recognized text
print("Full OCR Text:\n", text)

# Output the best-matched article number (if any)
print("\nDetected Article Number:")
print(f"Found: {serial}" if serial else "None found.")
