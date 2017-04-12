#!/usr/bin/env python
# -*-coding:utf-8-*-

from __future__ import print_function, absolute_import

import subprocess
from optparse import OptionParser

from pymongo import MongoClient

from console_dict.config import PACKAGE_VERSION, DEFAULT_DATABASE, DEFAULT_COLLECTION, DEFAUTL_PATH, LOG
from console_dict.jinshan import jinshan
from console_dict.tools import print_data


PACKAGE_VERSION = '%prog '+PACKAGE_VERSION


def search_word(word, collection=None):
    if collection:
        doc = collection.find_one({'_id':word})
        if not doc:
            try:
                doc = jinshan(word)
            except KeyError:
                print('We cannot find the word.')
                return None
            collection.insert(doc)
    else:
        try:
            doc = jinshan(word)
        except KeyError:
            print('We cannot find the word.')
            return None

    try:
        print_data(doc, collection)
        return doc
    except KeyError:
        print('We cannot find the word.')
        if collection:
            collection.delete_one(doc['_id'])
        return None


def search_words(collection=None):
    print("Let's begin to search words!")
    word = raw_input("Input: ")
    while word:
        search_word(word, collection)
        word = raw_input('Input: ')


def main():
    usage = "usage: %prog [options] arg1 arg2"
    parser = OptionParser(usage=usage, version=PACKAGE_VERSION)
    parser.add_option('-w', '--word', default=None, help='The word going to be searched')
    parser.add_option('-s', '--store', default=True)
    parser.add_option('-d', '--database', default=DEFAULT_DATABASE)
    parser.add_option('-c', '--collection',default=DEFAULT_COLLECTION)
    (options, args) = parser.parse_args()

    # clean the mongodb process
    log = open(LOG, 'w')
    p = subprocess.Popen("kill -2 `pgrep mongo`", shell=True, stdout=log)
    p.kill()

    if options.word:
        if options.store:
            p = subprocess.Popen(['mongod', '--dbpath', DEFAUTL_PATH], stdout=log)
            client = MongoClient()
            db = client[options.database]
            collection = db[options.collection]
            search_word(options.word, collection)
            p.kill()
        else:
            search_word(options.word)


    else:
        if options.store:
            p = subprocess.Popen(['mongod', '--dbpath', DEFAUTL_PATH], stdout=log)
            client = MongoClient()
            db = client[options.database]
            collection = db[options.collection]
            search_words(collection)
            p.kill()
        else:
            search_words()

    log.close()


if __name__=="__main__":
    search_words()
