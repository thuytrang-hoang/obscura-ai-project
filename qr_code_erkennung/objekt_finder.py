import cv2
import numpy as np
import os
import subprocess
import pickle
from tkinter import filedialog, Tk

"""Code mit Chat GPT generiert oder unterstützt"""
def bild_auswaehlen():
    root = Tk()
    root.withdraw()
    return filedialog.askopenfilename(
        title="Wähle ein Gesamtbild mit Barcode",
        filetypes=[("Bilddateien", "*.jpg *.jpeg *.png *.bmp")]
    )

def erweitere_und_schneide(bild, x, y, w, h, abstand=0.05):
    """Schneidet ein rechteckiges Objekt aus dem Bild basierend auf Konturenbox."""
    h_img, w_img = bild.shape[:2]
    dx = int(w * abstand)
    dy = int(h * abstand)
    x_neu = max(x - dx, 0)
    y_neu = max(y - dy, 0)
    x_max = min(x + w + dx, w_img)
    y_max = min(y + h + dy, h_img)
    return bild[y_neu:y_max, x_neu:x_max]

def finde_und_teste_regionen(bild):
    """
    Sucht im Bild nach möglichen rechteckigen Regionen, die QR-Codes enthalten könnten.
    Nutzt Konturenerkennung und Formfilterung.
    """
    grau = cv2.cvtColor(bild, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grau, (5, 5), 0)
    kanten = cv2.Canny(blur, 30, 100)

    konturen, _ = cv2.findContours(kanten, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print(f" Gefundene Konturen: {len(konturen)}")

    qr_detector = cv2.QRCodeDetector()

    for i, cnt in enumerate(konturen):
        x, y, w, h = cv2.boundingRect(cnt)
        seitenverh = max(w, h) / (min(w, h) + 1e-5)

        if seitenverh > 1.3 or min(w, h) < 30:
            continue

        region = erweitere_und_schneide(bild, x, y, w, h)
        cv2.imshow(f"Versuch {i+1}: mögliche QR-Region", region)
        cv2.waitKey(500)

        decoded, _, _ = qr_detector.detectAndDecode(region)
        if decoded:
            print(f" QR-Code erkannt: {decoded}")
            cv2.destroyAllWindows()
            return region

    cv2.destroyAllWindows()
    return None

def übergebe_an_erkennung(region):
    with open("temp_bild.pkl", "wb") as f:
        pickle.dump(region, f)
    subprocess.run(["python", "qr_code_auslese.py", "temp_bild.pkl"])

def main():
    bildpfad = bild_auswaehlen()
    if not bildpfad:
        print(" Kein Bild ausgewählt.")
        return

    bild = cv2.imread(bildpfad)
    if bild is None:
        print(" Bild konnte nicht geladen werden.")
        return

    region = finde_und_teste_regionen(bild)
    if region is not None:
        übergebe_an_erkennung(region)
    else:
        print(" Kein QR-Code erkannt.")

if __name__ == "__main__":
    main()
