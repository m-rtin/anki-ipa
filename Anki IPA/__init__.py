# -*- coding: utf-8 -*-
import urllib

from anki.hooks import addHook, wrap
from aqt.utils import showInfo
from aqt.editor import Editor
from aqt import mw

import os
import re

from . import parse_ipa

ADDONPATH = os.path.dirname(__file__)
ICONPATH = os.path.join(ADDONPATH, "icons", "button.png")
CONFIG = mw.addonManager.getConfig(__name__)

LANGUAGES_MAP = {'eng_b': 'british', 'eng_a': 'american', 'ru': 'russian'}

select_elm = ("""<select onchange='pycmd("shLang:" +"""
              """ this.selectedOptions[0].text)' """
              """style='vertical-align: top;'>{}</select>""")


def paste_ipa(editor):
    lang_alias = editor.ipa_lang_alias
    note = editor.note

    try:
        input = note[CONFIG["WORD_FIELD"]]
    except KeyError:
        showInfo(f"Field '{CONFIG['WORD_FIELD']}' doesn't exist.")
        return

    words = strip_list(re.findall(r"[\w']+", input))

    try:
        ipa = parse_ipa.transcript(words=words, language=lang_alias)
    except urllib.error.HTTPError:
        showInfo("IPA not found.")
        return

    try:
        note[CONFIG["IPA_FIELD"]] = ipa
    except KeyError:
        showInfo(f"Field '{CONFIG['IPA_FIELD']}' doesn't exist.")
        return

    editor.loadNote()
    editor.web.setFocus()
    editor.web.eval("focusField(%d);" % editor.currentField)


def strip_list(list_):
    codes = ["nbsp", "i", "b", "u"]
    return [element.lower() for element in list_ if element not in codes]


def get_deck_name(mw):
    try:
        deck_name = mw.col.decks.current()['name']
    except AttributeError:
        # No deck opened?
        deck_name = None
    return deck_name


def get_default_lang(mw):
    lang = CONFIG['lang']
    if CONFIG['defaultlangperdeck']:
        deck_name = get_deck_name(mw)
        if deck_name and deck_name in CONFIG['deckdefaultlang']:
            lang = CONFIG['deckdefaultlang'][deck_name]
    return lang


def on_setup_buttons(buttons, editor):
    button = editor.addButton(ICONPATH, "IPA", paste_ipa)
    buttons.append(button)

    # HTML "combobox"
    previous_lang = get_default_lang(mw)

    option_str = """<option>{}</option>"""
    options = []

    selection = sorted(LANGUAGES_MAP.keys(), key=str.lower)

    options.append(option_str.format(previous_lang))
    for lang in selection:
        if option_str.format(lang) not in options:
            options.append(option_str.format(lang))

    combo = select_elm.format("".join(options))
    buttons.append(combo)

    return buttons


def set_default_lang(mw, lang):
    CONFIG['lang'] = lang  # Always update the overall default
    if CONFIG['defaultlangperdeck']:
        deck_name = get_deck_name(mw)
        if deck_name:
            CONFIG['deckdefaultlang'][deck_name] = lang


def on_ipa_language_select(editor, lang):
    try:
        alias = LANGUAGES_MAP[lang]
    except KeyError as e:
        print(e)
        showInfo("mist")
        editor.ipa_lang_alias = ""
        return False
    set_default_lang(mw, lang)
    editor.ipa_lang_alias = alias


def init_ipa(editor, *args, **kwargs):
    # Get the last selected language (or the default language if the user
    # has never chosen any)
    previous_lang = get_default_lang(mw)
    editor.ipa_lang_alias = LANGUAGES_MAP.get(previous_lang, "")


def onBridgeCmd(ed, cmd, _old):
    if not cmd.startswith("shLang"):
        return _old(ed, cmd)
    (type, lang) = cmd.split(":")
    on_ipa_language_select(ed, lang)


addHook("setupEditorButtons", on_setup_buttons)
Editor.onBridgeCmd = wrap(Editor.onBridgeCmd, onBridgeCmd, "around")
Editor.__init__ = wrap(Editor.__init__, init_ipa)
