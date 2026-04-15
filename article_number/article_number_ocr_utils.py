import requests
import base64
import json

"""
This class is used to connect to the Roboflow cloud API for object detection.

It encodes a local image in base64 format, sends it to the Roboflow project
trained to detect article numbers, and extracts the predicted objects from
the response.

Although this API version was helpful during early development, it was later
replaced by a local YOLOv5 model to ensure offline functionality. This script
remains as an optional tool for testing and comparing results between
cloud-based and offline predictions.
"""

# Roboflow configuration
ROBOFLOW_API_KEY = "2yivUMg84cLeKBKwtgFy"
MODEL = "artikelnummererkennung"   # Model name from the Roboflow dashboard
VERSION = "6"                      # Model version

def extract_text_and_serial(image_path):
    # Convert the image to base64 format
    with open(image_path, "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode("utf-8")

    # Prepare and send the POST request to the Roboflow API
    url = f"https://detect.roboflow.com/{MODEL}/{VERSION}?api_key={ROBOFLOW_API_KEY}"
    response = requests.post(
        url,
        files={"file": image_base64},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    # Handle errors in the API response
    if response.status_code != 200:
        return "Fehler bei Roboflow", None

    # Parse the API response
    result = response.json()
    predictions = result.get("predictions", [])

    # Collect detected article numbers
    artikelnummern = []
    for pred in predictions:
        if pred.get("class") == "Artikelnummer":
            artikelnummern.append(pred.get("class")) 

    # Return the first valid article number (if any)
    best_guess = artikelnummern[0] if artikelnummern else None

    return json.dumps(result, indent=2), best_guess
