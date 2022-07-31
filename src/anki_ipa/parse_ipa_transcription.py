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
from typing import List

# Create a dictionary for all transcription methods
transcription_methods = {}
transcription = lambda f: transcription_methods.setdefault(f.__name__, f)


@transcription
def british(word: str):
    link = f"https://www.lexico.com/definition/{word}"
    return ", ".join(parse_website(link, {"class": "phoneticspelling"}))


@transcription
def american(word: str) -> str:
    link = f"https://www.lexico.com/en/definition/{word}"
    return ", ".join(parse_website(link, {"class": "phoneticspelling"}))


@transcription
def russian(word):
    link = f"https://ru.wiktionary.org/wiki/{word}"
    return ", ".join(parse_website(link, {'class': 'IPA'}))


@transcription
def french(word):
    link = f"https://fr.wiktionary.org/wiki/{word}"
    return ", ".join(parse_website(link, {'title': 'Prononciation API'}))


@transcription
def spanish(word):
    link = f"https://es.wiktionary.org/wiki/{word}"
    return ", ".join(parse_website(link, {'style': 'color:#368BC1'}))


@transcription
def german(word):
    link = f"https://de.wiktionary.org/wiki/{word.capitalize()}"
    transcriptions = parse_website(link, {'class': 'ipa'})
    if len(transcriptions) == 1:
        return transcriptions[0]
    else:
        # ignore rhym words
        return transcriptions[1]


@transcription
def polish(word):
    link = f"https://pl.wiktionary.org/wiki/{word}"
    return ", ".join(parse_website(
        link, {'title': 'To jest wymowa w zapisie IPA; zobacz hasło IPA w Wikipedii'}))


@transcription
def dutch(word):
    link = f"https://nl.wiktionary.org/wiki/{word}"
    return ", ".join(parse_website(link, {"class": "IPAtekst"}))


def parse_website(link: str, css_code: dict) -> List[str]:
    try:
        website = requests.get(link)
    except requests.exceptions.RequestException as e:
        return [""]
    soup = bs4.BeautifulSoup(website.text, "html.parser")
    results = soup.find_all('span', css_code) 
    transcriptions = map(lambda result: result.getText()
        .replace("/", "")
        .replace("]", "")
        .replace("[", "")
        .replace(".", "")
        .replace("\\", ""), results)
    return sorted(list(set(transcriptions)))


def transcript(words: List[str], language: str) -> str:
    transcription_method = transcription_methods[language]
    transcribed_words = [transcription_method(word) for word in words]
    return " ".join(transcribed_words)
