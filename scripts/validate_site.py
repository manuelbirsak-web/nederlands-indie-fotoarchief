#!/usr/bin/env python3
"""Static pre-deployment checks for the Indisch Beeldarchief."""
from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

from build_knil_weapons_index import build_index as build_knil_weapons_index

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
ARCHIVE_INDEX = ROOT / "assets" / "nationaal-archief.json"
RIJKSMUSEUM_INDEX = ROOT / "assets" / "rijksmuseum.json"
KNIL_WEAPONS_INDEX = ROOT / "assets" / "knil-bewapening.json"

FAMILY_ASSETS = {
    "assets/family/IMG_5108.jpeg": {
        "size": 166524,
        "sha256": "2807b2f5048ca65df0026d02c8449f411fb9415c7f9871403fc1d0024a4893fb",
    },
    "assets/family/IMG_5107.jpeg": {
        "size": 259653,
        "sha256": "9766e8a2e8a0976a8c00ee522474aa352322909d5acd4ab0186d969a1bff3ccb",
    },
}

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
    if not RIJKSMUSEUM_INDEX.is_file():
        fail("Rijksmuseum-foto-index ontbreekt")
    if not KNIL_WEAPONS_INDEX.is_file():
        fail("KNIL-bewapeningsindex ontbreekt")
    for relative, expected in FAMILY_ASSETS.items():
        asset = ROOT / relative
        if not asset.is_file():
            fail(f"Originele familiefoto ontbreekt: {relative}")
        data = asset.read_bytes()
        if len(data) != expected["size"]:
            fail(f"Bestandsgrootte originele familiefoto wijkt af: {relative}")
        if __import__("hashlib").sha256(data).hexdigest() != expected["sha256"]:
            fail(f"SHA-256 originele familiefoto wijkt af: {relative}")
        if not data.startswith(bytes.fromhex("ffd8ff")):
            fail(f"Originele familiefoto is geen geldige JPEG: {relative}")


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
        "naSnapshotNote", "rmArchive", "rmResults", "rmCount", "rmSnapshotNote", "rmMore",
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
    if "function isReusableCommonsLicense(meta)" not in source or "if (!isReusableCommonsLicense(meta)) continue;" not in source:
        fail("Wikimedia-afbeeldingen worden niet geblokkeerd zonder expliciete herbruikbare licentie")
    if "function commonsLicenseUrl(meta)" not in source or "creativecommons.org/publicdomain/zero/1.0/" not in source:
        fail("Rechtencontrole mist de expliciete CC0-allowlist")
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
    for term in ("marechaussee", "veldpolitie", "klewang", "karabijn", "infanterie", "artillerie", "garnizoen"):
        if term not in source.lower():
            fail(f"KNIL-zoekselectie mist historische militaire terminologie: {term}")
    for term in ("pemuda", "pemoeda", "laskar", "tentara keamanan rakyat", "politionele actie", "agresi militer", "linggadjati", "renville"):
        if term not in source.lower():
            fail(f"Bersiap/dekolonisatie-zoekselectie mist historische terminologie: {term}")
    for term in ("ml-knil", "militaire luchtvaart", "heiho", "gurkha", "bataljon"):
        if term not in source.lower():
            fail(f"KNIL-zoekselectie mist termen uit de Indische kampwoordenlijst: {term}")
    for term in ("nica", "rapwi", "apwi", "amacab", "seac", "tentara keamanan rakjat", "badan keamanan rakjat"):
        if term not in source.lower():
            fail(f"Bersiap-zoekselectie mist termen uit de Indische kampwoordenlijst: {term}")
    for term in ("cultuurstelsel", "ethische politiek", "batig slot", "slavernij", "adat", "repatriering", "peta", "nefis", "mariniersbrigade", "stoottroepen", "tijgerbrigade", "madioen-opstand", "renville-overeenkomst", "soevereiniteitsoverdracht", "soerakarta", "djocja", "preanger", "batik", "gamelan", "wajang", "krakatau", "lahar", "nootmuskaat", "kpm", "knilm"):
        if term not in source.lower():
            fail(f"Nedindie thematische zoekselectie mist een term uit de LINKS-directory: {term}")
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
    if "const seenFiles=new Set()" not in source or "foundThisLoad < 8 && batches < 8" not in source:
        fail("Zoeken moet duplicaten voorkomen en lege zoekpagina’s automatisch overslaan")
    if "AbortController" not in source or "data.continue" not in source:
        fail("Abort/continuation afhandeling ontbreekt")
    if "const UI_STATE_KEY='indisch-beeldarchief-ui-state-v1'" not in source or "function restoreUiState()" not in source:
        fail("Actief tabblad en filters moeten na browserrefresh worden hersteld")
    if "restoreUiState();syncView();" not in source or "saveUiState()" not in source:
        fail("Navigatie- en filterstatus wordt niet vóór de eerste beeldzoekopdracht hersteld en opgeslagen")
    if "img.crossOrigin='anonymous'" in source:
        fail("Externe foto-CDN mag niet onnodig met CORS-modus worden geladen")
    if "img.loading=visibleCount<6?'eager':'lazy'" not in source or "cache:'no-store'" not in source:
        fail("Zichtbare foto's moeten direct laden en filterwijzigingen moeten verse bronresultaten aanvragen")
    if "batches < 8" not in source:
        fail("Fotoselectie moet voldoende bronpagina's doorzoeken bij beperkte filterresultaten")
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

    if "assets/family/IMG_5108.jpeg" not in source or "assets/family/IMG_5107.jpeg" not in source:
        fail("Familiepagina verwijst niet naar de originele foto's")
    if "assets/family/birsak-woning.jpg" in source or "assets/family/birsak-familieportret.jpg" in source:
        fail("Verouderde verkleinde familiefoto's worden nog gebruikt")

    if "assets/rijksmuseum.json" not in source or "function renderRijksmuseumRecords" not in source:
        fail("Rijksmuseum Linked Art-index wordt niet door de website geïntegreerd")
    if "assets/knil-bewapening.json" not in source or "function renderKnilWeaponsRecords" not in source or "loadKnilWeaponsIndex();" not in source:
        fail("KNIL-bewapeningsindex wordt niet in de website geïntegreerd")
    if 'id="knilWeapons"' not in source or 'id="knilWeaponsMore"' not in source:
        fail("KNIL-bewapeningssectie of paginering ontbreekt")
    if "RM_IMAGE_RIGHTS.has(record.imageRightsUrl)" not in source:
        fail("De browser moet de beeldlicentie expliciet allowlisten vóór een afbeelding wordt getoond")
    if "loadRijksmuseumIndex()" not in source:
        fail("Rijksmuseum-foto-index wordt niet geïnitialiseerd")
    if "function addRijksmuseumGalleryCard(record)" not in source or "function appendRightsClearedRijksmuseumImages()" not in source:
        fail("Rechtenveilige Rijksmuseum-foto's worden niet geïntegreerd in de hoofdgalerij")
    if "RM_IMAGE_RIGHTS.has(record.imageRightsUrl)" not in source or "appendRightsClearedRijksmuseumImages();" not in source:
        fail("Hoofdgalerij moet alleen expliciet vrijgegeven Rijksmuseum-beelden toevoegen na laden en zoeken")


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
    if archive.get("count") != len(records):
        fail("Nationaal Archief-index telling komt niet overeen met het aantal records")
    if any(record.get("image") or record.get("thumbnail") or record.get("imageUrl") for record in records):
        fail("Nationaal Archief-record bevat een afbeelding terwijl rechtenstatus niet vooraf per beeld is vrijgegeven")
    try:
        rijksmuseum = json.loads(RIJKSMUSEUM_INDEX.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"Rijksmuseum JSON is ongeldig: {exc}")
    rm_records = rijksmuseum.get("records", [])
    if rijksmuseum.get("schemaVersion") != 1:
        fail("Rijksmuseum-index mist schemaVersion 1")
    if not isinstance(rm_records, list) or len(rm_records) < 20:
        fail("Rijksmuseum-index bevat minder dan 20 foto-objecten")
    if rijksmuseum.get("count") != len(rm_records):
        fail("Rijksmuseum-index telling komt niet overeen met het aantal objectrecords")
    rm_allowed_rights = {
        "https://creativecommons.org/publicdomain/mark/1.0/",
        "https://creativecommons.org/publicdomain/zero/1.0/",
    }
    if len({record.get("id") for record in rm_records}) != len(rm_records):
        fail("Rijksmuseum-index bevat dubbele object-ID's")
    rm_image_count = 0
    for record in rm_records:
        if record.get("recordType") != "photograph":
            fail("Rijksmuseum-index bevat een object dat niet als foto is geclassificeerd")
        if not str(record.get("objectUrl", "")).startswith("https://id.rijksmuseum.nl/"):
            fail("Rijksmuseum-record mist een permanent Linked Art-object-ID")
        if not isinstance(record.get("topics"), list) or not isinstance(record.get("places"), list):
            fail("Rijksmuseum-record mist onderwerp- of plaatslabels")
        if not set(record["topics"]).issubset(allowed_topics):
            fail("Onbekend onderwerp-label in Rijksmuseum-index")
        if not set(record["places"]).issubset(allowed_places):
            fail("Onbekend plaats-label in Rijksmuseum-index")
        if record.get("imageUrl"):
            rm_image_count += 1
            if not str(record["imageUrl"]).startswith("https://iiif.micr.io/"):
                fail("Rijksmuseum-afbeelding is geen geverifieerde IIIF-micr.io URL")
            if record.get("imageRightsUrl") not in rm_allowed_rights:
                fail("Rijksmuseum-afbeelding mist expliciete Public Domain Mark/CC0-beeldrechten")
        elif record.get("imageRightsUrl") in rm_allowed_rights and record.get("imageUnavailableReason") is None:
            fail("Rijksmuseum-record zonder beeldlink bevat tegenstrijdige rechtenmetadata")
    if rijksmuseum.get("imageCount") != rm_image_count:
        fail("Rijksmuseum-index imageCount komt niet overeen met het aantal rechtenveilige beelden")
    if rijksmuseum.get("metadataOnlyCount") != sum(1 for record in rm_records if not record.get("imageUrl")):
        fail("Rijksmuseum metadataOnlyCount komt niet overeen met de records zonder beeld")
    if rijksmuseum.get("imageCount") + rijksmuseum.get("metadataOnlyCount") != len(rm_records):
        fail("Rijksmuseum beeld- en metadata-only telling dekt niet alle records")

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

    try:
        knil_weapons = json.loads(KNIL_WEAPONS_INDEX.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"KNIL-bewapeningsindex JSON is ongeldig: {exc}")
    weapon_records = knil_weapons.get("records", [])
    expected_weapons = build_knil_weapons_index(archive)
    if knil_weapons != expected_weapons:
        fail("KNIL-bewapeningsindex is niet reproduceerbaar uit de actuele Nationaal Archief-snapshot")
    if knil_weapons.get("schemaVersion") != 1 or knil_weapons.get("sourceSnapshot") != archive.get("snapshotDate"):
        fail("KNIL-bewapeningsindex mist schema of verwijst niet naar dezelfde Nationaal Archief-snapshot")
    na_by_uri = {r.get("uri"): r for r in records}
    if len({r.get("uri") for r in weapon_records}) != len(weapon_records):
        fail("KNIL-bewapeningsindex bevat dubbele bron-URI's")
    for record in weapon_records:
        original = na_by_uri.get(record.get("uri"))
        if not original or original.get("description") != record.get("description") or original.get("rights") != record.get("rights"):
            fail("KNIL-bewapeningsrecord is niet exact herleidbaar naar de gekoppelde Nationaal Archief-snapshot")
        if record.get("rights") != "http://rightsstatements.org/page/CNE/1.0/":
            fail("KNIL-bewapeningsrecord mist de oorspronkelijke snapshot-rechtenstatus")
        if record.get("primaryRightsStatus") != "Publiek Domein" or record.get("reuseAllowed") is not True or record.get("downloadAvailable") is not True:
            fail("KNIL-bewapeningsrecord mist de individueel gecontroleerde primaire rechtenstatus")
        if not str(record.get("rightsEvidenceUrl", "")).startswith("https://www.nationaalarchief.nl/onderzoeken/fotocollectie/") or record.get("primaryRightsCheckedAt") != "2026-11-13":
            fail("KNIL-bewapeningsrecord mist de primaire rechtenbron of controledatum")
        if record.get("imagePublished") is not False or record.get("imageUrl") or record.get("thumbnail"):
            fail("KNIL-bronindex mag zonder afzonderlijke beeldintegratie geen beeldbestand publiceren")
    rights_audit = knil_weapons.get("primaryRightsAudit", {})
    if rights_audit.get("checkedRecords") != len(weapon_records) or rights_audit.get("downloadAvailableRecords") != len(weapon_records):
        fail("KNIL-rechtenaudit dekt niet alle records in de index")
        if not str(record.get("uri", "")).startswith("http://proxy.handle.net/10648/"):
            fail("KNIL-bewapeningsrecord mist permanente Nationaal Archief-Handle")

    scripts = re.findall(r"<script>(.*?)</script>", source, flags=re.DOTALL | re.IGNORECASE)
    if not scripts:
        fail("Inline JavaScript ontbreekt")
    if not any("loadNationaalArchiefIndex();" in block for block in scripts):
        fail("Nationaal Archief-index wordt niet geïnitialiseerd")

    required_search_terms = ("viewTerms", "Nederlandsche Oost-Indiën", "gouvernement", "interneringskamp", "krijgsgevangenkamp", "Kempeitai", "Tjimahi", "Soekaboemi", "Tasikmalaja", "Tjilatjap", "Tjihapit", "Technische Hoogeschool", "Soekamiskin", "Depot Mobiele Artillerie", "romusha", "waroeng", "Vreemde Oosterlingen", "rubberplantage", "Atjeh", "Koetaradja", "VOC", "gouverneur-generaal", "Kempeitai", "ML-KNIL", "marechaussee", "klewang", "pemoeda", "BKR", "RAPWI")
    for term in required_search_terms:
        if term.lower() not in source.lower():
            fail(f"Historische zoekterminologie ontbreekt in de tabselecties: {term}")

    print(
        f"PASS: HTML geparsed; {len(parser.ids)} IDs; {len(parser.links)} bronlinks; "
        f"{len(records)} Nationaal Archief-records; {len(rm_records)} Rijksmuseum-foto-objecten "
        f"({rm_image_count} expliciet rechtenveilige beelden); {len(weapon_records)} KNIL-bewapeningsrecords; "
        "interface-, rechten-, herkomst- en datumcontroles aanwezig."
    )
    print("NOTE: Dit is een statische contractcheck. Browser-, performance- en visuele tests worden apart uitgevoerd.")

if __name__ == "__main__":
    main()
