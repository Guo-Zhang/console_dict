#!/usr/bin/env python
# -*-coding:utf-8-*-

from __future__ import print_function, absolute_import

from xtls.colorful import Color,colorful_print


def print_word(doc):
    if doc['ph_am']:
        colorful_print("%s |%s|" % (doc['_id'], doc['ph_am']), Color.RED)
    else:
        colorful_print("%s" % (doc['_id']), Color.RED)


def print_means(doc):
    parts = doc['parts']
    for part in parts:
        colorful_print(" %s %s"%(part['part'],';'.join(part['means'])),Color.BLUE)


def print_data(doc):
    print_word(doc)
    print_means(doc)