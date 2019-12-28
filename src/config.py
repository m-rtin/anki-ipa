# -*- coding: utf-8 -*-

"""
This file is part of the Anki IPA add-on for Anki.
Synch addon configuration.
Copyright: (c) m-rtin <https://github.com/m-rtin>
License: GNU AGPLv3 <https://www.gnu.org/licenses/agpl.html>
"""

from aqt import mw

from . import consts


def sync_keys(tosync, ref):
    for key in [x for x in list(tosync.keys()) if x not in ref]:
        del (tosync[key])

    for key in [x for x in list(ref.keys()) if x not in tosync]:
        tosync[key] = ref[key]


def sync_config_with_default(col):
    if not 'anki_ipa_conf' in col.conf:
        col.conf['anki_ipa_conf'] = consts.DEFAULT_CONFIG
    else:
        sync_keys(col.conf['anki_ipa_conf'], consts.DEFAULT_CONFIG)

    col.setMod()


def setup_synced_config():
    sync_config_with_default(mw.col)
