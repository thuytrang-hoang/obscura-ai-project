import cv2
import numpy as np
import requests
from tkinter import filedialog, Tk

"""Code mit Chat GPT generiert oder unterstützt"""

def bild_auswaehlen():
    root = Tk()
    root.withdraw()
    return filedialog.askopenfilename(
        title="Wähle ein QR-Code-Bild",
        filetypes=[("Bilddateien", "*.jpg *.jpeg *.png *.bmp")]
    )

def zxing_online_decode(image_array):
    _, buffer = cv2.imencode(".png", image_array)
    files = {"f": ("image.png", buffer.tobytes(), "image/png")}
    response = requests.post("https://zxing.org/w/decode", files=files)
    if response.ok:
        html = response.text
        start = html.find("<pre>") + 5
        end = html.find("</pre>")
        if start != -1 and end != -1:
            text = html[start:end].strip()
            cleaned = ''.join(c for c in text if ord(c) >= 32)
            return cleaned
    return None

def rotate_image(image, angle):
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, matrix, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    return rotated
"""Dreht das übergebene Bild um den angegebenen Winkel."""

def main():
    pfad = bild_auswaehlen()
    if not pfad:
        print(" Kein Bild ausgewählt.")
        return

    bild = cv2.imread(pfad)
    if bild is None:
        print(" Bild konnte nicht geladen werden.")
        return

    print(" Starte Winkelschleife (-10° bis +10° in 0.5er Schritten)...")

    for winkel in np.arange(-10, 10.5, 0.5):
        gedreht = rotate_image(bild, winkel)
        print(f" Teste Winkel: {winkel:.1f}°")

        # Bild anzeigen
        cv2.imshow(f"QR bei {winkel:.1f}°", gedreht)
        cv2.waitKey(300)  # 300 ms anzeigen
        cv2.destroyAllWindows()

        inhalt = zxing_online_decode(gedreht)
        if inhalt:
            print(f"\n Erkannt bei {winkel:.1f}°:\n{inhalt}")
            cv2.imshow(f" Erkannt bei {winkel:.1f}°", gedreht)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            return

    print(" Kein QR-Code erkannt in der Winkelschleife.")
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
