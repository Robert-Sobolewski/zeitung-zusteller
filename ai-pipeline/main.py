"""AI pipeline service — FastAPI.

Faza 1: LangGraph pipeline (PDF → JSON → walidacja → aprobata).
Faza 3: heurystyka planowania trasy.
"""
from fastapi import FastAPI

app = FastAPI(title="ZeitungsZusteller AI Pipeline")


@app.get("/health")
def health() -> dict:
    return {"status": "UP", "service": "ai-pipeline"}
