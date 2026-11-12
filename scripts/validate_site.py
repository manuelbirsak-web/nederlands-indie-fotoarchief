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
        "places", "bandungTopics", "naArchive", "naResults", "naCount", "naMore",
    )
    for required in required_ids:
        if required not in parser.ids:
            fail(f"Verplicht element ontbreekt: #{required}")

    if not parser.title_seen or "<title>" not in source:
        fail("Paginatitel ontbreekt")

    for view in ("home", "indies", "java", "bandung", "knil", "bersiap", "daily"):
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
    if "DateTimeOriginal" not in source or "Opnamedatering niet vermeld in bron" not in source:
        fail("Expliciete historische datering en onbekende datum moeten worden onderscheiden")
    if '<option value="1800-1959" selected>' not in source:
        fail("De standaardweergave moet de historische periode 1800–1959 gebruiken")
    if "function isRelevantHistoricalPhoto" not in source or "isRelevantHistoricalPhoto(page,meta,year)" not in source:
        fail("Historische beeldrelevantie wordt niet per resultaat gecontroleerd")
    if "if(year===null)return range==='1800-1959'" not in source:
        fail("Ongedateerde bestanden moeten via inhoudelijke relevantie kunnen worden toegelaten")
    if "if(year===null&&!historicalContext.test(text))return false;" not in source:
        fail("Ongedateerde beelden moeten een expliciete historische contextverwijzing bevatten")
    if "year>=1800&&year<=1959)return year" not in source:
        fail("Opnamedatering moet worden begrensd tot 1800–1959")
    if "return base+" not in source or "filetype:bitmap" not in source:
        fail("Commons-zoekquery moet de bronzoekterm ongewijzigd doorgeven")
    if "|letter|lettre|envelope|postcard" not in source:
        fail("Niet-fotografische poststukken moeten uit de fotogalerij worden geweerd")
    if "topics.includes('decolonization')" not in source or "year<1945||year>1950" not in source:
        fail("Bersiap-rubriek moet inhoudelijke onderwerpclassificatie en de periode 1945–1950 combineren")
    if "data-place=\"all\"" not in source or "let view='home',place='all'" not in source:
        fail("Java moet standaard alle Java-plaatsen tonen, niet uitsluitend Bandoeng")
    if "const topicFilterToArchive" not in source or "place==='other'?'other-java':place" not in source:
        fail("Archief-index mist de expliciete onderwerp- of plaatsfacetfilters")
    if "naVisibleCount+=12" not in source or "id=\"naMore\"" not in source:
        fail("Nationaal Archief-records moeten in pagina's doorzoekbaar blijven")
    if ".filters select{width:100%;max-width:100%;min-width:0}" not in source:
        fail("Mobiele datumfilters moeten binnen de viewport blijven")
    if "/\\b(wordmark|logo|map of|coat of arms|rank insignia|book cover" not in source:
        fail("Niet-fotografische illustraties en publicaties worden niet aantoonbaar uitgesloten")
    if "match(/(?:18|19|20)\\d{2}/)" not in source:
        fail("Datumparser voor Nationaal Archief-records ontbreekt of is onjuist")
    if "const seenFiles=new Set()" not in source or "foundThisLoad < 8 && batches < 4" not in source:
        fail("Zoeken moet duplicaten voorkomen en lege zoekpagina’s automatisch overslaan")
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
    for source_url in (
        "https://digitalcollections.universiteitleiden.nl/imagecollection-kitlv",
        "https://hetutrechtsarchief.nl/over-ons/nieuws/ruim-5-000-fotos-uit-voormalig-nederlands-indie-online-beschikbaar",
        "https://beeldbank.nimh.nl/",
        "https://collectie.wereldmuseum.nl/",
        "https://zoeken.nieuweinstituut.nl/nl/zoeken-op-het-portaal",
        "https://data.rijksmuseum.nl/docs/search",
        "https://www.europeana.eu/en/search",
        "https://www.delpher.nl/",
    ):
        if source_url not in source:
            fail(f"Primaire collectiebron ontbreekt: {source_url}")

    try:
        archive = json.loads(ARCHIVE_INDEX.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"Nationaal Archief JSON is ongeldig: {exc}")
    records = archive.get("records", [])
    if archive.get("schemaVersion") != 2:
        fail("Nationaal Archief-index mist schemaVersion 2 en de classificatievelden")
    if not isinstance(records, list) or len(records) < 20:
        fail("Nationaal Archief-index bevat minder dan 20 records")
    allowed_topics = {"knil", "military", "decolonization", "bersiap", "society", "architecture", "transport", "culture", "landscape"}
    allowed_places = {"java", "bandung", "batavia", "bogor", "semarang", "surabaya", "yogyakarta", "malang", "other-java", "sumatra", "other-islands"}
    if len({record.get("uri") for record in records}) != len(records):
        fail("Nationaal Archief-index bevat dubbele permanente record-URL's")
    for record in records:
        if not record.get("uri", "").startswith("http://proxy.handle.net/10648/"):
            fail("Nationaal Archief-record mist een permanente handle-URL")
        if not record.get("description"):
            fail("Nationaal Archief-record mist een beschrijving")
        if "thumbnail" in record or "image" in record:
            fail("Rechten-onzekere Nationaal Archief-afbeelding wordt onterecht als thumbnail opgeslagen")
        if not isinstance(record.get("topics"), list) or not isinstance(record.get("places"), list):
            fail("Nationaal Archief-record mist onderwerp- of plaatslabels")
        if not set(record["topics"]).issubset(allowed_topics):
            fail("Onbekend onderwerp-label in Nationaal Archief-index")
        if not set(record["places"]).issubset(allowed_places):
            fail("Onbekend plaats-label in Nationaal Archief-index")
        if "bersiap" in record["topics"] and not re.search(r"\bbersiap\b", record["description"], re.I):
            fail("Bersiap-label mag alleen verschijnen wanneer de bronbeschrijving deze term gebruikt")

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
