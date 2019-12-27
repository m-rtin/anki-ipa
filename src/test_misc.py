# -*- coding: utf-8 -*-

"""
This file is part of the Anki IPA add-on for Anki.
Test miscellaneous
Copyright: (c) 2019 m-rtin <https://github.com/m-rtin>
License: GNU AGPLv3 <https://www.gnu.org/licenses/agpl.html>
"""

import unittest
import misc


class TestMisc(unittest.TestCase):

    def test_get_words_from_field(self):
        """Check that HTML codes get removed."""
        test_str = "<b>das</b> <i>ist</i> <u>ein</u>&nbsp; &nbsp; &nbsp;<div>Test</div>"
        expected = ["das", "ist", "ein", "Test"]
        self.assertEqual(misc.get_words_from_field(test_str), expected)


if __name__ == "__main__":
    unittest.main()
