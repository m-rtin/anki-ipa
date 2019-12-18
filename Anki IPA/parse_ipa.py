# -*- coding: utf-8 -*-

import urllib
import bs4
import requests
import ssl


def get_english_ipa_list(word):
    url = 'https://www.oxfordlearnersdictionaries.com/definition/english/'

    context = ssl._create_unverified_context()
    page = urllib.request.urlopen(url + word, context=context)
    soup = bs4.BeautifulSoup(page, "html.parser")

    results = [
        x.getText() for x in soup.select('span[class="phon"]')
    ]

    return results


def get_british_ipa(word):
    ipa = get_english_ipa_list(word)
    result = ipa[0][3:].replace("//", "")
    return result


def get_american_ipa(word):
    ipa = get_english_ipa_list(word)
    result = ipa[1][4:].replace("//", "")
    return result


def get_russian_ipa(word):
    link = 'https://ru.wiktionary.org/wiki/{}'.format(word)
    website = requests.get(link)
    soup = bs4.BeautifulSoup(website.text, "html.parser")
    results = soup.find_all('span', {'class': 'IPA'})
    return results[0].getText()
