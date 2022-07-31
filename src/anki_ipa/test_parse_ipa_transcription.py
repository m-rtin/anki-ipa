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
        self.assertEqual(parse_ipa.british("charcoal"), "ˈtʃɑːkəʊl")
        self.assertEqual(parse_ipa.british("dog"), "dɒɡ")
        self.assertEqual(parse_ipa.british("thumb"), "θʌm")

    def test_american(self):
        self.assertEqual(parse_ipa.american("charcoal"), "ˈCHärˌkōl, ˈtʃɑrˌkoʊl")
        self.assertEqual(parse_ipa.american("dog"), "dôɡ, dɔɡ")
        self.assertEqual(parse_ipa.american("thumb"), "THəm, θəm")

    def test_russian(self):
        self.assertEqual(parse_ipa.russian("спасибо"), "spɐˈsʲibə")

    def test_french(self):
        self.assertEqual(parse_ipa.french("occasion"), "ɔkazjɔ̃, əˈkeɪʒən")
        self.assertEqual(parse_ipa.french("rencontre"), "ʁɑ̃kɔ̃tʁ")

    def test_spanish(self):
        self.assertEqual(parse_ipa.spanish("eternidad"), "eteɾniˈðað")

    def test_german(self):
        self.assertEqual(parse_ipa.german("Land"), "lant")
        self.assertEqual(parse_ipa.german("Kind"), "kɪnt")
        self.assertEqual(parse_ipa.german("spielen"), "ˈʃpiːlən")
        self.assertEqual(parse_ipa.german("blau"), "blaʊ̯")

    def test_polish(self):
        self.assertEqual(parse_ipa.polish("asteroida"), "ˌastɛˈrɔjda")
        self.assertEqual(parse_ipa.polish("mały"), "ˈmawɨ")

    def test_dutch(self):
        self.assertEqual(parse_ipa.dutch("wit"), "wit, wɪt, ʋɪt")
        self.assertEqual(parse_ipa.dutch("lucht"), "lʏxt")

if __name__ == "__main__":
    unittest.main()
