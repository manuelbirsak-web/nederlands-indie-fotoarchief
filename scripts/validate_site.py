#!/usr/bin/env python3
"""Static pre-deployment checks for the Indisch Beeldarchief."""
from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"

class SiteParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.buttons: list[dict[str, str | None]] = []
        self.links: list[str] = []
        self.images_with_alt = 0
        self.title_seen = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        data = dict(attrs)
        if "id" in data and data["id"]:
            self.ids.append(data["id"] or "")
        if tag == "button":
            self.buttons.append(data)
        if tag == "a" and data.get("href"):
            self.links.append(data["href"] or "")
        if tag == "img" and data.get("alt") is not None:
            self.images_with_alt += 1
        if tag == "title":
            self.title_seen = True

def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)

def main() -> None:
    if not INDEX.is_file():
        fail("index.html ontbreekt")
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
    for required in ("main", "nav", "results", "q", "period", "topic", "more", "places", "bandungTopics"):
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
    if "AbortController" not in source or "data.continue" not in source:
        fail("Abort/continuation afhandeling ontbreekt")
    if "textContent" not in source:
        fail("Veilige DOM-tekstweergave ontbreekt")
    if not any(link.startswith("https://") for link in parser.links):
        fail("Geen veilige HTTPS-bronlinks gevonden")

    script_blocks = re.findall(r"<script>(.*?)</script>", source, flags=re.DOTALL | re.IGNORECASE)
    if not script_blocks:
        fail("Inline JavaScript ontbreekt")
    if not any("syncView();load(true);" in block for block in script_blocks):
        fail("Applicatie-initialisatie ontbreekt")
    print(f"PASS: HTML geparsed; {len(parser.ids)} IDs; {len(parser.links)} HTTPS/bronlinks; vereiste views en Java-secties aanwezig.")
    print("NOTE: Dit is een statische contractcheck, geen browser-, netwerk-, performance- of visuele test.")

if __name__ == "__main__":
    main()
