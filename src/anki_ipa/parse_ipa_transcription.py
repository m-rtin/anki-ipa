# -*- coding: utf-8 -*-

"""
This file is part of the Anki IPA add-on for Anki.
Parsing methods
Copyright: (c) 2019 m-rtin <https://github.com/m-rtin>
License: GNU AGPLv3 <https://www.gnu.org/licenses/agpl.html>
"""

import urllib
import bs4
import requests
import ssl
from typing import List

# Create a dictionary for all transcription methods
transcription_methods = {}
transcription = lambda f: transcription_methods.setdefault(f.__name__, f)


@transcription
def british(word):
    link = f"https://www.lexico.com/definition/{word}"
    website = requests.get(link)
    soup  = bs4.BeautifulSoup(website.text, "html.parser")
    results = soup.find_all("span", {"class": "phoneticspelling"})
    ipa_transcriptions = sorted(list(set(map(lambda result: result.getText(), results))))
    result = ", ".join(ipa_transcriptions).replace("/", "")
    return result


@transcription
def american(word) -> str:
    link = f"https://www.lexico.com/en/definition/{word}"
    website = requests.get(link)
    soup  = bs4.BeautifulSoup(website.text, "html.parser")
    results = soup.find_all("span", {"class": "phoneticspelling"})
    ipa_transcriptions = sorted(list(set(map(lambda result: result.getText(), results))))
    result = ", ".join(ipa_transcriptions).replace("/", "")
    return result


@transcription
def russian(word):
    link = f"https://ru.wiktionary.org/wiki/{word}"
    results = parse_wiktionary(link, {'class': 'IPA'})
    return results[0].getText()


@transcription
def french(word):
    link = f"https://fr.wiktionary.org/wiki/{word}"
    results = parse_wiktionary(link, {'title': 'Prononciation API'})
    return results[0].getText().replace("\\", "")


@transcription
def spanish(word):
    link = f"https://es.wiktionary.org/wiki/{word}"
    results = parse_wiktionary(link, {'style': 'color:#368BC1'})
    return results[0].getText()


@transcription
def german(word):
    try:
        link = f"https://de.wiktionary.org/wiki/{word}"
        results = parse_wiktionary(link, {'class': 'ipa'})
    except (urllib.error.HTTPError, IndexError):
        word = word.capitalize()
        link = f"https://de.wiktionary.org/wiki/{word}"
        results = parse_wiktionary(link, {'class': 'ipa'})
    return results[0].getText()


@transcription
def polish(word):
    link = f"https://pl.wiktionary.org/wiki/{word}"
    results = parse_wiktionary(
        link, {'title': 'To jest wymowa w zapisie IPA; zobacz hasło IPA w Wikipedii'})
    return results[0].getText().replace("[", "").replace("]", "")


@transcription
def dutch(word):
    link = f"https://nl.wiktionary.org/wiki/{word}"
    results = parse_wiktionary(link, {
        'style': 'font-family:Gentium, Gentium Alternative, Arial Unicode MS, Lucida Sans Unicode, Lucida Grande, TITUS Cyberbit Basic, Doulos SIL, Code2000, MS Mincho, Arial;text-decoration:none; font-size: 110%;'})
    return results[0].getText().replace("/", "").replace("/", "")


def parse_wiktionary(link, css_code):
    website = requests.get(link)
    soup = bs4.BeautifulSoup(website.text, "html.parser")
    results = soup.find_all('span', css_code)
    return results


def transcript(words: List[str], language: str) -> str:
    transcription_method = transcription_methods[language]
    transcribed_words = [transcription_method(word) for word in words]
    return " ".join(transcribed_words)
