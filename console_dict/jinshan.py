#!/usr/bin/env python
# -*-coding:utf-8-*-
# Reference: http://open.iciba.com/index.php?c=wiki&t=cc

from __future__ import absolute_import

import requests


# API key of Jinshan
KEY = "FB30248420B78E380BB2FA4D11BA58E9"


def get_data(word):
    url = "http://dict-co.iciba.com/api/dictionary.php?type=json&w=%s&key=%s"%(word, KEY)
    r = requests.get(url)
    data = r.json()
    # print(data)
    return data


def sort_data(data):
    # print(data)
    doc = {}

    # useful
    doc['_id'] = data['word_name']
    doc['_grasp'] = 0
    doc['ph_am']= data['symbols'][0]['ph_am']
    doc['parts'] = data['symbols'][0]['parts']
    doc['ph_am_mp3'] = data['symbols'][0]['ph_am_mp3']

    # not so useful
    doc['exchange'] = data['exchange']
    doc['ph_en']= data['symbols'][0]['ph_en']
    doc['ph_en_mp3'] = data['symbols'][0]['ph_en_mp3']
    doc['ph_other'] = data['symbols'][0]['ph_other']
    doc['ph_tts_mp3'] = data['symbols'][0]['ph_tts_mp3']
    try:
        doc['items'] = data['items']  # useless
    except KeyError:
        pass
    doc['is_CRI'] = data['is_CRI']  # useless
    return doc


def jinshan(word):
    data = get_data(word)
    doc = sort_data(data)
    return doc


def main():
    doc = jinshan('hello')
    print(doc)


if __name__=="__main__":
    main()

