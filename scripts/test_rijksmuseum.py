#!/usr/bin/env python3
"""Unit tests for Rijksmuseum linked-art extraction and image-rights policy."""
from __future__ import annotations

import unittest

from harvest_rijksmuseum import classify_record, image_evidence, photograph_type


class RijksmuseumIndexTests(unittest.TestCase):
    def test_bandung_alias_is_normalized_from_record_metadata(self) -> None:
        topics, places = classify_record("Een dam nabij Bandung op Java")
        self.assertIn("bandung", places)
        self.assertIn("java", places)

    def test_bersiap_is_narrower_than_decolonization(self) -> None:
        topics, _ = classify_record("Een TNI-eenheid in Semarang")
        self.assertIn("decolonization", topics)
        self.assertNotIn("bersiap", topics)
        topics, _ = classify_record("Fotoreeks over de Bersiap in Batavia")
        self.assertIn("bersiap", topics)

    def test_historical_java_aliases_expand_place_classification(self) -> None:
        _, places = classify_record("Een straatbeeld in Soerakarta en de Preanger")
        self.assertIn("surakarta", places)
        self.assertIn("priangan", places)
        self.assertIn("java", places)

    def test_peta_is_not_misclassified_as_knil(self) -> None:
        topics, _ = classify_record("PETA-soldaten oefenen op Java")
        self.assertIn("military", topics)
        self.assertNotIn("knil", topics)

    def test_culture_and_daily_life_terms_are_classified(self) -> None:
        topics, _ = classify_record("Batik, gamelan en wajang tijdens pasar malam")
        self.assertIn("culture", topics)
        self.assertIn("society", topics)

    def test_non_photograph_album_is_not_a_single_photograph(self) -> None:
        self.assertFalse(photograph_type({
            "classified_as": [{"notation": [{"@value": "photograph album"}, {"@value": "fotoalbum"}]}]
        }))
        self.assertTrue(photograph_type({
            "classified_as": [{"notation": [{"@value": "albumblad"}, {"@value": "photograph"}]}]
        }))

    def test_linked_art_notation_may_be_a_single_object(self) -> None:
        self.assertTrue(photograph_type({
            "classified_as": [{"notation": {"@language": "nl", "@value": "foto"}}]
        }))

    def test_image_with_explicit_public_domain_mark_is_allowed(self) -> None:
        image, rights, evidence = image_evidence({
            "subject_of": [{
                "digitally_carried_by": [{
                    "access_point": [{"id": "https://iiif.micr.io/ABC/full/max/0/default.jpg"}],
                    "referred_to_by": [{"content": "https://creativecommons.org/publicdomain/mark/1.0/"}],
                }]
            }]
        })
        self.assertEqual(image, "https://iiif.micr.io/ABC/full/max/0/default.jpg")
        self.assertEqual(rights, "https://creativecommons.org/publicdomain/mark/1.0/")
        self.assertTrue(evidence)

    def test_in_copyright_image_is_not_exposed(self) -> None:
        image, rights, evidence = image_evidence({
            "subject_of": [{
                "digitally_carried_by": [{
                    "access_point": [{"id": "https://iiif.micr.io/ABC/full/max/0/default.jpg"}],
                    "referred_to_by": [{"content": "https://rightsstatements.org/vocab/InC/1.0/"}],
                }]
            }]
        })
        self.assertIsNone(image)
        self.assertIsNone(rights)
        self.assertIn("https://rightsstatements.org/vocab/InC/1.0/", evidence)

    def test_object_metadata_cc0_does_not_grant_image_rights(self) -> None:
        image, rights, evidence = image_evidence({
            "subject_to": [{
                "classified_as": [{"id": "https://creativecommons.org/publicdomain/zero/1.0/"}]
            }],
            "subject_of": [{
                "digitally_carried_by": [{
                    "access_point": [{"id": "https://iiif.micr.io/ABC/full/max/0/default.jpg"}],
                    "referred_to_by": [],
                }]
            }]
        })
        self.assertIsNone(image)
        self.assertIsNone(rights)
        self.assertEqual(evidence, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
