import sys
import pickle
"""
qr_code_auslese.py
Modul zur Erkennung von Barcodes (aktuell nur Fake-Modus aktiviert).
Später für echte Dekodierung (ZXing).
"""

"""Code mit Chat GPT generiert oder unterstützt"""
# ==== Konfiguration ====
USE_FAKE = True  #  Wechsle zu False, wenn echte Erkennung verfügbar ist

# === FAKE-Barcode-Erkennung (Dummy-Daten) ===
def fake_barcode_erkennung(bild):
    """Platzhalter-Funktion – gibt eine simulierte GS1-Barcode-Zahl zurück."""
    print(" (Fake-Modus) Barcode-Erkennung simuliert...")
    return "]C1800440612340000000000000003000176"

# === GS1-Code-Parsing ===
def parse_gs1(code):
    print("\n GS1 Parsing:")
    if "]C1" in code:
        code = code.replace("]C1", "")
    if code.startswith("80044061"):
        print("  (01) GTIN (Artikelnummer):", code[:18])
        print("  (30) Unbekannter AI:", code[18:])
    else:
        print("Kein GS1-Muster erkannt. Rohdaten:")
        print(code)

# === Barcode-Erkennung mit Rotation (nur Fake hier) ===
def winkel_schleife_decode(bild, anzeigen=False):
    print(" Starte Winkelschleife (Fake)...")
    for winkel in range(-5, 6):
        print(f" Drehe Bild um {winkel}°... (Simuliert)")
        # Statt echter Rotation: direkt Fake-Rückgabe
        inhalt = fake_barcode_erkennung(bild)
        if inhalt:
            print(f" Erkannt bei Rotation {winkel}°: {inhalt}")
            return inhalt
    print(" Kein Code erkannt in Winkelschleife.")
    return None

# === Direktaufruf durch pickle-Datei ===
def main():
    if len(sys.argv) < 2:
        print(" Keine Datei übergeben.")
        return

    pfad = sys.argv[1]
    print(f"\n Starte qr_code_auslese.py mit: {pfad}")

    try:
        with open(pfad, "rb") as f:
            bild = pickle.load(f)
    except Exception as e:
        print(f" Fehler beim Laden der Bilddatei: {e}")
        return

    if USE_FAKE:
        print(" Verwende FAKE-Barcoderkennung...")
        inhalt = fake_barcode_erkennung(bild)
    else:
        print(" Verwende ZXing oder andere Methoden (nicht aktiv)...")
        inhalt = None  # Platzhalter

    if inhalt:
        print(f"\n Erkannt:\n {inhalt}")
        parse_gs1(inhalt)
    else:
        print(" Kein Barcode erkannt.")

# === Export für Aufrufe aus tester.py ===
def übergebe_an_erkennung(bild):
    return fake_barcode_erkennung(bild) if USE_FAKE else None

def übergebe_mit_winkel(bild, anzeigen=True):
    return winkel_schleife_decode(bild, anzeigen=anzeigen)

if __name__ == "__main__":
    main()
