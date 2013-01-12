#!/usr/bin/python

from tokenize import *
import sys
import json
import os
import shutil

from genshi.template import TextTemplate

dest = 'www'

def process_template(template_file, outfile):
  fh = open(template_file)
  tmpl = TextTemplate(fh.read())
  stream = tmpl.generate(title='Foo')

  path = os.path.dirname(outfile)
  if not os.path.exists(path):
    os.makedirs(path)

  out = open(outfile, 'w')
  out.write(stream.render())
  out.close()


def process(file):
  print 'Processing ' + file
  fh = open(file)
  g = generate_tokens(fh.readline)
  #print g
  data = {}
  for toknum, tokval, tokstart, tokend, tokline in g:
    if toknum == NAME:
        if data.get(tokval) == None:
            data[tokval] = 0
        data[tokval] += 1
    # 1  NAME  (from, tokenize, import, def, process,...)
    # 4  NEWLINE

    # added by the tokenizer
    # 53 COMMENT comments starting with # and sh-bang?
    # 54 NL

    # 55 N_TOKENS  (if I understand this is the non-token, that is the number above the largest one in use)
    #print toknum, tokval
    #print tokval
    #if tokval == 'import':
    #    print toknum
  process_template('template/main.tmpl', dest + '/index.html')

def main():

  if len(sys.argv) == 1:
    print 'Usage: ' + sys.argv[0] + '  conf/name.json'
    exit()

  fh = open(sys.argv[1])
  conf = json.load(fh)

  # Create destination directory and copy static files
  if not os.path.exists(dest):
    os.makedirs(dest)
  if os.path.exists(dest + '/bootstrap'):
    shutil.rmtree(dest + '/bootstrap')
  shutil.copytree('static/bootstrap', dest + '/bootstrap')
  shutil.copy('static/robots.txt', dest)

  # delete existing tree?
  for p in conf["things"]:
    process(p["file"])

main()

