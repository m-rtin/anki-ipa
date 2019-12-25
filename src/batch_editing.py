# -*- coding: utf-8 -*-

"""
This file is part of the Anki IPA add-on for Anki.
Add IPA transcription in Anki browser.
Copyright: (c) 2019 m-rtin <https://github.com/m-rtin>
License: GNU AGPLv3 <https://www.gnu.org/licenses/agpl.html>
"""

from aqt.browser import Browser
from aqt.utils import tooltip
import aqt.qt as qt

from .typing import List
from . import consts
from . import parse_ipa
from . import main


class AddIpaTranscriptDialog(qt.QDialog):
    """QDialog to add IPA transcription to multiple notes in Anki browser."""

    def __init__(self, browser: Browser, selected_notes: List[int]) -> None:
        """Initialize AddIpaTranscriptDialog."""
        qt.QDialog.__init__(self, parent=browser)
        self.browser = browser
        self.selected_notes = selected_notes
        self._setup_comboboxes()
        self._setup_form()
        self._setup_buttons()
        self._setup_main()

    def _setup_comboboxes(self) -> None:
        """Setup comboboxes for language, base field and target field."""
        fields = self._get_fields()

        self.lang_combobox = qt.QComboBox()
        self.lang_combobox.addItems(consts.LANGUAGES_MAP.values())

        self.base_combobox = qt.QComboBox()
        self.base_combobox.addItems(fields)

        self.field_combobox = qt.QComboBox()
        self.field_combobox.addItems(fields)

    def _setup_form(self) -> None:
        """Setup form for user interaction."""
        self.form_group_box = qt.QGroupBox("Options")

        form_layout = qt.QFormLayout()
        form_layout.addRow(qt.QLabel("Language:"), self.lang_combobox)
        form_layout.addRow(qt.QLabel("Field of word:"), self.base_combobox)
        form_layout.addRow(qt.QLabel("Field of IPA transcription:"), self.field_combobox)

        self.form_group_box.setLayout(form_layout)

    def _setup_buttons(self) -> None:
        """Setup add button."""
        button_box = qt.QDialogButtonBox(qt.Qt.Horizontal, self)
        add_button = button_box.addButton("Add", qt.QDialogButtonBox.ActionRole)

        self.bottom_hbox = qt.QHBoxLayout()
        self.bottom_hbox.addWidget(button_box)

        add_button.clicked.connect(self.on_confirm)

    def _setup_main(self) -> None:
        """Setup diag window."""
        main_layout = qt.QVBoxLayout()
        main_layout.addWidget(self.form_group_box)
        main_layout.addLayout(self.bottom_hbox)
        self.setLayout(main_layout)
        self.setWindowTitle("Add IPA transcriptions")

    def _get_fields(self) -> None:
        """Get all fields of selected notes."""
        selected_note = self.selected_notes[0]
        mw = self.browser.mw
        model = mw.col.getNote(selected_note).model()
        fields = mw.col.models.fieldNames(model)
        return fields

    def on_confirm(self) -> None:
        """Call batch_edit_notes if button is clicked."""
        batch_edit_notes(
            self.browser,
            self.selected_notes,
            self.lang_combobox.currentText(),
            self.base_combobox.currentText(),
            self.field_combobox.currentText()
        )
        self.close()


def batch_edit_notes(browser: Browser, selected_notes: List[int], lang: str, base_field: str,
                     target_field: str) -> None:
    """ Add IPA transcription to all selected notes.

    :param browser:  Anki browser
    :param selected_notes: selected notes in browser to which we want to add IPA transcription
    :param lang: language for the IPA transcription
    :param base_field: name of the base field for IPA transcription
    :param target_field: name of the target field for IPA transcription
    """
    mw = browser.mw
    mw.checkpoint("batch edit")
    mw.progress.start()
    browser.model.beginReset()

    for selected_note in selected_notes:
        note = mw.col.getNote(selected_note)
        if base_field in note and target_field in note:
            words = main.get_words_from_field(field_text=note[base_field])
            try:
                note[target_field] = parse_ipa.transcript(words=words, language=lang)
            # IPA transcription not found
            except IndexError:
                continue
            note.flush()

    browser.model.endReset()
    mw.requireReset()
    mw.progress.finish()
    mw.reset()


def on_batch_edit(browser: Browser) -> None:
    """ Open BatchEditDialog when menu entry is clicked.

    :param browser: Anki browser
    """
    selected_notes = browser.selectedNotes()
    if not selected_notes:
        tooltip("No cards selected.")
        return
    dialog = AddIpaTranscriptDialog(browser, selected_notes)
    dialog.exec_()


def setup_menu(browser: Browser) -> None:
    """ Add menu entry to Anki Browser.

    :param browser: Anki browser
    """
    menu = browser.form.menuEdit
    menu.addSeparator()
    a = menu.addAction('Add IPA ...')

    # call onBatchEdit if entry is clicked
    a.triggered.connect(lambda _, b=browser: on_batch_edit(b))
