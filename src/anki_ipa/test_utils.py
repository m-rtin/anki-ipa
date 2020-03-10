# -*- coding: utf-8 -*-

"""
This file is part of the Anki IPA add-on for Anki.
Test miscellaneous
Copyright: (c) 2019 m-rtin <https://github.com/m-rtin>
License: GNU AGPLv3 <https://www.gnu.org/licenses/agpl.html>
"""

import unittest
import utils


class TestMisc(unittest.TestCase):

    def test_get_words_from_field(self):
        """Check that HTML codes get removed."""
        test_str = "<b>das</b> <i>ist</i> <u>ein</u>&nbsp; &nbsp; &nbsp;<div>Test</div>"
        expected = ["das", "ist", "ein", "Test"]
        self.assertEqual(utils.get_words_from_field(test_str), expected)

        test_str = ('<i>diffusée&nbsp; &nbsp;</i><h1>lumière&nbsp;&nbsp;</h1><div>'
                    '<span style="color: rgb(34, 34, 34);">latin</span><br></div>')
        expected = ["diffusée", "lumière", "latin"]
        self.assertEqual(utils.get_words_from_field(test_str), expected)


if __name__ == "__main__":
    unittest.main()
