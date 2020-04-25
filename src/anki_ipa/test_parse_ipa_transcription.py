# -*- coding: utf-8 -*-

"""
This file is part of the Anki IPA add-on for Anki.
Test parsing methods
Copyright: (c) 2019 m-rtin <https://github.com/m-rtin>
License: GNU AGPLv3 <https://www.gnu.org/licenses/agpl.html>
"""

import unittest
import parse_ipa_transcription as parse_ipa


class TestParseIpa(unittest.TestCase):

    def test_british(self):
        self.assertEqual(parse_ipa.british("box"), "bɒks")

    def test_american(self):
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

    def test_polish(self):
        self.assertEqual(parse_ipa.polish("asteroida"), "ˌastɛˈrɔjda")
        self.assertEqual(parse_ipa.polish("mały"), "ˈmawɨ")

    def test_dutch(self):
        self.assertEqual(parse_ipa.dutch("wit"), "ʋɪt")
        self.assertEqual(parse_ipa.dutch("lucht"), "lʏxt")

if __name__ == "__main__":
    unittest.main()
