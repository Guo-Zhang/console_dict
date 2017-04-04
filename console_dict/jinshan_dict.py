# -*-coding:utf-8-*-
# Reference: http://open.iciba.com/index.php?c=wiki&t=cc

from __future__ import print_function

import requests
from xtls.colorful import Color,colorful_print


KEY = "FB30248420B78E380BB2FA4D11BA58E9"


def get_data(word):
    url = "http://dict-co.iciba.com/api/dictionary.php?type=json&w=%s&key=%s"%(word, KEY)
    r = requests.get(url)
    data = r.json()
    return data


def print_means(parts):
    for part in parts:
        colorful_print(" %s %s"%(part['part'],';'.join(part['means'])),Color.BLUE)

def print_data(data):
    colorful_print("%s |%s|"%(data['word_name'],data['symbols'][0]['ph_am']),Color.RED)
    print_means(data['symbols'][0]['parts'])


def jinshan_dict(word):
    data = get_data(word)
    print_data(data)


def main():
    jinshan_dict('hello')


if __name__=="__main__":
    main()

