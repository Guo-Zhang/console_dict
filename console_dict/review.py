#!/usr/bin/env python
# -*-coding:utf-8-*-

from __future__ import print_function, absolute_import

import random
import subprocess
from optparse import OptionParser

from pymongo import MongoClient

from console_dict.config import PACKAGE_VERSION, DEFAULT_DATABASE, DEFAULT_COLLECTION, DEFAUTL_PATH, LOG
from console_dict.tools import print_word, print_means, play_pron


PACKAGE_VERSION = '%prog '+PACKAGE_VERSION


def cal_status(prompt = ''):
    status = raw_input(prompt)

    yes = ['Yes', 'yes', 'Y', 'y', '1']
    no = ['No', 'no', 'N', 'n', '0']

    if status in yes:
        return True
    elif status in no:
        return False
    elif status == 'stop':
        return 'stop'
    elif status == 'del':
        return 'del'
    else:
        print("please choose again.")
        return cal_status(prompt)


def review_words(collection):
    words = list(collection.find({'_grasp': {"$lt": 10}}))

    if not words:
        print("No Words. Please change another word list.")
        return None

    usage = """
Please input 'y' if you know and 'n' if you don't know.
Input 'stop' if you want to stop.
    """
    print(usage)

    while words:
        word = words.pop(random.randrange(len(words)))
        print_word(word)
        play_pron(word, collection=collection)

        train_status = cal_status("Do you know it?")
        if train_status == 'del':
            collection.delete_one(word['_id'])
        if train_status == 'stop':
            break

        try:
            print_means(word)
        except KeyError:
            print('This is not a correct word.')
            collection.delete_one(word['_id'])

        if train_status:
            test_status = cal_status("Do you really know it? ")
            if test_status == 'del':
                collection.delete_one(word['_id'])
            if test_status == 'stop':
                break

        if train_status and test_status:
            status = 1
        elif train_status and (not test_status):
            status = -1
            words.append(word)
        else:
            status = 0
            words.append(word)

        collection.update_one({'_id': word['_id']}, {"$inc":{'_grasp': status}})

        next = raw_input("next?")
        if next=='stop':
            break
        else:
            print()



    print("Happy that you are willing to review us. See you next time!")


def stats(collection):
    data_total = list(collection.find())
    data_new = list(collection.find({'_grasp': {"$lt": 10}}))

    total = len(data_total)
    new = len(data_new)
    new_percentage = float(new)/float(total)*100.
    score = sum([doc['_grasp'] for doc in data_total])
    score_percentage = score*0.1/total*100.

    info ="""
There are %d words in total in the words list, including %d old words(%0.2f %%) and %d new words(%0.2f %%).

At present you have got %d score(%0.2f %%).

Cheer up! Try you best to deal with the problems of new words!
    """%(total, total-new, 100-new_percentage, new, new_percentage, score, score_percentage)

    print(info)


def main():
    usage = "usage: %prog [options] arg1 arg2"
    parser = OptionParser(usage=usage, version=PACKAGE_VERSION)
    parser.add_option('-d', '--database', default=DEFAULT_DATABASE)
    parser.add_option('-c', '--collection', default=DEFAULT_COLLECTION)
    parser.add_option('-s', action="store_false", dest='stats', default=True)
    (options, args) = parser.parse_args()

    # clean the mongodb process
    log = open(LOG, 'w')
    p = subprocess.Popen("kill -2 `pgrep mongo`", shell=True, stdout=log)
    p.kill()

    # open the database
    p = subprocess.Popen(['mongod', '--dbpath', DEFAUTL_PATH], stdout=log)
    client = MongoClient()
    db = client[options.database]
    collection = db[options.collection]

    # review words
    if options.stats:
        print("Let's begin to review the words from %s of %s" % (options.collection, options.database))
        review_words(collection)
    else:
        stats(collection)

    # clean the mongodb process
    p.kill()
    log.close()


if __name__ == "__main__":
    # clean the mongodb process
    log = open('console_dict.log', 'w')
    p = subprocess.Popen("kill -2 `pgrep mongo`", shell=True, stdout=log)
    p.kill()

    # open the database
    p = subprocess.Popen(['mongod', '--dbpath', DEFAUTL_PATH], stdout=log)
    client = MongoClient()
    db = client[DEFAULT_DATABASE]
    collection = db[DEFAULT_COLLECTION]

    # review words
    review_words(collection)

    # stats
    stats(collection)

    # clean the mongodb process
    p.kill()
    log.close()
