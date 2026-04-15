import cv2
from tkinter import Tk, filedialog
from barcode_erkennung import fake_barcode_erkennung

"""
main.py
Simpler Einstiegspunkt zur Barcode-Simulation.
Bildauswahl → Fake-Erkennung → Ausgabe in Konsole.

Dieses Skript ist Teil eines Prototyps zur visuellen Erkennung von Bauteilen mit Barcodes.
Ziel: Bild → Barcode extrahieren → Ausgabe in PowerApps und Excel.
Aktuell: Nur Fake-Daten, echte Erkennung folgt.

"""

"""Code mit Chat GPT generiert oder unterstützt"""

def lade_bild(pfad):
    """Lädt das Bild aus dem angegebenen Pfad mit OpenCV."""
    return cv2.imread(pfad)

def bild_auswaehlen():
    """Öffnet ein Dialogfenster zur Bildauswahl."""
    root = Tk()
    root.withdraw()
    return filedialog.askopenfilename(
        title="Wähle ein Bild mit QR-/Barcode",
        filetypes=[("Bilddateien", "*.jpg *.jpeg *.png *.bmp")]
    )

def main():
    pfad = bild_auswaehlen()
    if not pfad:
        return

    bild = lade_bild(pfad)
    if bild is None:
        return

    inhalt = fake_barcode_erkennung(bild)
    if inhalt:
        print(f"GS1 Code gefunden: {inhalt}")

if __name__ == "__main__":
    main()