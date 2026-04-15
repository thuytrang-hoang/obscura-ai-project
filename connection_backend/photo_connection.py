from fastapi import FastAPI, Request
import base64
import os
from baugruppen_label_recognition.baugruppen_detector import BaugruppenDetector
from article_number.run_roboflow_test import detect_article_text
from qr_code_erkennung.qr_code_auslese import fake_barcode_erkennung  

# Teile dieses Codes wurden mit Unterstützung von ChatGPT entwickelt.

app = FastAPI()
baugruppe = BaugruppenDetector()

@app.post("/analyze")
async def analyze(request: Request):
    data = await request.json()
    image_base64 = data.get("image")
    schrank = data.get("schrank")

    print(f"Bild empfangen für Schrank: {schrank}")

    # Entferne Base64-Header
    if "," in image_base64:
        image_base64 = image_base64.split(",")[1]

    # Ordner erstellen, falls nicht vorhanden
    os.makedirs("saved_images", exist_ok=True)
    filename = f"saved_images/{schrank}.png"

    # Speichere Bild
    with open(filename, "wb") as f:
        f.write(base64.b64decode(image_base64))

    # 1. Baugruppenbezeichnung
    baugruppe_detector = BaugruppenDetector()
    baugruppen_words = baugruppe_detector.analyze_image(filename)

    # 2. Artikelnummer
    artikelnummern_text = detect_article_text(filename)

    # 3. Barcode
    barcode = fake_barcode_erkennung(filename)

    print("Baugruppen:", baugruppen_words)
    print("Artikelnummer:", artikelnummern_text)
    print("Barcode:", barcode)
    
    
    return {
    "message": "Bild erhalten und gespeichert",
    "schrank": schrank,
    "baugruppenbezeichnungen": baugruppen_words,
    "artikelnummer_text": artikelnummern_text,
    "barcode": barcode
}

