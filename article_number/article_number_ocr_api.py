from fastapi import FastAPI, Request
import base64
import os
from article_number_ocr_utils import extract_text_and_serial

"""
This FastAPI application provides an endpoint for article number recognition from images.

It receives an image (base64-encoded) and a related identifier ("schrank") via a POST request.
The image is decoded, saved locally, and passed to the OCR pipeline. The extracted article
number and full OCR text are returned in the response.

Used for integration with external tools like PowerApps to automatically process uploaded images.
"""

# Initialize FastAPI app
app = FastAPI()

# Define POST endpoint for image analysis
@app.post("/analyze")
async def analyze(request: Request):
    # Extract JSON data from request
    data = await request.json()
    image_base64 = data.get("image")
    schrank = data.get("schrank")

    # Remove base64 prefix if it exists 
    if "," in image_base64:
        image_base64 = image_base64.split(",")[1]

    # Create folder if it doesn't exist
    os.makedirs("saved_images", exist_ok=True)
    filename = f"saved_images/{schrank}.png"

    # Decode base64 image and save it as a file
    with open(filename, "wb") as f:
        f.write(base64.b64decode(image_base64))

    # Run OCR and extract article number from the saved image
    text, artikelnummer = extract_text_and_serial(filename)

    # Return the results to the client
    return {
        "message": "Bild analysiert",
        "schrank": schrank,
        "text": text,
        "artikelnummer": artikelnummer
    }
