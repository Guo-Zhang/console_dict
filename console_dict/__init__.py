# -*-coding:utf-8-*-
# Reference: http://www.tuicool.com/articles/veaaYby

from __future__ import absolute_import

import subprocess
from optparse import OptionParser

from pymongo import MongoClient

from console_dict.search import search_word, search_words


PACKAGE_VERSION =  "%prog 0.0.1.dev2"


def main():
    usage = "usage: %prog [options] arg1 arg2"
    parser = OptionParser(usage=usage, version=PACKAGE_VERSION)
    parser.add_option('-w', '--word', default=None, help='The word going to be searched')
    parser.add_option('-s', '--store', default=True)
    # parser.add_option('-m', '--mode', default='search', help="Choose 'search' or 'review'")
    parser.add_option('-d', '--database', default='GRE')
    parser.add_option('-c', '--collection',default='filling')
    (options, args) = parser.parse_args()

    # clean the mongodb process
    log = open('console_dict.log', 'w')
    p = subprocess.Popen("kill -2 `pgrep mongo`", shell=True, stdout=log)
    p.kill()

    if options.word:
        if options.store:
            p = subprocess.Popen(['mongod', '--dbpath', '/Users/zhangguo/MyWords'], stdout=log)
            client = MongoClient()
            db = client[options.database]
            collection = db[options.collection]
            search_word(options.word, collection)
            p.kill()
        else:
            search_word(options.word)

    else:
        if options.store:
            p = subprocess.Popen(['mongod', '--dbpath', '/Users/zhangguo/MyWords'], stdout=log)
            client = MongoClient()
            db = client[options.database]
            collection = db[options.collection]
            search_words(collection)
            p.kill()
        else:
            search_words()

    log.close()


if __name__=="__main__":
    main()