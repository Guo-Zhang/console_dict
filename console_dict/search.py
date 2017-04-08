#!/usr/bin/env python
# -*-coding:utf-8-*-

from __future__ import print_function, absolute_import

import subprocess

from pymongo import MongoClient
from xtls.colorful import Color,colorful_print

from console_dict.jinshan import jinshan


def _print_means(parts):
    for part in parts:
        colorful_print(" %s %s"%(part['part'],';'.join(part['means'])),Color.BLUE)


def _print_data(doc):
    colorful_print("%s |%s|"%(doc['_id'],doc['ph_am']),Color.RED)
    _print_means(doc['parts'])


def search_word(word, collection=None):
    if collection:
        doc = collection.find_one({'_id':word})
        if not doc:
            doc = jinshan(word)
            collection.insert(doc)
    else:
        doc = jinshan(word)

    _print_data(doc)
    return doc


def search_words(collection=None):
    print("Let's begin to search words!")
    word = raw_input("Input: ")
    while word:
        search_word(word, collection)
        word = raw_input('Input: ')


def main():
    # database
    p = subprocess.Popen(['mongod', '--dbpath', '/Users/zhangguo/MyWords'])
    client = MongoClient()
    db = client.test
    collection = db.test

    word = 'test'
    search_word(word, collection)

    print(collection.count())
    p.kill()



if __name__=="__main__":
    # main()
    search_words()
