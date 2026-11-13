#!/usr/bin/env python3
"""Tests for the reproducible KNIL armament metadata index."""
from __future__ import annotations

import unittest

from build_knil_weapons_index import build_index, category_for


class KnilWeaponsIndexTests(unittest.TestCase):
    def record(self, description, uri="http://proxy.handle.net/10648/test", topics=None, rights="http://rightsstatements.org/page/CNE/1.0/"):
        return {
            "date": "1947-01-01",
            "description": description,
            "uri": uri,
            "collection": "Fotocollectie Dienst voor Legercontacten Indonesië",
            "rights": rights,
            "topics": topics if topics is not None else ["knil", "military"],
            "places": [],
        }

    def test_includes_knil_bren_description_as_metadata_only(self):
        archive = {"schemaVersion": 2, "snapshotDate": "2026-11-12T00:00:00Z", "records": [
            self.record("KNIL-militair met brengun", "http://proxy.handle.net/10648/a")
        ]}
        result = build_index(archive)
        self.assertEqual(result["selection"]["recordCount"], 1)
        self.assertEqual(result["records"][0]["category"], "Machinegeweren en machinepistolen")
        self.assertFalse(result["records"][0]["imagePublished"])
        self.assertEqual(result["records"][0]["rights"], "http://rightsstatements.org/page/CNE/1.0/")
        self.assertEqual(result["sourceSnapshot"], archive["snapshotDate"])

    def test_excludes_non_knil_weapon_record(self):
        archive = {"schemaVersion": 2, "snapshotDate": "2026-11-12T00:00:00Z", "records": [
            self.record("Nederlandse soldaat met geweer", topics=["military"])
        ]}
        self.assertEqual(build_index(archive)["records"], [])

    def test_excludes_knil_records_without_weapon_terms(self):
        archive = {"schemaVersion": 2, "snapshotDate": "2026-11-12T00:00:00Z", "records": [
            self.record("KNIL-militairen poseren voor een groepsfoto")
        ]}
        self.assertEqual(build_index(archive)["records"], [])

    def test_excludes_contextual_weapon_word_matches(self):
        excluded = [
            "Wapenbroeders bij het afscheid van KNIL-militairen",
            "Het Wapen der Genie viert een jubileum",
            "KNIL-militairen krijgen les in ongewapende zelfverdediging",
            "Kjai Dophir roept op verborgen wapens in te leveren",
        ]
        for description in excluded:
            with self.subTest(description=description):
                archive = {"schemaVersion": 2, "snapshotDate": "2026-11-12T00:00:00Z", "records": [
                    self.record(description)
                ]}
                self.assertEqual(build_index(archive)["records"], [])

    def test_weapon_categories_are_search_aids(self):
        self.assertEqual(category_for("Stuart tank van een KNIL eskadron"), "Pantserwagens en tanks")
        self.assertEqual(category_for("Twee KNIL-militairen bij Vickers mitrailleur"), "Machinegeweren en machinepistolen")
        self.assertEqual(category_for("KNIL-afdeling veldartillerie met mortier"), "Artillerie en mortieren")
        self.assertEqual(category_for("KNIL-militair met bajonet op geweer"), "Geweerschutters en handwapens")
        self.assertEqual(category_for("KNIL-militair met wapens"), "Overige bewapening")

    def test_duplicates_with_distinct_permanent_handles_are_preserved(self):
        archive = {"schemaVersion": 2, "snapshotDate": "2026-11-12T00:00:00Z", "records": [
            self.record("KNIL-militair met geweer", "http://proxy.handle.net/10648/a"),
            self.record("KNIL-militair met geweer", "http://proxy.handle.net/10648/b"),
        ]}
        result = build_index(archive)
        self.assertEqual(result["selection"]["recordCount"], 2)
        self.assertEqual(result["selection"]["uniqueDescriptions"], 1)


if __name__ == "__main__":
    unittest.main()
