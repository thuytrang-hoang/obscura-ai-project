from roboflow import Roboflow
from PIL import Image
import pytesseract
import os

"""
This script performs article number recognition by combining Roboflow's object detection 
with local OCR using Tesseract.

It loads a test image, sends it to a trained Roboflow model to detect bounding boxes 
around article numbers, and applies Tesseract OCR to each detected region to extract text.

This hybrid approach allows accurate localization via Roboflow and detailed text recognition 
via Tesseract. Recognition works best with high-quality, properly oriented images.
"""


# Tesseract path (lokal installation)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Roboflow Setup
rf = Roboflow(api_key="2yivUMg84cLeKBKwtgFy")  # API-Key for Roboflow
project = rf.workspace("softwareentwicklungsprojekt").project("artikelnummererkennung")
model = project.version(6).model

def detect_article_text(image_path):
    image = Image.open(image_path)
    prediction = model.predict(image_path, confidence=0.05).json()

    texts = []
    for i, obj in enumerate(prediction["predictions"]):
        x, y = obj["x"], obj["y"]
        w, h = obj["width"], obj["height"]
        left = int(x - w / 2)
        top = int(y - h / 2)
        right = int(x + w / 2)
        bottom = int(y + h / 2)
        cropped = image.crop((left, top, right, bottom))
        text = pytesseract.image_to_string(cropped, lang="deu").strip()
        texts.append(text)
    return texts

