"""LangGraph orchestration for the Tagesliste import (requirement F1).

Stages:
    extract  — PDF bytes -> layout-mode page texts (pypdf)
    parse    — deterministic state machine -> product JSON structure
    validate — copy totals vs document header and 'Summe' block

Human-in-the-loop approval lives at the API layer, not inside the graph:
POST /api/parse returns a preview with the validation report; the ADMIN
approves it in the UI before it is persisted to backend-spring. This keeps
the graph pure (no I/O beyond the PDF) and trivially testable.
"""
from __future__ import annotations

import io
from typing import TypedDict

from langgraph.graph import END, START, StateGraph
from pypdf import PdfReader

from tagesliste_parser import parse_tagesliste_text


class ParseState(TypedDict):
    pdf_bytes: bytes
    pages: list[str]
    result: dict


def extract(state: ParseState) -> dict:
    """PDF bytes -> layout-mode text per page (column positions preserved)."""
    reader = PdfReader(io.BytesIO(state["pdf_bytes"]))
    return {
        "pages": [page.extract_text(extraction_mode="layout") or "" for page in reader.pages]
    }


def parse(state: ParseState) -> dict:
    """Layout texts -> product JSON (streets/customers in document order)."""
    return {"result": parse_tagesliste_text(state["pages"])}


def build_graph():
    graph = StateGraph(ParseState)
    graph.add_node("extract", extract)
    graph.add_node("parse", parse)  # validation runs inside the parser (single source of truth)
    graph.add_edge(START, "extract")
    graph.add_edge("extract", "parse")
    graph.add_edge("parse", END)
    return graph.compile()


app_graph = build_graph()
