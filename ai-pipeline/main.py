"""AI pipeline service — FastAPI.

Faza 1: LangGraph pipeline (PDF → JSON → walidacja sumy kopii).
Aprobata (human-in-the-loop) happens at the API layer: /api/parse returns a
preview + validation report; ADMIN approves in the UI before persisting to
backend-spring. Faza 3: heurystyka planowania trasy.
"""
from fastapi import FastAPI, File, HTTPException, UploadFile

from graph import app_graph

app = FastAPI(title="ZeitungsZusteller AI Pipeline")


@app.get("/health")
def health() -> dict:
    return {"status": "UP", "service": "ai-pipeline"}


@app.post("/api/parse")
async def parse_pdf(file: UploadFile = File(...)) -> dict:
    """Parse a Tagesliste PDF into the product JSON structure.

    Returns miasto/rejon/dostawca/data, ulice[] with klienci[] in document
    (route) order, suma_gazet and walidacja (copy totals must match).
    """
    data = await file.read()
    if not data:
        raise HTTPException(status_code=400, detail="empty file")
    try:
        state = app_graph.invoke({"pdf_bytes": data})
    except Exception as exc:  # unreadable PDF / unexpected layout
        raise HTTPException(status_code=422, detail=f"parse failed: {exc}") from exc
    return state["result"]
