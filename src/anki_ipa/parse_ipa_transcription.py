# -*- coding: utf-8 -*-

"""
This file is part of the Anki IPA add-on for Anki.
Parsing methods
Copyright: (c) 2019 m-rtin <https://github.com/m-rtin>
License: GNU AGPLv3 <https://www.gnu.org/licenses/agpl.html>
"""

import urllib
import bs4
import re
import requests
from typing import List

# Create a dictionary for all transcription methods
transcription_methods = {}
transcription = lambda f: transcription_methods.setdefault(f.__name__, f)


@transcription
def british(word: str, strip_syllable_separator: bool) -> str:
    payload = {'action': 'parse', 'page': word, 'format': 'json', 'prop': 'wikitext'}
    r = requests.get('https://en.wiktionary.org/w/api.php', params=payload)
    try:
        wikitext = r.json()['parse']['wikitext']['*']
        p = re.compile("{{a\|UK}} {{IPA\|en\|([^}]+)}}")
        m = p.search(wikitext)
        if m is None:
            p = re.compile("{{a\|RP}} {{IPA\|en\|([^}]+)}}")
            m = p.search(wikitext)
        if m is None: 
            p = re.compile("{{IPA\|en\|([^}]+)}}")
            m = p.search(wikitext)
        if m is None: 
            p = re.compile("{{IPA\|en\|([^}]+)\|([^}]+)}}")
            m = p.search(wikitext)
            
        ipa = m.group(1)
        return remove_special_chars(word=ipa, strip_syllable_separator=strip_syllable_separator)
    except (KeyError, AttributeError):
        return ""

@transcription
def american(word: str, strip_syllable_separator: bool) -> str:
    payload = {'action': 'parse', 'page': word, 'format': 'json', 'prop': 'wikitext'}
    r = requests.get('https://en.wiktionary.org/w/api.php', params=payload)
    try:
        wikitext = r.json()['parse']['wikitext']['*']
        p = re.compile("{{a\|US}} {{IPA\|en\|([^}]+)}}")
        m = p.search(wikitext)
        if m is None: 
            p = re.compile("{{a\|GA}}.*?{{IPA\|en\|([^}]+)}}")
            m = p.search(wikitext)
        if m is None: 
            p = re.compile("{{a\|GenAm}}.*?{{IPA\|en\|([^}]+)}}")
            m = p.search(wikitext)
        if m is None:
            p = re.compile("{{IPA\|en\|([^}]+)}}")
            m = p.search(wikitext)
        if m is None:
            p = re.compile("{{IPA\|en\|([^}]+)\|([^}]+)}}")
            m = p.search(wikitext)

        ipa = m.group(1)
        return remove_special_chars(word=ipa, strip_syllable_separator=strip_syllable_separator)
    except (KeyError, AttributeError):
        return ""

@transcription
def french(word: str, strip_syllable_separator: bool) -> str:
    link = f"https://fr.wiktionary.org/wiki/{word}"
    return ", ".join(parse_website(link, {'title': 'Prononciation API'}, strip_syllable_separator))


@transcription
def russian(word: str, strip_syllable_separator: bool) -> str:
    link = f"https://ru.wiktionary.org/wiki/{word}"
    return ", ".join(parse_website(link, {'class': 'IPA'}, strip_syllable_separator))


@transcription
def spanish(word: str, strip_syllable_separator: bool) -> str:
    link = f"https://es.wiktionary.org/wiki/{word}"
    return ", ".join(parse_website(link, {'class': 'ipa'}, strip_syllable_separator))


@transcription
def german(word: str, strip_syllable_separator: bool) -> str:
    payload = {'action': 'parse', 'page': word, 'format': 'json', 'prop': 'wikitext'}
    r = requests.get('https://de.wiktionary.org/w/api.php', params=payload)
    try:
        wikitext = r.json()['parse']['wikitext']['*']
        p = re.compile("{{IPA}}.*?{{Lautschrift\|([^}]+)")
        m = p.search(wikitext)
        ipa = m.group(1)
        return ipa
    except (KeyError, AttributeError):
        return ""

@transcription
def polish(word: str, strip_syllable_separator: bool) -> str:
    link = f"https://pl.wiktionary.org/wiki/{word}"
    return ", ".join(parse_website(
        link, {'title': 'To jest wymowa w zapisie IPA; zobacz hasło IPA w Wikipedii'}, strip_syllable_separator))


@transcription
def dutch(word: str, strip_syllable_separator: bool) -> str:
    link = f"https://nl.wiktionary.org/wiki/{word}"
    return ", ".join(parse_website(link, {"class": "IPAtekst"}, strip_syllable_separator))


@transcription
def italian(word: str, strip_syllable_separator: bool) -> str:
    link = f"https://it.wiktionary.org/wiki/{word}"
    return ", ".join(parse_website(link, {"class": "IPA"}, strip_syllable_separator))


@transcription
def portuguese(word: str, strip_syllable_separator: bool) -> str:
    link = f"https://pt.wiktionary.org/wiki/{word}"
    return ", ".join(parse_website(link, {"class": "ipa"}, strip_syllable_separator))


@transcription
def mandarin(word: str, strip_syllable_separator: bool) -> str:
    link = f"https://zh.wiktionary.org/wiki/{word}"
    return ", ".join(parse_website(link, {"class": "IPA"}, strip_syllable_separator))


@transcription
def catalan(word: str, strip_syllable_separator: bool) -> str:
    link = f"https://ca.wiktionary.org/wiki/{word}"
    return ", ".join(parse_website(link, {"class": "IPA"}, strip_syllable_separator))


def parse_website(link: str, css_code: dict, strip_syllable_separator: bool=True) -> List[str]:
    try:
        website = requests.get(link)
    except requests.exceptions.RequestException as e:
        return [""]
    soup = bs4.BeautifulSoup(website.text, "html.parser")
    results = soup.find_all('span', css_code) 
    if strip_syllable_separator:
        transcriptions = map(lambda result: result.getText()
            .replace("/", "")
            .replace("]", "")
            .replace("[", "")
            .replace(".", "")
            .replace("\\", ""), results)
    else:
        transcriptions = map(lambda result: result.getText()
            .replace("/", "")
            .replace("]", "")
            .replace("[", "")
            .replace("\\", ""), results)
    _transcriptions = sorted(list(set(transcriptions))[0])
    return _transcriptions


def remove_special_chars(word: str, strip_syllable_separator: bool) -> str:
    word = word.replace("/", "").replace("]", "").replace("[", "").replace("\\", "").replace(".", "")
    if strip_syllable_separator:
        word = word.replace(".", "")
    return word


def transcript(words: List[str], language: str, strip_syllable_separator: bool=True) -> str:
    transcription_method = transcription_methods[language]
    transcribed_words = [transcription_method(word, strip_syllable_separator) for word in words]
    return " ".join(transcribed_words)
