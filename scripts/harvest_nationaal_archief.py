#!/usr/bin/env python3
"""Refresh a rights-aware, tagged metadata index from the Nationaal Archief SPARQL service."""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "assets" / "nationaal-archief.json"
ENDPOINT = "https://api.triplydb.com/datasets/nationaal-archief/beeldbank/services/beeldbank/sparql"
GRAPH = "https://demo.triply.cc/nationaal-archief/beeldbank/graphs/default"
PAGE_SIZE = 500
MAX_PAGES = 8

# Search the catalogue descriptions, not collection labels. A collection name such as
# "Dienst voor Legercontacten" is not evidence that every record depicts the KNIL.
QUERY = f"""
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX schema: <http://schema.org/>
SELECT ?s ?description (SAMPLE(?date) AS ?date)
       (SAMPLE(?collection) AS ?collection)
       (SAMPLE(?rights) AS ?rights)
       (SAMPLE(?creator) AS ?creator)
WHERE {{
  GRAPH <{GRAPH}> {{
    ?s a schema:Photograph ; dc:description ?description .
    OPTIONAL {{ ?s dc:date ?date }}
    OPTIONAL {{ ?s <http://purl.org/dc/dcmitype/Collection> ?collection }}
    OPTIONAL {{ ?s dc:creator ?creator }}
    OPTIONAL {{ ?s dc:rights ?rights }}
    FILTER(REGEX(LCASE(STR(?description)),
      "bandoeng|bandung|batavia|buitenzorg|bogor|semarang|soerabaja|surabaya|djokja|yogyakarta|malang|java|sumatra|borneo|celebes|sulawesi|indones|nederlands.?indi[eë]|nederlandsch.?indi[eë]|dutch east indies|netherlands indies|knil|bersiap|tni|pemoeda|agresi militer|politionele actie|onafhankelijkheidsstrijd"))
  }}
}}
GROUP BY ?s ?description
ORDER BY STR(?s)
LIMIT {PAGE_SIZE}
OFFSET {offset}
"""

PLACE_PATTERNS = {
    "bandung": r"\b(?:bandoeng|bandung)\b",
    "batavia": r"\b(?:batavia|jakarta)\b",
    "bogor": r"\b(?:buitenzorg|bogor)\b",
    "semarang": r"\bsemarang\b",
    "surabaya": r"\b(?:soerabaja|surabaya)\b",
    "yogyakarta": r"\b(?:djokja|djocja|yogyakarta|jogjakarta)\b",
    "malang": r"\bmalang\b",
}
JAVA_CONTEXT = re.compile(r"\b(?:java|bandoeng|bandung|batavia|jakarta|buitenzorg|bogor|semarang|soerabaja|surabaya|djokja|djocja|yogyakarta|jogjakarta|malang|poerwokerto|tjimahi|cheribon|garoet|tjikampek)\b", re.I)
KNIL = re.compile(r"\bknil\b|koninklijk nederlands(?:ch)?[- ]indisch leger|militaire luchtvaart knil|nederlands[- ]indisch leger", re.I)
MILITARY = re.compile(r"\b(?:militair(?:en)?|soldat(?:en)?|sergeant|officier|kapitein|luitenant|generaal|bataljon|eskadron|compagnie|krijgsraad|troepen|geweer|wapen(?:s)?|tank(?:s)?|kazern(?:e|es)|vliegveld|artillerie|leger)\b|\bknil\b", re.I)
DECOLONIZATION = re.compile(
    r"\b(?:bersiap|tni|pemoeda|republikeins(?:e)?|republiek indonesia|onafhankelijkheidsstrijd|"
    r"onafhankelijkheid|indonesian national revolution|indonesian war of independence|"
    r"agresi militer|politionele actie|politionele acties|perang kemerdekaan|perang revolusi|"
    r"linggadjati|renville|roem[- ]royen|soevereiniteitsoverdracht)\b",
    re.I,
)
SOCIETY = re.compile(r"\b(?:bevolking|inwoner(?:s)?|familie|gezin|vrouw(?:en)?|kind(?:eren)?|school|onderwijs|markt|pasar|dorp|desa|kampong|werk(?:zaamheden)?|arbeid|boer(?:en)?|landbouw|feest|bruiloft|huwelijk|dagelijks leven)\b", re.I)
ARCHITECTURE = re.compile(r"\b(?:gebouw|gebouwen|architectuur|architect|woning|huis|huizen|kantoor|hotel|kerk|moskee|tempel|straat|plein|aloon[- ]?aloon|station|brug|fabriek|schoolgebouw)\b", re.I)
TRANSPORT = re.compile(r"\b(?:trein|spoor(?:baan|weg)?|tram|station|haven|schip|vliegtuig|luchtvaart|tank|voertuig|auto|brug|veerboot)\b", re.I)
CULTURE = re.compile(r"\b(?:muziek|dans|dansers|ceremonie|religie|kerk|moskee|tempel|feest|theater|toneel|kunst|traditie)\b", re.I)
LANDSCAPE = re.compile(r"\b(?:landschap|berg(?:en)?|vulkaan|rivier|plantage|bos|kust|meer|sawah|rijstveld)\b", re.I)


def binding_value(row: dict, key: str) -> str | None:
    item = row.get(key)
    return item.get("value") if isinstance(item, dict) else None


def classify_record(description: str, date: str | None = None) -> tuple[list[str], list[str]]:
    """Classify only what the record description explicitly supports."""
    text = description or ""
    places = [place for place, pattern in PLACE_PATTERNS.items() if re.search(pattern, text, re.I)]
    if JAVA_CONTEXT.search(text):
        places.insert(0, "java")
        if not any(place in places for place in PLACE_PATTERNS):
            places.append("other-java")
    if re.search(r"\b(?:sumatra|sumatera|atjeh|aceh|padang|palembang|medan)\b", text, re.I):
        places.append("sumatra")
    if re.search(r"\b(?:borneo|kalimantan|celebes|sulawesi|makassar|makassar)\b", text, re.I):
        places.append("other-islands")

    topics: list[str] = []
    if KNIL.search(text):
        topics.append("knil")
    if MILITARY.search(text):
        topics.append("military")
    if DECOLONIZATION.search(text):
        topics.append("decolonization")
    # "Bersiap" is a narrower historical label and is assigned only if the source uses it.
    if re.search(r"\bbersiap\b", text, re.I):
        topics.append("bersiap")
    if SOCIETY.search(text):
        topics.append("society")
    if ARCHITECTURE.search(text):
        topics.append("architecture")
    if TRANSPORT.search(text):
        topics.append("transport")
    if CULTURE.search(text):
        topics.append("culture")
    if LANDSCAPE.search(text):
        topics.append("landscape")

    # Never assign the Bersiap label from a date alone; date is retained as source metadata.
    return sorted(set(topics)), sorted(set(places))


def main() -> int:
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    try:
        records_by_uri: dict[str, dict] = {}
        harvested_pages = 0
        for page_number in range(MAX_PAGES):
            offset = page_number * PAGE_SIZE
            query_text = QUERY.format(offset=offset)
            query = urlencode({"query": query_text, "format": "application/sparql-results+json"})
            request = Request(
                f"{ENDPOINT}?{query}",
                headers={
                    "Accept": "application/sparql-results+json",
                    "User-Agent": "IndischBeeldarchief/2.0 (public archival metadata index)",
                },
            )
            with urlopen(request, timeout=60) as response:
                if response.status != 200:
                    raise RuntimeError(f"SPARQL endpoint returned HTTP {response.status}")
                data = json.loads(response.read().decode("utf-8"))
            rows = data.get("results", {}).get("bindings", [])
            harvested_pages += 1
            for row in rows:
                uri = binding_value(row, "s")
                description = binding_value(row, "description")
                if not uri or not description:
                    continue
                topics, places = classify_record(description, binding_value(row, "date"))
                records_by_uri[uri] = {
                    "uri": uri,
                    "description": description,
                    "date": binding_value(row, "date"),
                    "collection": binding_value(row, "collection"),
                    "creator": binding_value(row, "creator"),
                    "rights": binding_value(row, "rights") or "Copyrightstatus niet vermeld",
                    "topics": topics,
                    "places": places,
                }
            if len(rows) < PAGE_SIZE:
                break
        records = sorted(records_by_uri.values(), key=lambda item: (item["date"] or "9999", item["description"].casefold()))
        if len(records) < 20:
            raise RuntimeError(f"Only {len(records)} records returned; keeping previous snapshot")
        topic_counts = Counter(topic for record in records for topic in record["topics"])
        place_counts = Counter(place for record in records for place in record["places"])
        payload = {
            "schemaVersion": 2,
            "source": "Nationaal Archief — linked open data fotocollectie",
            "sourceUrl": "https://www.nationaalarchief.nl/onderzoeken/linked-open-data/sparql-interface-fotocollectie",
            "endpoint": ENDPOINT,
            "snapshotDate": datetime.now(timezone.utc).isoformat(),
            "count": len(records),
            "pageSize": PAGE_SIZE,
            "maxPages": MAX_PAGES,
            "harvestedPages": harvested_pages,
            "truncatedAtSafetyLimit": harvested_pages == MAX_PAGES,
            "topicCounts": dict(sorted(topic_counts.items())),
            "placeCounts": dict(sorted(place_counts.items())),
            "rightsNote": (
                "Metadata-index. Geen thumbnails opgenomen: de bevraagde records kunnen "
                "Copyright niet bekend / Copyright Not Evaluated vermelden. Controleer "
                "de oorspronkelijke bron voor ieder hergebruik."
            ),
            "records": records,
        }
        TARGET.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"PASS: refreshed {len(records)} Nationaal Archief metadata records.")
        print("Topics:", json.dumps(payload["topicCounts"], ensure_ascii=False))
        print("Places:", json.dumps(payload["placeCounts"], ensure_ascii=False))
        return 0
    except Exception as exc:
        if TARGET.exists():
            print(f"WARN: Nationaal Archief refresh failed; retained previous snapshot: {exc}")
            return 0
        print(f"FAIL: no Nationaal Archief snapshot available: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
