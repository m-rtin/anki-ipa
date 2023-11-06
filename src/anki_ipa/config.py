# -*- coding: utf-8 -*-

"""
This file is part of the Anki IPA add-on for Anki.
Synchronize addon configuration.
Copyright: (c) m-rtin <https://github.com/m-rtin>
License: GNU AGPLv3 <https://www.gnu.org/licenses/agpl.html>
"""

from aqt import mw


def setup_synced_config() -> None:
    """Create new configuration if not already done."""
    conf_name = "anki_ipa_conf"

    if conf_name not in mw.col.conf:
        mw.col.conf[conf_name] = {
            "defaultlangperdeck": 1,
            "deckdefaultlang": {},  # default addon language for specific decks
            "lang": "eng"
        }

    mw.col.setMod()
