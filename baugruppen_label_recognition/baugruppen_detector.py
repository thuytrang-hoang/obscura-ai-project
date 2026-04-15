from roboflow import Roboflow
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

class BaugruppenDetector:
    def __init__(self):
        rf = Roboflow(api_key="Ync40EHPtNWLLQmTc8ff")
        project = rf.workspace("obscurabaugruppe").project("baugruppen-labels")
        self.model = project.version(3).model

    def analyze_image(self, image_path):
        image = Image.open(image_path)
        prediction = self.model.predict(image_path, confidence=0.35).json()

        # OCR für jedes Objekt
        words = []
        for obj in prediction["predictions"]:
            x, y, width, height = obj["x"], obj["y"], obj["width"], obj["height"]
            cropped = image.crop((x - width / 2, y - height / 2, x + width / 2, y + height / 2))
            text = pytesseract.image_to_string(cropped).strip()
            if text:
                words.append(text)
        return words