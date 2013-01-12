#!/usr/bin/python

from tokenize import *
import sys
import json
import os

#from genshi.template import TemplateLoader
from genshi.template import TextTemplate

#loader = TemplateLoader(
#    os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'),
#    auto_reload=True
#)

def process_template(template_file, outfile):
#  tmpl = loader.load(template_file)
#  template = tmpl.generate(title='Geddit').render('html', doctype='html')
  fh = open(template_file)
  tmpl = TextTemplate(fh.read())
  stream = tmpl.generate(title='Foo')
  #print stream
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
  process_template('template/main.tmpl', 'html/index.html')

def main():

  if len(sys.argv) == 1:
    print 'Usage: ' + sys.argv[0] + '  conf/name.json'
    exit()

  fh = open(sys.argv[1])
  conf = json.load(fh)

  # delete existing tree?
  for p in conf["things"]:
    process(p["file"])


main()

