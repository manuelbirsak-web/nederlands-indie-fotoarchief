#!/usr/bin/env python3
"""Harvest a bounded, rights-aware metadata and image index from Rijksmuseum Data Services."""
from __future__ import annotations

import json
import re
import sys
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "assets" / "rijksmuseum.json"
SEARCH_ENDPOINT = "https://data.rijksmuseum.nl/search/collection"
PAGE_LIMIT = 100
MAX_OBJECTS = 350
WORKERS = 6
ALLOWED_IMAGE_RIGHTS = {
    "https://creativecommons.org/publicdomain/mark/1.0/",
    "https://creativecommons.org/publicdomain/zero/1.0/",
}

# Search API parameters are combined with AND. Each term is a separate query,
# and result IDs are deduplicated before object metadata is resolved.
SEARCH_TERMS = [
    ("Nederlands-Indië", 80),
    ("Dutch East Indies", 35),
    ("Bandung", 30),
    ("Bandoeng", 25),
    ("Java", 45),
    ("Batavia", 25),
    ("Buitenzorg", 15),
    ("Semarang", 15),
    ("Soerabaja", 15),
    ("KNIL", 10),
    ("Sumatra", 20),
]

PLACE_PATTERNS = {
    "bandung": r"\b(?:bandoeng|bandung)\b",
    "batavia": r"\b(?:batavia|jakarta)\b",
    "bogor": r"\b(?:buitenzorg|bogor)\b",
    "semarang": r"\bsemarang\b",
    "surabaya": r"\b(?:soerabaja|surabaya)\b",
    "yogyakarta": r"\b(?:djokja|djocja|yogyakarta|jogjakarta)\b",
    "malang": r"\bmalang\b",
}
JAVA_CONTEXT = re.compile(
    r"\b(?:java|bandoeng|bandung|batavia|jakarta|buitenzorg|bogor|semarang|"
    r"soerabaja|surabaya|djokja|djocja|yogyakarta|jogjakarta|malang|"
    r"poerwokerto|tjimahi|cheribon|garoet|tjikampek)\b",
    re.I,
)
TOPIC_PATTERNS = {
    "knil": re.compile(r"\bknil\b|koninklijk nederlands(?:ch)?[- ]indisch leger|nederlands[- ]indisch leger", re.I),
    "military": re.compile(
        r"\b(?:militair(?:e|en)?|solda(?:at|ten)|soldier(?:s)?|sergeant|officier|kapitein|"
        r"luitenant|generaal|bataljon|eskadron|compagnie|troepen|geweer|wapen(?:s)?|"
        r"tank(?:s)?|kazern(?:e|es)|vliegveld|artillerie|leger)\b|\bknil\b",
        re.I,
    ),
    "decolonization": re.compile(
        r"\b(?:bersiap|tni|pemoeda|republikeins(?:e)?|republiek indonesia|"
        r"onafhankelijkheidsstrijd|onafhankelijkheid|indonesian national revolution|"
        r"indonesian war of independence|agresi militer|politionele acties?|"
        r"perang kemerdekaan|perang revolusi|linggadjati|renville|roem[- ]royen|"
        r"soevereiniteitsoverdracht)\b",
        re.I,
    ),
    "bersiap": re.compile(r"\bbersiap\b", re.I),
    "society": re.compile(
        r"\b(?:bevolking|inwoner(?:s)?|familie|gezin|vrouw(?:en)?|kind(?:eren)?|school|"
        r"onderwijs|markt|pasar|dorp|desa|kampong|werk(?:zaamheden)?|arbeid|boer(?:en)?|"
        r"landbouw|feest|bruiloft|huwelijk|dagelijks leven|daily life|family|market)\b",
        re.I,
    ),
    "architecture": re.compile(
        r"\b(?:gebouw|gebouwen|architectuur|architect|woning|huis|huizen|kantoor|hotel|"
        r"kerk|moskee|tempel|straat|plein|aloon[- ]?aloon|station|brug|fabriek|"
        r"schoolgebouw|building|house|street)\b",
        re.I,
    ),
    "transport": re.compile(
        r"\b(?:trein|spoor(?:baan|weg)?|tram|station|haven|schip|vliegtuig|luchtvaart|"
        r"tank|voertuig|auto|brug|veerboot|train|railway|harbour|ship|aircraft)\b",
        re.I,
    ),
    "culture": re.compile(
        r"\b(?:muziek|dans|dansers|ceremonie|religie|kerk|moskee|tempel|feest|"
        r"theater|toneel|kunst|traditie|music|dance|ceremony|religion)\b",
        re.I,
    ),
    "landscape": re.compile(
        r"\b(?:landschap|berg(?:en)?|vulkaan|rivier|plantage|bos|kust|meer|"
        r"sawah|rijstveld|landscape|mountain|river|plantation)\b",
        re.I,
    ),
}


def request_json(url: str, attempts: int = 3) -> dict:
    """Fetch JSON with bounded retries and a descriptive user agent."""
    last_error: Exception | None = None
    for attempt in range(attempts):
        try:
            request = Request(
                url,
                headers={
                    "Accept": "application/ld+json, application/json",
                    "User-Agent": "IndischBeeldarchief/1.0 (public cultural heritage index)",
                },
            )
            with urlopen(request, timeout=35) as response:
                if response.status != 200:
                    raise RuntimeError(f"HTTP {response.status} for {url}")
                return json.loads(response.read().decode("utf-8"))
        except (HTTPError, URLError, TimeoutError, json.JSONDecodeError, RuntimeError) as exc:
            last_error = exc
            if attempt + 1 < attempts:
                time.sleep(1.5 * (attempt + 1))
    raise RuntimeError(f"Request failed after {attempts} attempts: {url}: {last_error}")


def search_objects(term: str, per_term: int) -> tuple[list[tuple[str, str]], dict]:
    params = urlencode({
        "description": term,
        "type": "photograph",
        "imageAvailable": "true",
    })
    response = request_json(f"{SEARCH_ENDPOINT}?{params}")
    items = response.get("orderedItems", [])
    total = (response.get("partOf") or {}).get("totalItems")
    return (
        [(item.get("id", ""), term) for item in items[:per_term] if item.get("id")],
        {"term": term, "available": total, "selectedFromFirstPage": min(len(items), per_term)},
    )


def values(record: dict, array_key: str) -> list[str]:
    return [
        str(item.get("content"))
        for item in record.get(array_key, [])
        if isinstance(item, dict) and item.get("content")
    ]


def object_number(obj: dict) -> str | None:
    for item in obj.get("identified_by", []):
        if item.get("type") != "Identifier":
            continue
        classifiers = item.get("classified_as", [])
        if any(entry.get("id") == "https://id.rijksmuseum.nl/22015218" for entry in classifiers):
            return item.get("content")
    return None


def photograph_type(obj: dict) -> bool:
    notations = [
        str(value.get("@value", "")).casefold()
        for cls in obj.get("classified_as", [])
        for value in cls.get("notation", [])
    ]
    return "photograph" in notations or "foto" in notations


def image_evidence(obj: dict) -> tuple[str | None, str | None, list[str]]:
    """Return an image URL only where the image object itself states an allowed right."""
    for subject in obj.get("subject_of", []):
        for digital in subject.get("digitally_carried_by", []):
            access_points = [
                entry.get("id", "")
                for entry in digital.get("access_point", [])
                if isinstance(entry, dict)
            ]
            image_url = next(
                (url for url in access_points if url.startswith("https://iiif.micr.io/")),
                None,
            )
            if not image_url:
                continue
            rights_urls = [
                str(entry.get("content"))
                for entry in digital.get("referred_to_by", [])
                if isinstance(entry, dict)
                and isinstance(entry.get("content"), str)
                and entry.get("content").startswith("https://")
            ]
            # The allowlist is deliberately strict. Object-metadata CC0 is not
            # used as a substitute for the rights statement on the image itself.
            if rights_urls and all(url in ALLOWED_IMAGE_RIGHTS for url in rights_urls):
                return image_url, rights_urls[0], rights_urls
            return None, None, rights_urls
    return None, None, []


def classify_record(text: str) -> tuple[list[str], list[str]]:
    topics = [label for label, pattern in TOPIC_PATTERNS.items() if pattern.search(text)]
    places = [label for label, pattern in PLACE_PATTERNS.items() if pattern.search(text)]
    if JAVA_CONTEXT.search(text):
        places.append("java")
        if not any(place in places for place in PLACE_PATTERNS):
            places.append("other-java")
    if re.search(r"\b(?:sumatra|sumatera|atjeh|aceh|padang|palembang|medan)\b", text, re.I):
        places.append("sumatra")
    if re.search(r"\b(?:borneo|kalimantan|celebes|sulawesi|makassar)\b", text, re.I):
        places.append("other-islands")
    return sorted(set(topics)), sorted(set(places))


def extract_record(object_uri: str, search_terms: list[str]) -> dict | None:
    object_id = object_uri.rstrip("/").split("/")[-1]
    obj = request_json(f"https://data.rijksmuseum.nl/{object_id}?_profile=la-framed")
    if not photograph_type(obj):
        return None

    names = [item.get("content") for item in obj.get("identified_by", []) if item.get("type") == "Name" and item.get("content")]
    title = names[0] if names else None
    production = obj.get("produced_by") or {}
    timespan = production.get("timespan") or {}
    dates = values(timespan, "identified_by")
    date = dates[0] if dates else None

    descriptions = [
        item.get("content")
        for item in obj.get("referred_to_by", [])
        if item.get("content")
    ]
    # Use the record's descriptive text when the Linked Art classification marks it
    # as the object's description; do not substitute later annotations or donor notes.
    description = None
    for item in obj.get("referred_to_by", []):
        classifiers = {entry.get("id") for entry in item.get("classified_as", [])}
        if "http://vocab.getty.edu/aat/300435452" in classifiers and item.get("content"):
            description = item["content"]
            break

    creators = []
    for part in production.get("part", []):
        for item in part.get("referred_to_by", []):
            content = item.get("content")
            if isinstance(content, str) and re.match(r"^(?:fotograaf|photographer):", content, re.I):
                creators.append(content)
    creator = next(iter(creators), None)

    image_url, image_rights_url, image_rights = image_evidence(obj)
    all_text = " ".join([title or "", description or "", " ".join(descriptions), " ".join(search_terms)])
    topics, places = classify_record(all_text)

    if not title and not description:
        return None

    return {
        "id": object_id,
        "objectNumber": object_number(obj),
        "title": title or description or "Object zonder titel",
        "otherTitles": names[1:4],
        "description": description,
        "date": date,
        "creator": creator,
        "objectUrl": object_uri,
        "imageUrl": image_url,
        "imageRightsUrl": image_rights_url,
        "imageRightsEvidence": image_rights,
        "imageUnavailableReason": None if image_url else "Geen expliciete Public Domain Mark/CC0-verklaring gevonden voor het digitale beeld",
        "searchTerms": sorted(set(search_terms)),
        "topics": topics,
        "places": places,
        "recordType": "photograph",
    }


def main() -> int:
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    try:
        collected: dict[str, set[str]] = {}
        search_summaries = []
        for term, per_term in SEARCH_TERMS:
            results, summary = search_objects(term, per_term)
            search_summaries.append(summary)
            for object_uri, search_term in results:
                collected.setdefault(object_uri, set()).add(search_term)
            if len(collected) >= MAX_OBJECTS:
                break

        candidates = list(collected.items())[:MAX_OBJECTS]
        records_by_id: dict[str, dict] = {}
        failures = 0
        with ThreadPoolExecutor(max_workers=WORKERS) as executor:
            futures = {
                executor.submit(extract_record, uri, sorted(terms)): uri
                for uri, terms in candidates
            }
            for future in as_completed(futures):
                try:
                    record = future.result()
                    if record:
                        records_by_id[record["id"]] = record
                except Exception as exc:
                    failures += 1
                    print(f"WARN: {futures[future]}: {exc}", file=sys.stderr)

        records = sorted(
            records_by_id.values(),
            key=lambda item: (item.get("date") or "9999", (item.get("title") or "").casefold()),
        )
        if len(records) < 20:
            raise RuntimeError(f"Only {len(records)} valid photograph records; previous snapshot retained")

        safe_images = sum(bool(record["imageUrl"]) for record in records)
        topic_counts = Counter(topic for record in records for topic in record["topics"])
        place_counts = Counter(place for record in records for place in record["places"])
        payload = {
            "schemaVersion": 1,
            "source": "Rijksmuseum Data Services — Search API and Linked Art",
            "sourceUrl": "https://data.rijksmuseum.nl/docs/search",
            "snapshotDate": datetime.now(timezone.utc).isoformat(),
            "count": len(records),
            "candidateCount": len(candidates),
            "searches": search_summaries,
            "failedObjectLookups": failures,
            "imageCount": safe_images,
            "metadataOnlyCount": len(records) - safe_images,
            "imageRightsPolicy": "Only the image-level Public Domain Mark 1.0 or CC0 1.0 statements are displayed as thumbnails. Object-level metadata CC0 is not treated as an image licence.",
            "topicCounts": dict(sorted(topic_counts.items())),
            "placeCounts": dict(sorted(place_counts.items())),
            "records": records,
        }
        TARGET.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"PASS: refreshed {len(records)} Rijksmuseum photograph records from {len(candidates)} object candidates.")
        print(f"Images with explicit PD Mark/CC0 image rights: {safe_images}; metadata-only: {len(records) - safe_images}")
        print("Topics:", json.dumps(payload["topicCounts"], ensure_ascii=False))
        print("Places:", json.dumps(payload["placeCounts"], ensure_ascii=False))
        return 0
    except Exception as exc:
        if TARGET.exists():
            print(f"FAIL: Rijksmuseum refresh failed; retained previous snapshot: {exc}", file=sys.stderr)
            return 1
        print(f"FAIL: no Rijksmuseum snapshot available: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
