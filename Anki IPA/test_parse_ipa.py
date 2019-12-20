# -*- coding: utf-8 -*-

import unittest
import parse_ipa


class TestParseIpa(unittest.TestCase):

    def test_british(self):
        self.assertEqual(parse_ipa.british("go"), "ɡəʊ")
        self.assertEqual(parse_ipa.british("box"), "bɒks")

    def test_american(self):
        self.assertEqual(parse_ipa.american("go"), "ɡoʊ")
        self.assertEqual(parse_ipa.american("box"), "bɑːks")

    def test_russian(self):
        self.assertEqual(parse_ipa.russian("спасибо"), "spɐˈsʲibə")

    def test_french(self):
        self.assertEqual(parse_ipa.french("occasion"), "ɔ.ka.zjɔ̃")
        self.assertEqual(parse_ipa.french("rencontre"), "ʁɑ̃.kɔ̃tʁ")

    def test_spanish(self):
        self.assertEqual(parse_ipa.spanish("eternidad"), "e.teɾ.niˈðað")

    def test_german(self):
        self.assertEqual(parse_ipa.german("Land"), "lant")


if __name__ == "__main__":
    unittest.main()
