# -*- coding: utf-8 -*-

"""
This file is part of the Anki IPA add-on for Anki.
Miscellaneous
Copyright: (c) m-rtin <https://github.com/m-rtin>
License: GNU AGPLv3 <https://www.gnu.org/licenses/agpl.html>
"""

import re
from .typing import List


def get_words_from_field(field_text: str) -> List[str]:
    """ Get all the words in a given note field.

    :param field_text: text of the given field
    :return: words in the given field
    """
    words = strip_list(re.findall(r"[\w']+", field_text))
    return words


def strip_list(list_: List[str]) -> List[str]:
    """ Removes HTML code from list elements.

    :param list_: list of IPA transcriptions
    :return: cleaned list (no HTML code)
    """
    codes = ["nbsp", "i", "b", "u", "div", "br"]
    return [element for element in list_ if element not in codes]
