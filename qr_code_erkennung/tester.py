import subprocess
import pickle
import cv2
import os
from tkinter import filedialog, Tk
import sys

"""
tester.py
Interaktive Testumgebung zur Validierung:
1. Manuelle Auswahl erkannter QR-Code-Regionen
2. Objektfinder-Test: Automatische Prüfung erkannter Regionen mit Benutzerrückmeldung (Y/N)
3. Vollautomatische Prüfung aller Regionen inkl. Rotation
"""

"""Code mit Chat GPT generiert oder unterstützt"""

def bild_auswaehlen(titel="Wähle ein Bild"):
    root = Tk()
    root.withdraw()
    root.call('wm', 'attributes', '.', '-topmost', True)
    pfad = filedialog.askopenfilename(
        title=titel,
        filetypes=[("Bilddateien", "*.jpg *.jpeg *.png *.bmp")]
    )
    root.destroy()
    return pfad

def starte_barcode_erkennung(temp_datei):
    print(f"\n Starte qr_code_auslese.py mit: {temp_datei}")
    subprocess.run([sys.executable, "qr_code_auslese.py", temp_datei])

def manueller_test():
    print("\n Manueller Test: QR-Code direkt übergeben")
    pfad = bild_auswaehlen("Wähle ein zugeschnittenes QR-Code-Bild")
    if not pfad:
        print(" Kein Bild gewählt.")
        return

    bild = cv2.imread(pfad)
    if bild is None:
        print(" Bild konnte nicht geladen werden.")
        return

    with open("temp_bild.pkl", "wb") as f:
        pickle.dump(bild, f)

    starte_barcode_erkennung("temp_bild.pkl")

def objektfinder_test():
    print("\n Test: Gesamtbild mit objekt_finder.py analysieren")
    pfad = bild_auswaehlen("Wähle ein Gesamtbild (z. B. Schaltschrank)")
    if not pfad:
        print(" Kein Bild gewählt.")
        return

    subprocess.run([sys.executable, "objekt_finder.py", pfad])

def automatischer_test():
    print("\n Vollautomatischer Test mit Rotation")
    pfad = bild_auswaehlen("Wähle ein Gesamtbild für vollautomatische Regionenanalyse")
    if not pfad:
        print(" Kein Bild gewählt.")
        return

    subprocess.run([sys.executable, "objekt_finder.py", pfad, "--auto"])

if __name__ == "__main__":
    print("=== TESTMODUS ===")
    print("1. Manueller Test (direktes QR-Bild)")
    print("2. Objektfinder-Test (Regionen prüfen mit Benutzerwahl)")
    print("3. Vollautomatischer Regionentest (Rotation und QR-Code-Erkennung)")

    wahl = input(" Bitte wähle 1, 2 oder 3: ")

    if wahl == "1":
        manueller_test()
    elif wahl == "2":
        objektfinder_test()
    elif wahl == "3":
        automatischer_test()
    else:
        print(" Ungültige Auswahl.")
