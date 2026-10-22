"""Tagesliste PDF parser — deterministic state machine (no LLM).

Document format (zustellerportal export, pypdf layout-mode text):

    Page header : 'Tagesliste vom Bezirk {code} vom {date} ... Seite n/m'
    Header table: 3 columns — area/city | Ablade (drop-off address) | Zusteller
    Total       : '{N} Exemplare' (page 1 only)
    Street block: street marker line, column header 'Objekt ...', data rows
                  '{CODE/AUSGABE} {hausnr} {Name, Vorname} {erschw} {ex}'
    Summary     : last page — 'Summe' + per-code copy totals + grand total
    Footer      : 'Generiert am {timestamp}'

Only business-relevant fields are extracted: city, bezirk code, delivery person,
date, streets in document (route) order and customers with name / house number /
newspaper code. Internal markings (Erschw.) are discarded. Chronological order
of the document is preserved — it IS the delivery route order.

Output JSON keys follow the product spec (Polish): miasto, rejon, dostawca,
data, ulice[{ulica, klienci[{imie, nazwisko, nr_domu, obiekt, ilosc}]}],
suma_gazet{total, per_obiekt}, walidacja{...}.
"""
from __future__ import annotations

import re

# 'Tagesliste vom Bezirk 8019 vom 21.10.2026 ... Seite 1/4'
PAGE_HEADER_RE = re.compile(
    r"^Tagesliste vom Bezirk (?P<bezirk>\d+) vom (?P<data>[\d.]+)\s+Seite\s+\d+/\d+\s*$"
)
# '84 Exemplare' — total copy count stated in the header (page 1)
TOTAL_EX_RE = re.compile(r"^(?P<n>\d+) Exemplare$")
# Data row: newspaper code | house number | 'Name, Vorname' | Erschw. (discarded) | Ex. (copies)
DATA_ROW_RE = re.compile(
    r"^(?P<code>[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*/AUSGABE)\s+"
    r"(?P<hausnr>\S+)\s+"
    r"(?P<name>.+?)\s+"
    r"(?P<erschw>\d+)\s+"
    r"(?P<ex>\d+)\s*$"
)
# Summary block row: newspaper code | Erschw. (discarded) | copy count for that code
SUMMARY_ROW_RE = re.compile(
    r"^(?P<code>[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)*/AUSGABE)\s+(?P<erschw>\d+)\s+(?P<count>\d+)\s*$"
)
# Street marker with trailing 'PLZ city' (layout mode keeps it on the same line)
STREET_PLZ_RE = re.compile(r"^(?P<street>.+?)\s+\d{5}\s+\S.*$")
# Header continuation line: starts with a 5-digit PLZ ('63853 Mömlingen')
PLZ_LINE_RE = re.compile(r"^\d{5}\s+\S")


def _split_header_columns(line: str) -> list[str]:
    """Split the 3-column header table row (layout mode pads columns with >=2 spaces)."""
    return [c for c in re.split(r"\s{2,}", line.strip()) if c]


def parse_tagesliste_text(pages: list[str]) -> dict:
    """Parse layout-mode page texts into the product JSON structure.

    Args:
        pages: one string per PDF page (pypdf extraction_mode='layout').

    Returns:
        Dict with miasto/rejon/dostawca/data, ulice[] in document order,
        suma_gazet (computed) and walidacja (document totals vs computed).
    """
    result: dict = {
        "miasto": "",
        "rejon": "",
        "dostawca": "",
        "data": "",
        "total_z_dokumentu": None,
        "ulice": [],  # [{"ulica": str, "klienci": [ {...} ]}] — document order
    }
    per_code_doc: dict[str, int] = {}  # copy totals from the 'Summe' block (last page)
    suma_doc: int | None = None

    state = "header"  # header -> streets -> summary
    expecting_header_values = False
    current_street: dict | None = None

    for page_text in pages:
        for raw_line in page_text.splitlines():
            stripped = raw_line.strip()
            if not stripped:
                continue

            m = PAGE_HEADER_RE.match(stripped)
            if m:
                result["rejon"] = m.group("bezirk")
                result["data"] = m.group("data")
                state = "header"  # new page: back to header/street context
                expecting_header_values = False
                continue
            if stripped.startswith("Generiert am"):
                continue

            if state == "summary":
                sm = SUMMARY_ROW_RE.match(stripped)
                if sm:
                    per_code_doc[sm.group("code")] = int(sm.group("count"))
                    continue
                if re.fullmatch(r"\d+", stripped):
                    suma_doc = int(stripped)
                    continue
                # anything else inside the summary block is layout noise

            if state == "header":
                if expecting_header_values:
                    cols = _split_header_columns(stripped)
                    if cols:
                        # left column: area/city ('Mömlingen, Bahnhofstr.' -> 'Mömlingen')
                        result["miasto"] = cols[0].split(",")[0].strip()
                        # right column: delivery person name
                        result["dostawca"] = cols[-1].strip()
                    expecting_header_values = False
                    continue
                if stripped.startswith("Bezirk") and "Ablade" in stripped:
                    expecting_header_values = True  # next line holds the values
                    continue
                tm = TOTAL_EX_RE.match(stripped)
                if tm:
                    result["total_z_dokumentu"] = int(tm.group("n"))
                    continue
                if PLZ_LINE_RE.match(stripped):
                    continue  # header address continuation ('63853 Mömlingen')
                # first street marker of the page — fall through to streets state
                state = "streets"

            # state == "streets" (or just transitioned)
            if stripped == "Summe":
                state = "summary"
                continue
            if stripped.startswith("Objekt"):
                continue  # column header repeated per street block
            dm = DATA_ROW_RE.match(stripped)
            if dm:
                if current_street is None:  # defensive: row before any street marker
                    current_street = {"ulica": "", "klienci": []}
                    result["ulice"].append(current_street)
                name_full = dm.group("name").strip()
                if "," in name_full:
                    nazwisko, imie = (p.strip() for p in name_full.split(",", 1))
                else:
                    nazwisko, imie = name_full, ""
                current_street["klienci"].append(
                    {
                        "imie": imie,
                        "nazwisko": nazwisko,
                        "nr_domu": dm.group("hausnr"),
                        "obiekt": dm.group("code"),
                        "ilosc": int(dm.group("ex")),
                    }
                )
                continue
            # anything else in streets state is a street marker
            sm_street = STREET_PLZ_RE.match(stripped)
            street_name = sm_street.group("street").strip() if sm_street else stripped
            current_street = {"ulica": street_name, "klienci": []}
            result["ulice"].append(current_street)

    # --- computed totals (from parsed rows, in document order) -----------------
    per_obiekt: dict[str, int] = {}
    total_wyliczone = 0
    for street in result["ulice"]:
        for klient in street["klienci"]:
            total_wyliczone += klient["ilosc"]
            kod = klient["obiekt"]
            per_obiekt[kod] = per_obiekt.get(kod, 0) + klient["ilosc"]

    # --- validation: computed totals must match the document's own numbers -----
    errors: list[str] = []
    if result["total_z_dokumentu"] is None:
        errors.append("brak 'N Exemplare' w naglowku")
    elif total_wyliczone != result["total_z_dokumentu"]:
        errors.append(
            f"suma kopii nie zgadza sie: wyliczono {total_wyliczone}, "
            f"dokument podaje {result['total_z_dokumentu']}"
        )
    if suma_doc is not None and total_wyliczone != suma_doc:
        errors.append(
            f"suma z bloku 'Summe' nie zgadza sie: wyliczono {total_wyliczone}, "
            f"blok podaje {suma_doc}"
        )
    for kod, licznik in per_code_doc.items():
        if per_obiekt.get(kod, 0) != licznik:
            errors.append(
                f"kopie dla {kod} nie zgadza sie: wyliczono {per_obiekt.get(kod, 0)}, "
                f"blok 'Summe' podaje {licznik}"
            )

    result["suma_gazet"] = {"total": total_wyliczone, "per_obiekt": per_obiekt}
    result["walidacja"] = {
        "status": "OK" if not errors else "BLEDY",
        "bledy": errors,
        "total_z_dokumentu": result.pop("total_z_dokumentu"),
        "total_wyliczone": total_wyliczone,
        "zgadza_sie": not errors,
        "per_obiekt_z_dokumentu": per_code_doc,
    }
    return result
