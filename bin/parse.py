#!/usr/bin/python

#import tokenize
from tokenize import *
import sys

def process(file):
  print 'Processing ' + file
  fh = open(file)
  g = generate_tokens(fh.readline)
  #print g
  tree = []
  for toknum, tokval, tokstart, tokend, tokline in g:
    # 1  NAME  (from, tokenize, import, def, process,...)
    # 4  NEWLINE

    # added by the tokenizer
    # 53 COMMENT comments starting with # and sh-bang?
    # 54 NL

    # 55 N_TOKENS  (if I understand this is the non-token, that is the number above the largest one in use)
    print toknum, tokval
    #print tokval
    #if tokval == 'import':
    #    print toknum


def main():

  if len(sys.argv) == 1:
    print 'Usage: ' + sys.argv[0] + '  FILENAME.s'
    exit()

  for i in range(1, len(sys.argv)):
    process(sys.argv[i])


main()

