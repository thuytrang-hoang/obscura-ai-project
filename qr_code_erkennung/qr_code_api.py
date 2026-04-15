from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
"""
qr_code_api.py
Ein minimalistischer FastAPI-Server, der eine gefälschte Barcode-Antwort simuliert.

Verwendung:
- GET /barcode gibt eine statische Testnummer aus
- Dient zur Simulation der Verbindung mit PowerApps

Wird durch ngrok getunnelt, um extern erreichbar zu sein.
"""

app = FastAPI()

@app.get("/barcode")
async def barcode():
    fake_code = "12345678"
    return {"barcode": fake_code}
    """Simulierter Endpunkt für Barcode-Abruf – Rückgabe eines Dummy-Codes."""
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
