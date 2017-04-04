# -*-coding:utf-8-*-

from optparse import OptionParser

from jinshan_dict import jinshan_dict


def main():
    usage = "usage: %prog [options] arg1 arg2"
    parser = OptionParser(usage=usage, version="%prog 0.0.1.dev1")
    parser.add_option('-w', '--word')
    (options, args) = parser.parse_args()
    jinshan_dict(options.word)


if __name__=="__main__":
    pass