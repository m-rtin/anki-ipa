# -*- coding: utf-8 -*-

from anki.hooks import addHook, wrap
from aqt.utils import showInfo
from aqt.editor import Editor
from aqt import mw

import os
import re
from .typing import List

from . import parse_ipa

ADDONPATH = os.path.dirname(__file__)
ICONPATH = os.path.join(ADDONPATH, "icons", "button.png")
CONFIG = mw.addonManager.getConfig(__name__)

LANGUAGES_MAP = {
    'eng_b': 'british',
    'eng_a': 'american',
    'ru': 'russian',
    'fr': 'french',
    'es': 'spanish',
    'ger': 'german',
    'pl': 'polish'
}

select_elm = ("""<select onchange='pycmd("shLang:" +"""
              """ this.selectedOptions[0].text)' """
              """style='vertical-align: top;'>{}</select>""")


def paste_ipa(editor: Editor) -> None:
    """ Paste IPA transcription into the IPA field of the Anki editor.

    :param editor: Anki editor window
    """
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
    except (urllib.error.HTTPError, IndexError):
        showInfo("IPA not found.")
        return

    # workaround for cursive on Mac OS
    ipa.replace("ɪm", "")

    try:
        note[CONFIG["IPA_FIELD"]] = ipa
    except KeyError:
        showInfo(f"Field '{CONFIG['IPA_FIELD']}' doesn't exist.")
        return

    editor.loadNote()
    editor.web.setFocus()
    editor.web.eval("focusField(%d);" % editor.currentField)


def strip_list(list_: List[str]) -> List[str]:
    """ Removes HTML code from list elements.

    :param list_: list of IPA transcriptions
    :return: cleaned list (no HTML code)
    """
    codes = ["nbsp", "i", "b", "u"]
    return [element for element in list_ if element not in codes]


def get_deck_name(main_window: mw) -> str:
    """ Get the name of the current deck.

    :param main_window: main window of Anki
    :return: name of selected deck
    """
    try:
        deck_name = main_window.col.decks.current()['name']
    except AttributeError:
        # No deck opened?
        deck_name = None
    return deck_name


def get_default_lang(main_window: mw) -> str:
    """ Get the IPA default language.

    :param main_window: main window of Anki
    :return: default IPA language for Anki or Anki deck
    """
    lang = CONFIG['lang']
    if CONFIG['defaultlangperdeck']:
        deck_name = get_deck_name(main_window)
        if deck_name and deck_name in CONFIG['deckdefaultlang']:
            lang = CONFIG['deckdefaultlang'][deck_name]
    return lang


def on_setup_buttons(buttons: List[str], editor: Editor) -> List[str]:
    """ Add Addon button and Addon combobox to card editor.

    :param buttons: HTML codes of the editor buttons (e.g. for bold, italic, ...)
    :param editor: card editor object
    :return: updated list of buttons
    """
    # add HTML button
    button = editor.addButton(ICONPATH, "IPA", paste_ipa)
    buttons.append(button)

    # create list of language options
    previous_lang = get_default_lang(mw)
    options = [f"""<option>{previous_lang}</option>"""]  # first entry is the last selection

    options += [
        f"""<option>{language}</option>"""
        for language in sorted(LANGUAGES_MAP.keys(), key=str.lower)
        if language != previous_lang
    ]

    # add HTML combobox
    combo = select_elm.format("".join(options))
    buttons.append(combo)

    return buttons


def set_default_lang(main_window: mw, lang: str) -> None:
    """ Set new IPA default language.

    :param main_window: main window of Anki
    :param lang: new default language
    """
    CONFIG['lang'] = lang  # Always update the overall default
    if CONFIG['defaultlangperdeck']:
        deck_name = get_deck_name(main_window)
        if deck_name:
            CONFIG['deckdefaultlang'][deck_name] = lang


def on_ipa_language_select(editor: Editor, lang: str):
    """ Set new default IPA language.

    :param editor: Anki editor window
    :param lang: name of selected language
    """
    alias = LANGUAGES_MAP[lang]
    set_default_lang(mw, lang)
    editor.ipa_lang_alias = alias


def init_ipa(editor: Editor, *args, **kwargs):
    """ Get the last selected/default IPA language.

    :param editor: Anki editor window
    """
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
