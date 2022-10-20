<p align="center"><img src="https://raw.githubusercontent.com/martyngal/anki-ipa/master/screenshots/new_screenshot_1.jpg"></p>

<h2 align="center">Anki IPA</h2>
<p align="center">
<a title="License: GNU AGPLv3" href="https://github.com/m-rtin/anki-ipa/blob/master/LICENSE"><img  src="https://img.shields.io/badge/license-GNU AGPLv3-green.svg"></a>
<a title="Rate on AnkiWeb" href="https://ankiweb.net/shared/info/799647424"><img src="https://glutanimate.com/logos/ankiweb-rate.svg"></a><br>
</p>


Allows you to insert IPA transcriptions into the spaced-repetition flashcard app [Anki](https://apps.ankiweb.net/).

### Installation

The easiest way to install Anki IPA is through [AnkiWeb](https://ankiweb.net/shared/info/799647424).


### Testing

To test the addon in Anki, navigate to Tools/Add-ons and press on the "View Files" button. The addons21 directory should open up in your file explorer. Copy your local `anki-ipa/src/anki_ipa/` folder into this directory and restart Anki. You are now able to test the addon.  

To run the unittests of this project, go to the anki-ipa/src/anki_ipa directory and run: 

`python3 -m test_parse_ipa_transcription`

### Contributing 

Languages can be added or improved in the [parse_ipa_transcription.py](https://github.com/m-rtin/anki-ipa/blob/master/src/anki_ipa/parse_ipa_transcription.py) file. The changes should be tested in the [test_parse_ipa_transcription.py](https://github.com/m-rtin/anki-ipa/blob/master/src/anki_ipa/test_parse_ipa_transcription.py) file.

### License and Credits

*Anki IPA* is based on [*Syntax Highlighting for Code*](https://ankiweb.net/shared/info/1463041493) and [*Batch Editing*](https://ankiweb.net/shared/info/291119185) by [Glutanimate](https://github.com/glutanimate). 

Anki IPA is free and open-source software. The add-on code that runs within Anki is released under the GNU AGPLv3 license, extended by a number of additional terms. For more information please see the [LICENSE](https://github.com/m-rtin/anki-ipa/blob/master/LICENSE) file that accompanied this program.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY.
