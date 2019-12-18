# -*- coding: utf-8 -*-

import urllib

import bs4
import requests
import ssl

transcription_methods = {}
transcription = lambda f: transcription_methods.setdefault(f.__name__, f)


def get_english_ipa_list(word):
    url = 'https://www.oxfordlearnersdictionaries.com/definition/english/'

    context = ssl._create_unverified_context()
    page = urllib.request.urlopen(url + word, context=context)
    soup = bs4.BeautifulSoup(page, "html.parser")

    results = [
        x.getText() for x in soup.select('span[class="phon"]')
    ]

    return results


@transcription
def british(word):
    ipa = get_english_ipa_list(word)
    result = ipa[0][3:].replace("//", "")
    return result


@transcription
def american(word):
    ipa = get_english_ipa_list(word)
    result = ipa[1][4:].replace("//", "")
    return result


@transcription
def russian(word):
    link = 'https://ru.wiktionary.org/wiki/{}'.format(word)
    website = requests.get(link)
    soup = bs4.BeautifulSoup(website.text, "html.parser")
    results = soup.find_all('span', {'class': 'IPA'})
    return results[0].getText()


def transcript(words, language):
    transcription_method = transcription_methods[language]
    transcribed_words = [transcription_method(word) for word in words]
    return " ".join(transcribed_words)
