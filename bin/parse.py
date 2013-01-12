#!/usr/bin/python

from tokenize import *
import sys
import json
import os
import shutil

from genshi.template import TextTemplate

dest = 'www'

def process_template(template_file, outfile, params):
  fh = open(template_file)
  tmpl = TextTemplate(fh.read())
  stream = tmpl.generate(title=params["title"], content=params["content"])

  path = os.path.dirname(outfile)
  if not os.path.exists(path):
    os.makedirs(path)

  out = open(outfile, 'w')
  out.write(stream.render())
  out.close()


def process(file, outfile):
  if file[-3:] != '.py':
    return
  print 'Processing {} to {}'.format(file, outfile)

  fh = open(file)
  g = generate_tokens(fh.readline)
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
  content = '<h1>' + file + '</h1>\n'
  content += '<ul>\n'
  for k in data.keys():
    content += '<li>{} {}</li>\n'.format(k, data[k])
  content += '</ul>\n'
  process_template('template/main.tmpl', dest + outfile + '.html',
     {'title' : file, 'content' : content})

def process_dir(args, dirname, fnames):

  print dirname
  #print fnames
  start = args["prefix"]
  # TODO: remove other unwanted names? and do it in a saner way!
  try:
    fnames.index('.git')
    fnames.remove('.git')
  except Exception:
    pass
  for f in fnames:
    file = os.path.join(dirname, f)
    if os.path.isfile(file):
      #print '  ' + f
      #print args["project_name"]
      #outfile = os.path.join(args["project_name"], file[start:])
      outfile = '/' + args["project_name"] + file[start:]
      process(file, outfile)

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
  for p in conf["projects"]:
    project_name = p["name"]
    root = p["root"]
    # Alternatively, if there is no root, but let's say it has a URL then we fetch the file,
    # unzip and work from there...
    os.path.walk(root, process_dir, { "project_name" : project_name, "prefix" : len(root) })

main()

