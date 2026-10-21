"""Generator danych testowych — syntetyczne bezirki w strukturze realnych PDF-ów.

Użycie: python tools/generate_testdata.py [--bezirk 8019] [--seed 42]
Wynik: test-data/generated/<bezirk>.json (NIGDY nie commitujemy real-data/)
"""
from __future__ import annotations

import json
import random
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent.parent / "test-data" / "generated"

# Struktura z realnych PDF-ów: kody gazet, ulice, nazwiska (niemieckie)
NEWSPAPER_CODES = ["ME-OBB/AUSGABE", "FR-BILD/AUSGABE", "FR-SZ/AUSGABE", "ME-LAN/AUSGABE"]
STREETS = [
    "Bahnhofstr.", "Am Holzberg", "Bergstr.", "Blumenstr.", "Eichwaldstr.",
    "Uhlandstr.", "Wendelinusstr.", "Marienstr.", "Odenwaldstr.", "Kettelerstr.",
]
SURNAMES = [
    "Müller", "Schmidt", "Schneider", "Fischer", "Weber", "Schulz", "Koch",
    "Richter", "Hoffmann", "Wagner", "Becker", "Bauer", "Krüger", "Neumann",
]
FIRST_NAMES = ["Anna", "Lukas", "Marie", "Fritz", "Hans", "Ernst", "Uwe", "Karl"]


def gen_street(rng: random.Random) -> dict:
    street = rng.choice(STREETS)
    points = []
    for _ in range(rng.randint(3, 12)):
        points.append({
            "hausnr": str(rng.randint(1, 40)),
            "g_u": rng.choice(["", "", "g", "u"]),
            "name": f"{rng.choice(SURNAMES)}, {rng.choice(FIRST_NAMES)}",
            "newspaper_code": rng.choice(NEWSPAPER_CODES),
            "exemplare": 1,
        })
    return {"street": street, "points": points}


def gen_bezirk(bezirk: str, seed: int) -> dict:
    rng = random.Random(seed)
    streets = [gen_street(rng) for _ in range(8)]
    total = sum(p["exemplare"] for s in streets for p in s["points"])
    return {
        "bezirk": bezirk,
        "ort": "Mömlingen",
        "zusteller": {"name": "Test, Zusteller"},
        "exemplare_total": total,
        "streets": streets,
        "_meta": {"generated": True, "seed": seed},
    }


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for bezirk in ("8019", "8031"):
        data = gen_bezirk(bezirk, seed=42)
        out = OUT_DIR / ("bezirk_" + bezirk + ".json")
        out.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"[OK] {out} ({data['exemplare_total']} egz.)")


if __name__ == "__main__":
    main()
