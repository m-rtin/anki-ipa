# -*- coding: utf-8 -*-

import unittest
import parse_ipa


class TestParseIpa(unittest.TestCase):

    # TODO test special cases

    def test_get_british_ipa(self):
        self.assertEqual(parse_ipa.get_british_ipa("go"), "ɡəʊ")
        self.assertEqual(parse_ipa.get_british_ipa("box"), "bɒks")

    def test_get_american_ipa(self):
        self.assertEqual(parse_ipa.get_american_ipa("go"), "ɡoʊ")
        self.assertEqual(parse_ipa.get_american_ipa("box"), "bɑːks")

    def test_get_russian_ipa(self):
        self.assertEqual(parse_ipa.get_russian_ipa("спасибо"), "spɐˈsʲibə")


if __name__ == "__main__":
    unittest.main()
