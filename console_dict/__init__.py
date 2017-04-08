# -*-coding:utf-8-*-
# Reference: http://www.tuicool.com/articles/veaaYby

from __future__ import print_function, absolute_import

import subprocess
from optparse import OptionParser

from pymongo import MongoClient

from console_dict.search import search_word, search_words
from console_dict.review import review_words, stats
from console_dict.config import PACKAGE_VERSION, DEFAULT_COLLECTION, DEFAUTL_PATH, DEFAULT_DATABASE, LOG


PACKAGE_VERSION = '%prog '+PACKAGE_VERSION


def main():
    usage = "usage: %prog [options] arg1 arg2"
    parser = OptionParser(usage=usage, version=PACKAGE_VERSION)
    parser.add_option('-m', '--mode', default='search', help="'search'or 'review'")
    parser.add_option('-d', '--database', default=DEFAULT_DATABASE)
    parser.add_option('-c', '--collection',default=DEFAULT_COLLECTION)
    parser.add_option('-w', '--word', default=None, help="Only work for 'search'")
    parser.add_option('-k', '--keep', default=True, help="Only work for 'search'")
    parser.add_option('-s', action='store_false', dest='stats', default=True)
    (options, args) = parser.parse_args()

    # clean the mongodb process
    log = open(LOG, 'w')
    p = subprocess.Popen("kill -2 `pgrep mongo`", shell=True, stdout=log)
    p.kill()

    if options.mode == 'search':
        if options.word:
            if options.keep:
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

    elif options.mode == 'review':
        p = subprocess.Popen(['mongod', '--dbpath', DEFAUTL_PATH], stdout=log)
        client = MongoClient()
        db = client[options.database]
        collection = db[options.collection]
        if options.stats:
            print("Let's begin to review the words from %s of %s" % (options.collection, options.database))
            review_words(collection)
        else:
            stats(collection)

        p.kill()

    log.close()