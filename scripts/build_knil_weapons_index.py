#!/usr/bin/env python3
"""Build a reproducible, metadata-only KNIL armament index from the NA snapshot."""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "assets" / "nationaal-archief.json"
TARGET = ROOT / "assets" / "knil-bewapening.json"

WEAPON_TERMS = re.compile(
    r"wapen|geweer|karabijn|revolver|pistool|machinegeweer|mitrailleur|bajonet|"
    r"munitie|kanon|artillerie|sabel|zwaard|tank|pantser|bren|lee.?enfield|"
    r"stengun|sten gun|garand|springfield|mauser|vickers|thompson|lanchester|"
    r"mortier|afweergeschut|brencarrier|bren-carrier",
    re.IGNORECASE,
)

# Exclude contextual or idiomatic matches that do not describe depicted weaponry.
NON_WEAPON_CONTEXT = re.compile(
    r"ongewapend|wapenbroeders|wapen der genie|verborgen wapens|wapens inleveren",
    re.IGNORECASE,
)

CATEGORIES = (
    ("Pantserwagens en tanks", re.compile(r"tank|pantser|carrier", re.I)),
    ("Machinegeweren en machinepistolen", re.compile(r"mitrailleur|machinegeweer|machinepistool|bren|vickers|lanchester", re.I)),
    ("Artillerie en mortieren", re.compile(r"artillerie|kanon|mortier|afweergeschut", re.I)),
    ("Geweerschutters en handwapens", re.compile(r"geweer|karabijn|bajonet|pistool|revolver|sabel|zwaard", re.I)),
)


def category_for(description: str) -> str:
    for label, pattern in CATEGORIES:
        if pattern.search(description):
            return label
    return "Overige bewapening"


def build_index(archive: dict) -> dict:
    records = []
    for source_record in archive.get("records", []):
        description = str(source_record.get("description") or "")
        if "knil" not in source_record.get("topics", []):
            continue
        if not WEAPON_TERMS.search(description) or NON_WEAPON_CONTEXT.search(description):
            continue
        records.append({
            "date": source_record.get("date"),
            "description": description,
            "uri": source_record.get("uri"),
            "collection": source_record.get("collection"),
            "rights": source_record.get("rights"),
            "category": category_for(description),
            "evidenceLevel": "Bronbeschrijving; geen onafhankelijke identificatie van het afgebeelde wapentype",
            "imagePublished": False,
        })

    records.sort(key=lambda item: (item["date"] or "9999", item["uri"] or ""))
    counts = Counter(record["category"] for record in records)
    return {
        "schemaVersion": 1,
        "source": "Nationaal Archief — linked open data fotocollectie",
        "sourceUrl": archive.get("sourceUrl", "https://www.nationaalarchief.nl/onderzoeken/linked-open-data/sparql-interface-fotocollectie"),
        "snapshotDate": archive.get("snapshotDate"),
        "sourceSnapshot": archive.get("snapshotDate"),
        "selection": {
            "topic": "knil",
            "descriptionPattern": WEAPON_TERMS.pattern,
            "recordCount": len(records),
            "uniqueDescriptions": len({record["description"] for record in records}),
        },
        "categoryCounts": dict(sorted(counts.items())),
        "rightsPolicy": (
            "The linked-open-data snapshot marks these records CNE (Copyright Not Evaluated). "
            "Live individual Nationaal Archief pages can show a different current rights status; "
            "verify each primary record before reuse. The index remains metadata-only until "
            "individual image rights and access are verified."
        ),
        "records": records,
    }


def main() -> int:
    archive = json.loads(SOURCE.read_text(encoding="utf-8"))
    if archive.get("schemaVersion") != 2 or not archive.get("snapshotDate"):
        raise SystemExit("FAIL: Nationaal Archief snapshot is missing schemaVersion 2 or snapshotDate")
    payload = build_index(archive)
    if not payload["records"]:
        raise SystemExit("FAIL: no KNIL armament source records found; previous index retained")
    TARGET.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"PASS: built {len(payload['records'])} KNIL armament metadata records "
        f"({payload['selection']['uniqueDescriptions']} unique descriptions), "
        f"snapshot {payload['sourceSnapshot']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
