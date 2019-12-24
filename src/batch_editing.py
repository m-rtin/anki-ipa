from aqt.browser import Browser
from aqt.utils import tooltip
import aqt.qt as qt

from .typing import List, Callable
from . import consts


class BatchEditDialog(qt.QDialog):
    """Browser batch editing dialog"""

    def __init__(self, browser: Browser, selected_notes: List[int]) -> None:
        qt.QDialog.__init__(self, parent=browser)
        self.browser = browser
        self.nids = selected_notes
        self._setupUi()

    def _setupUi(self):
        # Language combobox
        lang_label = qt.QLabel("Language:")
        self.lang_combobox = qt.QComboBox()
        self.lang_combobox.addItems(consts.LANGUAGES_MAP.keys())
        lang_hbox = qt.QHBoxLayout()
        lang_hbox.addWidget(lang_label)
        lang_hbox.addWidget(self.lang_combobox)
        lang_hbox.setAlignment(qt.Qt.AlignLeft)

        # Available fields
        fields = self._getFields()

        # Base field
        base_label = qt.QLabel("Put IPA transcription of this field:")
        self.base_combobox = qt.QComboBox()
        self.base_combobox.addItems(fields)
        base_hbox = qt.QHBoxLayout()
        base_hbox.addWidget(base_label)
        base_hbox.addWidget(self.base_combobox)
        base_hbox.setAlignment(qt.Qt.AlignLeft)

        # Target field combobox
        field_label = qt.QLabel("Into this field:")
        self.field_combobox = qt.QComboBox()
        self.field_combobox.addItems(fields)
        field_hbox = qt.QHBoxLayout()
        field_hbox.addWidget(field_label)
        field_hbox.addWidget(self.field_combobox)
        field_hbox.setAlignment(qt.Qt.AlignLeft)

        # Buttons
        button_box = qt.QDialogButtonBox(qt.Qt.Horizontal, self)
        adda_btn = button_box.addButton("Add &after", qt.QDialogButtonBox.ActionRole)
        adda_btn.setToolTip("Add after existing field contents")
        bottom_hbox = qt.QHBoxLayout()
        bottom_hbox.addWidget(button_box)

        # Connect button
        adda_btn.clicked.connect(self.on_confirm)

        # Main window
        vbox_main = qt.QVBoxLayout()
        vbox_main.addLayout(lang_hbox)
        vbox_main.addLayout(base_hbox)
        vbox_main.addLayout(field_hbox)
        vbox_main.addLayout(bottom_hbox)
        self.setLayout(vbox_main)
        self.setMinimumWidth(540)
        self.setMinimumHeight(400)
        self.setWindowTitle("Add IPA")

    def _getFields(self):
        nid = self.nids[0]
        mw = self.browser.mw
        model = mw.col.getNote(nid).model()
        fields = mw.col.models.fieldNames(model)
        return fields

    def on_confirm(self):
        # batchEditNotes(self.browser, self.nids)
        self.close()


def batch_edit_notes(browser: Browser, selected_notes: List[int]) -> None:
    # TODO
    mw = browser.mw
    mw.checkpoint("batch edit")
    mw.progress.start()
    browser.model.beginReset()

    for note in selected_notes:
        note = mw.col.getNote(note)
        if fld in note:
            content = note[fld]
            if content.endswith(breaks):
                spacer = ""
            note[fld] += spacer + html
            note.flush()

    browser.model.endReset()
    mw.requireReset()
    mw.progress.finish()
    mw.reset()


def on_batch_edit(browser: Browser) -> None:
    selected_notes = browser.selectedNotes()
    if not selected_notes:
        tooltip("No cards selected.")
        return
    dialog = BatchEditDialog(browser, selected_notes)
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
