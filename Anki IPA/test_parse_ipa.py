# -*- coding: utf-8 -*-

import unittest
import parse_ipa


class TestParseIpa(unittest.TestCase):

    # TODO test special cases

    def test_british(self):
        self.assertEqual(parse_ipa.british("go"), "ɡəʊ")
        self.assertEqual(parse_ipa.british("box"), "bɒks")

    def test_american(self):
        self.assertEqual(parse_ipa.american("go"), "ɡoʊ")
        self.assertEqual(parse_ipa.american("box"), "bɑːks")

    def test_russian(self):
        self.assertEqual(parse_ipa.russian("спасибо"), "spɐˈsʲibə")


if __name__ == "__main__":
    unittest.main()
