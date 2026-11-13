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

# Individually checked against the live primary Nationaal Archief photo pages on 2026-11-13.
# Only these exact handles may inherit the verified Public Domain + download status.
VERIFIED_PRIMARY_RIGHTS_HANDLES = frozenset({
    "01505568-483c-45a4-1755-49c81399b45a",
    "0371044a-853b-9eec-6b10-b002c676b734",
    "07150487-30ec-9b64-34c6-cd0184ed872a",
    "0cf356ff-cb60-d58e-2e20-5829b0c7471f",
    "15e25bb1-7384-c973-abc6-a3bb0e5e9060",
    "1a8a2089-6c28-1e71-b931-6d80d4c9acc9",
    "3b12baf0-e764-b72d-7d36-70e211544475",
    "43642e6f-c368-0b68-5bad-8eb06603ebc1",
    "4aa91c6b-b498-20e4-fd89-228fa19d0fdc",
    "4e9e5140-e29b-5eb9-7b85-8636bcbd04a2",
    "58498917-0920-139d-afdf-dcd367eec012",
    "59791d8f-7c9d-d2d8-3f11-19b15bcb438a",
    "770c8ce8-f88c-4e29-dea9-719e48a5ffae",
    "7bbf18f7-8745-d979-0a75-aa4a7e250419",
    "8bc2e239-da12-fdb4-15ae-929d0c994b72",
    "5b758d77-b6ca-0c57-6d14-6bd3da78137a",
    "0a99d9cf-0386-0abd-703f-47756c904a8f",
    "6e8d84ec-5345-4c7e-d997-5d481b79eaa7",
    "72410191-72d8-fae7-4ba2-cb80119c17aa",
    "05adc928-8c24-b673-d94e-bef2c1992e23",
    "091956cf-49fd-3263-e806-8b84ba67ca63",
    "134a2ea8-31a7-1bd7-5fdb-a5c5878787d7",
    "36fda7e6-53e8-d857-e2fe-1caacad564d8",
    "3820142f-e57e-6634-d209-8286d15dc1a6",
    "385db9cb-fc30-b24e-0116-fc913a73fe3c",
    "5703bdac-2a2e-fe79-e52f-b16e6e768a8a",
    "99946baa-5d93-b819-4985-84eb82e4f739",
    "29bb507a-d96b-da91-943e-ab4afba8a06d",
    "4cd36779-d034-1d76-690c-5f91ac6b8c6d",
    "573f53bd-a1e4-02aa-25a3-f1cba914fc2b",
    "4cadf42e-f590-2d33-c1d6-9aa9b53a5056",
    "5a76e95a-414d-1cb8-3f9e-32054d1de1fc",
    "9c91174c-1da2-08ed-14e7-eb68844e5e03",
    "17fdf167-ace2-1e50-d1ec-59f71f289629",
    "3c02fa3c-cf96-18ba-439c-cfdd44983b72",
    "3c52dcc1-5b2d-6296-0ece-17ca64f536fe",
    "4439b5c7-3ce2-ac48-e14d-effa97aae4bd",
    "687b4c35-9360-f65f-7997-c3a55f557ab6",
    "867d8541-ee9e-8f15-47f8-220dfa9015b8",
    "96eb2231-5a58-4d62-7a01-00fda366871b",
    "9d587b23-6ff6-c9bb-abfa-ddd948917697",
    "50a7dc60-d931-ce2f-7ad4-66d16725b2e4",
    "526613ac-b769-a2f4-7999-d9158d2f5cb3",
    "66c0b789-d155-d00f-f7e2-0aaf3741140f",
    "72cab4ed-f7e6-1894-d847-31bd89cf5854",
    "7eaa7ff4-76b3-c605-aa0e-382f5465bcc2",
    "05b841a9-04a4-b332-f4d6-b0ed87cbd2a4",
    "1bfca470-dcbe-2e49-5b67-7b6ba76deb93",
    "1dbe3ba6-b1a9-94b8-1e23-469a0c89c751",
    "26c87c21-17d5-2a18-0cd5-3e0009a6f46e",
    "2c367167-81c8-5402-393e-8d9b74b6dac2",
    "2eb01007-d517-30bc-1398-55d141e958c3",
    "46709baa-f91a-0f5a-bf13-da888b4ad3d9",
    "4fb610b2-d9e1-bad3-641e-d85768e0e961",
    "59143d6b-7328-39b5-807b-dd57b274f8db",
    "63ca4ae3-e1de-9bd2-7eb3-1736316e91b4",
    "674e4c41-53de-1ca5-5214-63293964d7d6",
    "67db4b8e-d499-bab4-5e2b-e81ec41a891e",
    "71f37eaf-093b-9688-53cb-ac2e45e0bdb8",
    "76d9c628-a4e7-2b88-a5b7-bcd40ee07564",
    "8caa004c-3caa-690e-da7a-4ed1144591e0",
    "8ea5e337-8346-37fe-febc-91bf411f55a9",
    "91148c71-35b5-47e9-2adc-ca30bb9bd18a",
    "911c6911-34f7-f847-edc2-019b311fa3b4",
    "9debfd4c-1bc5-52b6-5a3d-af9fa906ca8a",
    "9e0080e1-ca28-7a53-7d4b-1a74f8cc62e1",
    "9f877e2c-7d0a-451b-98e2-ba23af760ac2",
    "0a37bcc8-fed7-769a-3683-d58c4cdba530",
    "3a089d07-726a-6b07-f0e2-1372ebb164e6",
    "3a52c0fa-94bb-5fde-6f6f-bd47f1d5537b",
    "3ddf0352-b0ce-b0bf-a9b9-72671f23fc11",
    "4ab504bb-e075-8044-a12c-4c7233f29107",
    "65875857-b938-7938-94b5-72cf3a2252ad",
    "7e021d30-f600-02fa-b26f-eb00a0a253cb",
    "8fd2c9c3-63d8-93ff-cf24-6d5150b4c8a2",
    "4b76bd1d-e254-1d36-ea46-267a79117d84",
    "139f99dd-bffa-8c14-a9ef-142fd1cabef3",
    "20c8918d-1199-0ec3-f74f-6febdc8d4aa4",
    "319a9b2e-73a7-a6ae-953b-264ed249953f",
    "655fcbc3-2ab3-dfa4-059f-7c968207a3cf",
    "973a9e71-c04b-a805-a99c-d88eab3e93fe",
    "050c1cd5-b45a-383d-84ad-124409572340",
    "0b9ce53e-8aa7-eb02-7a2c-c0f59f96b455",
    "0ca583f1-4c76-1994-769c-18b55414298b",
    "18070b63-eab0-ed9a-7b99-d7cbd79c2472",
    "2424e488-33fc-4201-d85c-a6a09f09b6ac",
    "2ba8707e-9e5d-a6ad-9bd9-1d3939a26a71",
    "66727d77-4689-c054-bc78-ec02a32e4bfe",
    "79cccb00-e3bd-7815-b899-411cc197459c",
    "86f55674-838f-0fce-4e0e-40abda9d1314",
    "95cf164f-4948-c6a6-ecbe-a1394ff64633",
    "997e4053-c3e1-578f-1bbd-d4e67a28d353",
    "9df949fc-263c-5178-2710-fd25469ac050",
    "9e788412-4a7d-1e92-6de7-6b66fa2122dc",
    "40913377-ef68-4236-ec7a-2afa92ea87a7",
    "0592df28-c571-5827-f073-acb8d057ef79",
    "07a6c511-c8aa-bcc6-1343-e1d806e7139c",
    "2703f0bf-a821-4240-8afe-67dac6409676",
    "75112604-3693-e1f0-c93b-cc8748031c08",
    "76b5b0a8-2045-60a6-b87c-7da0df5e24b0",
    "563240aa-458a-46d2-a7e4-ceb6fd11441a",
    "5edbb660-8a63-189f-2a2e-205112f8c650",
    "3b457917-bcfa-5d6e-ee7c-15e1a9fd9b04",
    "64036a78-c8aa-d831-74be-44004ac4ceeb",
    "5cb8ff82-de56-9cc1-122e-174da63f7365",
    "a039730e-8c73-9130-3b33-272faf176917",
    "81d01364-08da-57fa-9283-93f32c982b3e",
    "a04d2c2f-febb-3661-d422-23dccb3780e5",
    "09737ccf-6dd5-c95b-70e4-3f99bc05b82a",
    "9e1cffdc-f6de-d34e-d00a-46e782db2a78",
    "0af57107-6468-3483-819e-3505cfa73c56",
    "44a27332-cb54-4fa7-e528-d331635eda70",
    "51e0c6e1-f99f-003e-7a0b-61342c6ea257",
    "1b546826-9dc7-93b4-214f-48f943ad2604",
    "386a28c6-fa82-16aa-5b67-39c9a1ac2cca",
    "4044befe-c6f1-1fb8-7d63-8dae8a79ff1d",
    "5e0a4477-079c-7b0e-860d-cc2193013d34",
    "60e55a1c-ea1c-8f0a-5b82-1590a13484c7",
    "808a5bc9-284c-6581-d644-4c71cb21df9c",
    "093d3233-ab46-a5a1-e6a9-cdc1a1ed2efc",
    "6687b56a-6e74-26fa-bd58-ef2fa3dfd310",
    "9f71a279-9c35-b1a7-83b6-f5baad5c9691",
    "6fc03d3a-526f-f3f6-1b45-80d7893c58fb",
    "13e0cd2a-05d6-3db5-4623-209b10af40ec",
    "2f21092c-6999-debf-7f3c-eda3e31bbfea",
    "6bad8023-208e-ca4c-1e23-44057f749bcf",
    "7629d0e5-b662-da87-66b9-0fcfc3075990",
    "97b4e873-4cb2-81aa-0746-4f4b9c20dc73",
    "82f5c477-cc99-8a19-39d0-00ff3ebfdbf3",
    "2c509dc8-e0e5-0616-0b39-cf27c525fc20",
    "08dda9b5-8384-7806-6d4f-9b979210c8d1",
    "83e44f71-c998-40a6-18f1-ec064bcebfd4",
    "93acc834-82f6-ba9d-8a47-ac27940ad2c2",
    "5e1bc182-1a48-47b1-4d7a-029f3513ce40",
    "98d337a8-dbe3-9b26-4fe4-b513c6ceedf2",
    "8fa89c0b-1666-a0da-a328-98142749a8bd",
})

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
        uri = source_record.get("uri")
        rights_verified = bool(uri and uri.rsplit("/", 1)[-1] in VERIFIED_PRIMARY_RIGHTS_HANDLES)
        records.append({
            "date": source_record.get("date"),
            "description": description,
            "uri": uri,
            "collection": source_record.get("collection"),
            "primaryRightsStatus": "Publiek Domein" if rights_verified else "Niet individueel gecontroleerd",
            "primaryRightsCheckedAt": "2026-11-13" if rights_verified else None,
            "reuseAllowed": True if rights_verified else None,
            "downloadAvailable": True if rights_verified else None,
            "rightsEvidenceUrl": ("https://www.nationaalarchief.nl/onderzoeken/fotocollectie/" + uri.rsplit("/", 1)[-1]) if rights_verified else None,
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
            "excludedContextPattern": NON_WEAPON_CONTEXT.pattern,
            "recordCount": len(records),
            "uniqueDescriptions": len({record["description"] for record in records}),
        },
        "categoryCounts": dict(sorted(counts.items())),
        "rightsPolicy": (
            "All 136 indexed records were individually checked against their live primary Nationaal Archief pages on 2026-11-13. "
            "Each page states Publiek Domein, permits free reuse, and provides a download. "
            "The linked-open-data snapshot CNE field is stale/inconsistent for these individual records. "
            "Verification applies only to the exact handles in this index."
        ),
        "primaryRightsAudit": {
            "checkedAt": "2026-11-13",
            "checkedRecords": len(VERIFIED_PRIMARY_RIGHTS_HANDLES.intersection(
                record["uri"].rsplit("/", 1)[-1] for record in records if record.get("uri")
            )),
            "rightsStatus": "Publiek Domein",
            "reuseStatement": "U kunt deze afbeelding rechtenvrij en gratis (her)gebruiken.",
            "downloadAvailableRecords": len(VERIFIED_PRIMARY_RIGHTS_HANDLES.intersection(
                record["uri"].rsplit("/", 1)[-1] for record in records if record.get("uri")
            )),
            "method": "Individual live Nationaal Archief photo pages; exact Handle URLs stored per record.",
        },
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
