#!/usr/bin/env python3
"""Static pre-deployment checks for the Indisch Beeldarchief."""
from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
ARCHIVE_INDEX = ROOT / "assets" / "nationaal-archief.json"

class SiteParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.links: list[str] = []
        self.title_seen = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = dict(attrs)
        if data.get("id"):
            self.ids.append(data["id"] or "")
        if tag == "a" and data.get("href"):
            self.links.append(data["href"] or "")
        if tag == "title":
            self.title_seen = True

def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)

def main() -> None:
    if not INDEX.is_file():
        fail("index.html ontbreekt")
    if not ARCHIVE_INDEX.is_file():
        fail("Nationaal Archief metadata-index ontbreekt")

    source = INDEX.read_text(encoding="utf-8")
    parser = SiteParser()
    try:
        parser.feed(source)
        parser.close()
    except Exception as exc:
        fail(f"HTML parserfout: {exc}")

    duplicates = sorted({item for item in parser.ids if parser.ids.count(item) > 1})
    if duplicates:
        fail("Dubbele id-attributen: " + ", ".join(duplicates))

    required_ids = (
        "main", "nav", "results", "q", "period", "topic", "more",
        "places", "bandungTopics", "naArchive", "naResults", "naCount",
    )
    for required in required_ids:
        if required not in parser.ids:
            fail(f"Verplicht element ontbreekt: #{required}")

    if not parser.title_seen or "<title>" not in source:
        fail("Paginatitel ontbreekt")

    for view in ("home", "indies", "java", "bandung", "knil", "daily"):
        if f'data-view="{view}"' not in source:
            fail(f"Navigatiesectie ontbreekt: {view}")
    for place in ("bandung", "batavia", "bogor", "semarang", "surabaya", "yogyakarta", "malang", "other"):
        if f'data-place="{place}"' not in source:
            fail(f"Java-plaatsfilter ontbreekt: {place}")

    if "https://commons.wikimedia.org/w/api.php" not in source:
        fail("Wikimedia Commons API-endpoint ontbreekt")
    if "filetype:bitmap" not in source or "info.mime" not in source:
        fail("Zoekfunctie filtert niet aantoonbaar op beeldbestanden")
    if "meta?.DateTime?.value" in source:
        fail("Uploaddatum mag niet als historische opnamedatum worden gebruikt")
    if "DateTimeOriginal" not in source or "Datering niet vermeld" not in source:
        fail("Expliciete historische datering en onbekende datum moeten worden onderscheiden")
    if '<option value="1800-1950" selected>' not in source:
        fail("De standaardweergave moet strikt op de historische periode 1800–1950 staan")
    if "function isRelevantHistoricalPhoto" not in source or "if (!isRelevantHistoricalPhoto(page,meta,year)) continue;" not in source:
        fail("Historische beeldrelevantie wordt niet per resultaat gecontroleerd")
    if "year===null||year<1800" not in source:
        fail("Ongedateerde of niet-historisch gedateerde afbeeldingen mogen niet standaard in de galerij")
    if "/\\b(wordmark|logo|map of|coat of arms|rank insignia|book cover" not in source:
        fail("Niet-fotografische illustraties en publicaties worden niet aantoonbaar uitgesloten")
    if "match(/(?:18|19|20)\\d{2}/)" not in source:
        fail("Datumparser voor Nationaal Archief-records ontbreekt of is onjuist")
    if "AbortController" not in source or "data.continue" not in source:
        fail("Abort/continuation afhandeling ontbreekt")
    if "textContent" not in source:
        fail("Veilige DOM-tekstweergave ontbreekt")
    if "assets/nationaal-archief.json" not in source:
        fail("Lokale Nationaal Archief index wordt niet geladen")
    if "view/collection/kitlvphotos" in source:
        fail("Verouderde KITLV-collectie-URL is nog aanwezig")
    if not any(link.startswith("https://") for link in parser.links):
        fail("Geen veilige HTTPS-bronlinks gevonden")

    try:
        archive = json.loads(ARCHIVE_INDEX.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"Nationaal Archief JSON is ongeldig: {exc}")
    records = archive.get("records", [])
    if not isinstance(records, list) or len(records) < 20:
        fail("Nationaal Archief-index bevat minder dan 20 records")
    for record in records:
        if not record.get("uri", "").startswith("http://proxy.handle.net/10648/"):
            fail("Nationaal Archief-record mist een permanente handle-URL")
        if not record.get("description"):
            fail("Nationaal Archief-record mist een beschrijving")
        if "thumbnail" in record or "image" in record:
            fail("Rechten-onzekere Nationaal Archief-afbeelding wordt onterecht als thumbnail opgeslagen")

    scripts = re.findall(r"<script>(.*?)</script>", source, flags=re.DOTALL | re.IGNORECASE)
    if not scripts:
        fail("Inline JavaScript ontbreekt")
    if not any("loadNationaalArchiefIndex();" in block for block in scripts):
        fail("Nationaal Archief-index wordt niet geïnitialiseerd")

    print(
        f"PASS: HTML geparsed; {len(parser.ids)} IDs; {len(parser.links)} bronlinks; "
        f"{len(records)} Nationaal Archief-records; vereiste secties, rechten- en datumcontroles aanwezig."
    )
    print("NOTE: Dit is een statische contractcheck. Browser-, performance- en visuele tests worden apart uitgevoerd.")

if __name__ == "__main__":
    main()
