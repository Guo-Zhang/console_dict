#!/usr/bin/env python
# -*-coding:utf-8-*-

from __future__ import print_function, absolute_import

import sys
import subprocess

from xtls.colorful import Color,colorful_print

from console_dict.jinshan import get_mp3


def print_word(doc):
    if doc['ph_am']:
        colorful_print("%s |%s|" % (doc['_id'], doc['ph_am']), Color.RED)
    else:
        colorful_print("%s" % (doc['_id']), Color.RED)


def print_means(doc):
    parts = doc['parts']
    for part in parts:
        colorful_print(" %s %s"%(part['part'],';'.join(part['means'])),Color.BLUE)


def _play_mp3(fname):
    if sys.platform=='darwin':
        subprocess.call(['afplay',fname])
    else:
        print("This platform is not supported.")
        raise


def _update_data(id, key, fname, collection=None):
    if collection is None:
        return None
    collection.update_one({'_id': id}, {"$set": {key: fname}})


def play_pron(doc, type='am', collection=None):
    key_source = '_'.join(['ph',type,'mp3'])
    key = '_'.join(['ph',type,'mp3','file'])
    try:
        fname = doc[key]
    except KeyError:
        fname = get_mp3(doc[key_source], doc['_id'], type='am')
        doc[key] = fname
        _update_data(doc['_id'], key, fname, collection)

    if fname is None:
        return None

    _play_mp3(fname)


def print_data(doc, collection=None):
    print_word(doc)
    play_pron(doc, collection=collection)
    print_means(doc)
    print()


def main():
    from console_dict.jinshan import jinshan
    doc = jinshan('hello')
    print_data(doc)


if __name__=='__main__':
    main()