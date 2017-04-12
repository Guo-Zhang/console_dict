#!/usr/bin/env python
# -*-coding:utf-8-*-
# Reference: http://open.iciba.com/index.php?c=wiki&t=cc

from __future__ import absolute_import

import os

import requests

from console_dict.config import JINSHAN_KEY, MP3_PATH


if not os.path.isdir(MP3_PATH):
    os.mkdir(MP3_PATH)


def get_data(word):
    url = "http://dict-co.iciba.com/api/dictionary.php?type=json&w=%s&key=%s"%(word, JINSHAN_KEY)
    r = requests.get(url)
    data = r.json()
    # print(data)
    return data


def get_mp3(url, word, type='am'):
    if not url:
        return None

    r = requests.get(url, stream=True)
    fname = '_'.join([word,type])+'.mp3'
    fname = os.path.join(MP3_PATH, fname)
    with open(fname, 'wb') as fd:
        for chunk in r.iter_content(chunk_size=128):
            fd.write(chunk)
    return fname


def sort_data(data):
    # print(data)
    doc = {}

    # useful
    doc['_id'] = data['word_name']
    doc['_grasp'] = 0
    doc['ph_am']= data['symbols'][0]['ph_am']
    doc['parts'] = data['symbols'][0]['parts']
    doc['ph_am_mp3'] = data['symbols'][0]['ph_am_mp3']
    doc['ph_am_mp3_file'] = get_mp3(doc['ph_am_mp3'], doc['_id'], type='am')

    # not so useful
    doc['exchange'] = data['exchange']
    doc['ph_en']= data['symbols'][0]['ph_en']
    doc['ph_en_mp3'] = data['symbols'][0]['ph_en_mp3']
    doc['ph_en_mp3_file'] = get_mp3(doc['ph_en_mp3'], doc['_id'], type='en')
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



