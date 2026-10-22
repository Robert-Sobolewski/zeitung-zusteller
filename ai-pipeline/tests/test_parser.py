"""Parser tests against the real Tagesliste PDFs (read-only; never committed).

Run from ai-pipeline/:  python -m pytest tests/ -v
"""
from __future__ import annotations

import io
from pathlib import Path

import pytest
from pypdf import PdfReader

from graph import app_graph
from tagesliste_parser import parse_tagesliste_text

REAL_DATA = Path(__file__).resolve().parent.parent.parent / "real-data" / "roberto_bz"


def _parse_file(name: str) -> dict:
    pdf_path = REAL_DATA / name
    reader = PdfReader(str(pdf_path))
    pages = [p.extract_text(extraction_mode="layout") or "" for p in reader.pages]
    return parse_tagesliste_text(pages)


@pytest.mark.parametrize(
    ("fname", "bezirk", "total"),
    [
        ("8019_21.10.2026.pdf", "8019", 84),
        ("8031_21.10.2026.pdf", "8031", 37),
        ("8094_21.10.2026.pdf", "8094", 54),
        ("8118_21.10.2026.pdf", "8118", 35),
    ],
)
def test_totals_match_document(fname: str, bezirk: str, total: int) -> None:
    """Computed copy totals must equal the document's stated totals (header + Summe block)."""
    result = _parse_file(fname)

    assert result["rejon"] == bezirk
    assert result["data"] == "21.10.2026"
    assert result["dostawca"] == "Robert Sobolewski"
    assert result["miasto"], "city must be extracted from the header table"

    walidacja = result["walidacja"]
    assert walidacja["status"] == "OK", f"validation errors: {walidacja['bledy']}"
    assert walidacja["zgadza_sie"] is True
    assert result["suma_gazet"]["total"] == total
    # per-newspaper totals must match the document's own 'Summe' block exactly
    assert result["suma_gazet"]["per_obiekt"] == walidacja["per_obiekt_z_dokumentu"]


def test_structure_and_chronological_order_8019() -> None:
    """Streets and customers keep the document (route) order; fields per product spec."""
    result = _parse_file("8019_21.10.2026.pdf")

    assert result["miasto"] == "Mömlingen"
    streets = [u["ulica"] for u in result["ulice"]]
    # first street block of the document is 'Am Holzberg' (from the header area)
    assert streets[0] == "Am Holzberg"
    # route order preserved: Am Ziegelrain comes after Am Holzberg, Bahnhofstr. after that
    assert streets.index("Am Ziegelrain") > streets.index("Am Holzberg")
    assert streets.index("Bahnhofstr.") > streets.index("Am Ziegelrain")

    first = result["ulice"][0]["klienci"][0]
    assert first == {
        "imie": "Werner",
        "nazwisko": "Schadt",
        "nr_domu": "1",
        "obiekt": "ME-OBB/AUSGABE",
        "ilosc": 1,
    }

    # every customer row has all spec fields populated (except imie for edge cases)
    for street in result["ulice"]:
        assert street["ulica"]
        for klient in street["klienci"]:
            assert klient["nazwisko"]
            assert klient["nr_domu"]
            assert klient["obiekt"].endswith("/AUSGABE")
            assert klient["ilosc"] >= 1


def test_graph_end_to_end_8031() -> None:
    """The LangGraph pipeline (extract → parse) works on raw PDF bytes."""
    pdf_bytes = (REAL_DATA / "8031_21.10.2026.pdf").read_bytes()
    state = app_graph.invoke({"pdf_bytes": pdf_bytes})

    result = state["result"]
    assert result["rejon"] == "8031"
    assert result["walidacja"]["status"] == "OK"
    assert result["suma_gazet"]["total"] == 37


def test_validation_catches_mismatch() -> None:
    """A tampered total must be flagged (the number MUST match)."""
    pages = [
        "Tagesliste vom Bezirk 9999 vom 01.01.2026 Seite 1/1\n"
        "Bezirk 9999                      Ablade                                     Zusteller\n"
        "Teststadt, Hauptstr.             Musterweg 1                                Max Mustermann\n"
        "12345 Teststadt\n"
        "5 Exemplare\n"
        "\n"
        "Hauptstr.\n"
        "Objekt                        HausNr (g/u) Name                                       Erschw.         Ex.\n"
        "ME-OBB/AUSGABE                1            A, B                                       1234567           1\n"
        "FR-BILD/AUSGABE               2            C, D                                       1234567           1\n"
    ]
    result = parse_tagesliste_text(pages)

    assert result["walidacja"]["status"] == "BLEDY"
    assert any("suma kopii nie zgadza sie" in e for e in result["walidacja"]["bledy"])
    assert result["suma_gazet"]["total"] == 2
