#!/usr/bin/python

import tokenize
import sys

def process(file):
  print 'Processing ' + file
  fh = open(file, 'r')
  g = tokenize.generate_tokens(fh)
  print g
  #for t, _, _, _, _ in g:
  #  print t
  #  pass



def main():

  if len(sys.argv) == 1:
    print 'Usage: ' + sys.argv[0] + '  FILENAME.s'
    exit()

  for i in range(1, len(sys.argv)):
    process(sys.argv[i])


main()

