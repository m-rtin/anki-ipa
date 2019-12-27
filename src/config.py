# -*- coding: utf-8 -*-

"""
This file is part of the Anki IPA add-on for Anki.
Save Anki IPA config.
Copyright: (c) 2019 m-rtin <https://github.com/m-rtin>
License: GNU AGPLv3 <https://www.gnu.org/licenses/agpl.html>
"""

import os

from aqt import mw
from anki.hooks import addHook

ADDON_PATH = os.path.dirname(__file__)
DEFAULT_PATH = os.path.join(ADDON_PATH, "config.json")

DEFAULT_CONF = {
    "WORD_FIELD": "Front",  # default base field
    "IPA_FIELD": "IPA",  # default target field
    "defaultlangperdeck": True,  # Default to last used language per deck
    "deckdefaultlang": {},  # Map to store the default language per deck
    "lang": "ger"  # default language is Python# default language is American English
}


def sync_keys(tosync, ref):
    for key in [x for x in list(tosync.keys()) if x not in ref]:
        del (tosync[key])

    for key in [x for x in list(ref.keys()) if x not in tosync]:
        tosync[key] = ref[key]


def sync_config_with_default(col):
    anki_ipa_config_name = "anki_ipa_conf"
    if not anki_ipa_config_name in col.conf:
        col.conf[anki_ipa_config_name] = DEFAULT_CONF
    else:
        sync_keys(col.conf[anki_ipa_config_name], DEFAULT_CONF)

    col.setMod()


def setupSyncedConf():
    # If config options have changed, sync with default config first
    sync_config_with_default(mw.col)


addHook("profileLoaded", setupSyncedConf)


def getConfig():
    return mw.addonManager.getConfig(__name__)


def writeConfig(config):
    mw.addonManager.writeConfig(__name__, config)


local_conf = getConfig()
