# -*- coding: utf-8 -*-

"""
This file is part of the Anki IPA add-on for Anki.
Miscellaneous
Copyright: (c) m-rtin <https://github.com/m-rtin>
License: GNU AGPLv3 <https://www.gnu.org/licenses/agpl.html>
"""

import re

from typing import List


def get_words_from_field(field_text: str) -> List[str]:
    """ Get all the words in a given note field.

    :param field_text: text of the given field
    :return: words in the given field
    """
    clean_regex = re.compile('<.*?>')
    cleaned_textfield = re.sub(clean_regex, '', field_text)
    cleaned_textfield = cleaned_textfield.replace("&nbsp;", " ")

    return cleaned_textfield.split()
