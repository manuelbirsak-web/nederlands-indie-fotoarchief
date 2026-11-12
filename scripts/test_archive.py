#!/usr/bin/env python3
"""Unit tests for evidence-based Nationaal Archief metadata classification."""
from __future__ import annotations

import unittest

from harvest_nationaal_archief import classify_record


class ArchiveClassificationTests(unittest.TestCase):
    def test_knil_is_only_assigned_when_description_says_knil(self) -> None:
        topics, places = classify_record("Stafmuziek KNIL omringd door publiek", "1947-01-19")
        self.assertIn("knil", topics)
        self.assertIn("military", topics)
        self.assertIn("java", places)

    def test_military_description_does_not_invent_knil(self) -> None:
        topics, _ = classify_record("Een Nederlandse soldaat bij een voertuig in Batavia", "1948-01-01")
        self.assertIn("military", topics)
        self.assertNotIn("knil", topics)

    def test_collection_name_is_not_used_for_classification(self) -> None:
        topics, _ = classify_record("Een gezin op de markt in Batavia")
        self.assertIn("society", topics)
        self.assertNotIn("military", topics)
        # The caller must classify the description; a collection label is never an argument.

    def test_year_alone_never_assigns_bersiap(self) -> None:
        topics, _ = classify_record("Straatbeeld in Bandoeng", "1946-01-01")
        self.assertNotIn("bersiap", topics)
        self.assertNotIn("decolonization", topics)

    def test_bersiap_requires_explicit_source_term(self) -> None:
        topics, _ = classify_record("Foto tijdens de Bersiap-periode in Batavia", "1946-01-01")
        self.assertIn("bersiap", topics)
        self.assertIn("decolonization", topics)

    def test_tni_is_decolonization_context_but_not_automatically_bersiap(self) -> None:
        topics, _ = classify_record("Overleg met TNI-commandant bij Buitenzorg", "1948-01-01")
        self.assertIn("decolonization", topics)
        self.assertNotIn("bersiap", topics)

    def test_historical_place_aliases_are_normalized(self) -> None:
        topics, places = classify_record("Het station van Bandoeng in de jaren dertig")
        self.assertIn("java", places)
        self.assertIn("bandung", places)
        self.assertIn("transport", topics)

    def test_other_java_is_separate_from_named_city(self) -> None:
        _, places = classify_record("Een overzicht van het landschap op Java")
        self.assertIn("java", places)
        self.assertIn("other-java", places)
        self.assertNotIn("bandung", places)


if __name__ == "__main__":
    unittest.main(verbosity=2)
