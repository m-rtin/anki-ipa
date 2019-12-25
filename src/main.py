# -*- coding: utf-8 -*-

"""
This file is part of the Anki IPA add-on for Anki.
Main Module, hooks add-on methods into Anki.
Copyright: (c) m-rtin <https://github.com/m-rtin>
License: GNU AGPLv3 <https://www.gnu.org/licenses/agpl.html>
"""

import os
import re
import urllib

from .typing import List, Callable

from anki.hooks import addHook, wrap
from aqt.utils import showInfo
from aqt.editor import Editor
from aqt import mw

from . import parse_ipa
from . import batch_editing
from . import consts

ADDON_PATH = os.path.dirname(__file__)
ICON_PATH = os.path.join(ADDON_PATH, "icons", "button.png")
CONFIG = mw.addonManager.getConfig(__name__)

select_elm = ("""<select onchange='pycmd("IPALang:" +"""
              """ this.selectedOptions[0].text)' """
              """style='vertical-align: top;'>{}</select>""")


def paste_ipa(editor: Editor) -> None:
    """ Paste IPA transcription into the IPA field of the Anki editor.

    :param editor: Anki editor window
    """
    lang_alias = editor.ipa_lang_alias
    note = editor.note

    try:
        field_text = note[CONFIG["WORD_FIELD"]]
    except KeyError:
        showInfo(f"Field '{CONFIG['WORD_FIELD']}' doesn't exist.")
        return

    words = get_words_from_field(field_text)

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


def get_words_from_field(field_text: str) -> List[str]:
    words = strip_list(re.findall(r"[\w']+", field_text))
    return words


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
    button = editor.addButton(ICON_PATH, "IPA", paste_ipa)
    buttons.append(button)

    # create list of language options
    previous_lang = get_default_lang(mw)
    options = [f"""<option>{previous_lang}</option>"""]  # first entry is the last selection

    options += [
        f"""<option>{language}</option>"""
        for language in sorted(consts.LANGUAGES_MAP.keys(), key=str.lower)
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


def on_ipa_language_select(editor: Editor, lang: str) -> None:
    """ Set new default IPA language.

    :param editor: Anki editor window
    :param lang: name of selected language
    """
    alias = consts.LANGUAGES_MAP[lang]
    set_default_lang(mw, lang)
    editor.ipa_lang_alias = alias


def init_ipa(editor: Editor, *args, **kwargs) -> None:
    """ Get the last selected/default IPA language.

    :param editor: Anki editor window
    """
    previous_lang = get_default_lang(mw)
    editor.ipa_lang_alias = consts.LANGUAGES_MAP.get(previous_lang, "")


def on_bridge_cmd(editor: Editor, command: str, _old: Callable) -> None:
    """ React when new combobox selection is made.

    :param editor: Anki editor window
    :param command: editor command (e.g. own IPALang or focus, blur, key, ...)
    :param _old: old editor.onBridgeCmd method
    """
    # old commands are executed like before
    if not command.startswith("IPALang"):
        _old(editor, command)
    # new language gets selected in the combobox
    else:
        _, lang = command.split(":")
        on_ipa_language_select(editor, lang)


# Overwrite Editor methods
addHook("setupEditorButtons", on_setup_buttons)
Editor.onBridgeCmd = wrap(Editor.onBridgeCmd, on_bridge_cmd, "around")
Editor.__init__ = wrap(Editor.__init__, init_ipa)

# Batch editing
addHook("browser.setupMenus", batch_editing.setup_menu)