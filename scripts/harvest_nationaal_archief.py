#!/usr/bin/env python3
"""Refresh a rights-aware metadata-only index from the Nationaal Archief SPARQL service."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "assets" / "nationaal-archief.json"
ENDPOINT = "https://api.triplydb.com/datasets/nationaal-archief/beeldbank/services/beeldbank/sparql"
GRAPH = "https://demo.triply.cc/nationaal-archief/beeldbank/graphs/default"
LIMIT = 300

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
    FILTER(
      CONTAINS(LCASE(STR(?description)), "bandoeng") ||
      CONTAINS(LCASE(STR(?description)), "bandung") ||
      CONTAINS(LCASE(STR(?description)), "batavia") ||
      CONTAINS(LCASE(STR(?description)), "buitenzorg") ||
      CONTAINS(LCASE(STR(?description)), "bogor") ||
      CONTAINS(LCASE(STR(?description)), "semarang") ||
      CONTAINS(LCASE(STR(?description)), "soerabaja") ||
      CONTAINS(LCASE(STR(?description)), "surabaya") ||
      CONTAINS(LCASE(STR(?description)), "djokja") ||
      CONTAINS(LCASE(STR(?description)), "yogyakarta") ||
      CONTAINS(LCASE(STR(?description)), "malang") ||
      CONTAINS(LCASE(STR(?description)), "knil") ||
      CONTAINS(LCASE(STR(?description)), "nederlands-indi") ||
      CONTAINS(LCASE(STR(?description)), "dutch east indies")
    )
  }}
}}
GROUP BY ?s ?description
LIMIT {LIMIT}
"""

def binding_value(row: dict, key: str) -> str | None:
    item = row.get(key)
    return item.get("value") if isinstance(item, dict) else None

def main() -> int:
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    try:
        query = urlencode({"query": QUERY, "format": "application/sparql-results+json"})
        request = Request(
            f"{ENDPOINT}?{query}",
            headers={
                "Accept": "application/sparql-results+json",
                "User-Agent": "IndischBeeldarchief/1.0 (public archival metadata index)",
            },
        )
        with urlopen(request, timeout=45) as response:
            if response.status != 200:
                raise RuntimeError(f"SPARQL endpoint returned HTTP {response.status}")
            data = json.loads(response.read().decode("utf-8"))
        rows = data.get("results", {}).get("bindings", [])
        records_by_uri: dict[str, dict] = {}
        for row in rows:
            uri = binding_value(row, "s")
            description = binding_value(row, "description")
            if not uri or not description:
                continue
            records_by_uri[uri] = {
                "uri": uri,
                "description": description,
                "date": binding_value(row, "date"),
                "collection": binding_value(row, "collection"),
                "creator": binding_value(row, "creator"),
                "rights": binding_value(row, "rights") or "Copyrightstatus niet vermeld",
            }
        records = list(records_by_uri.values())
        if len(records) < 20:
            raise RuntimeError(f"Only {len(records)} records returned; keeping previous snapshot")
        payload = {
            "source": "Nationaal Archief — linked open data fotocollectie",
            "sourceUrl": "https://www.nationaalarchief.nl/onderzoeken/linked-open-data/sparql-interface-fotocollectie",
            "endpoint": ENDPOINT,
            "snapshotDate": datetime.now(timezone.utc).isoformat(),
            "count": len(records),
            "queryLimit": LIMIT,
            "rightsNote": (
                "Metadata-index. Geen thumbnails opgenomen: de bevraagde records kunnen "
                "Copyright niet bekend / Copyright Not Evaluated vermelden. Controleer "
                "de oorspronkelijke bron voor ieder hergebruik."
            ),
            "records": records,
        }
        TARGET.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"PASS: refreshed {len(records)} Nationaal Archief metadata records.")
        return 0
    except Exception as exc:
        if TARGET.exists():
            print(f"WARN: Nationaal Archief refresh failed; retained previous snapshot: {exc}")
            return 0
        print(f"FAIL: no Nationaal Archief snapshot available: {exc}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
