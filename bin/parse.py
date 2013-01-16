#!/usr/bin/python

import argparse

from tokenize import *
import sys
import json
import os
import shutil
import re

import pygments
import pygments.lexers
import pygments.formatters

from genshi.template import TextTemplate

dest = 'www'
pages = []

def process_template(template_file, outpath, params):
  fh = open(template_file)
  tmpl = TextTemplate(fh.read())
  stream = tmpl.generate(title=params["title"], content=params["content"])

  path = os.path.dirname(outpath)
  if not os.path.exists(path):
    os.makedirs(path)

  out = open(outpath, 'w')
  out.write(stream.render())
  out.close()

def highlight(file):
  fh = open(file)
  code = fh.read()

  guessed_lexer = pygments.lexers.guess_lexer(code)
  #print guessed_lexer
  #print pygments.lex(code, pygments.lexers.CLexer())
  #html = pygments.highlight(code, pygments.lexers.CLexer(), pygments.formatters.html.HtmlFormatter())
  html = pygments.highlight(code, guessed_lexer, pygments.formatters.html.HtmlFormatter())
  return (guessed_lexer, html)
  
def analyze_file(file):
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
  return content

def process_file(file, outfile):
  print 'Processing {} to {}'.format(file, outfile)
  content = ''
  if file[-3:] == '.py':
    pass
    #content = analyze_file(file)

  if file[-4:] == '.png':
    return;

  hl = highlight(file)
  lexer = re.sub(r'[<>]', '', str(hl[0]))
  html = hl[1]
  content += '<p>Lexer: {}</p>{}'.format(lexer, html)
  process_template('template/main.tmpl', dest + outfile + '.html',
     {'title' : file, 'content' : content})
  pages.append({ "file" : outfile + '.html', "name" : file })

def process_dir(args, dirname, fnames):

  #print 'Dirname: ' + dirname
  #print fnames
  start = len(args["root"])
  # TODO: remove other unwanted names? and do it in a saner way!
  try:
    fnames.index('.git')
    fnames.remove('.git')
  except Exception:
    pass

  exclude_dirs = args.get("exclude dirs")
  if exclude_dirs != None:
    for dir in exclude_dirs:
      try:
        fnames.index(dir)
        fnames.remove(dir)
      except Exception:
        pass

  for f in fnames:
    file = os.path.join(dirname, f)
    if os.path.isfile(file):
      #print '  ' + f
      #print args["name"]
      #outfile = os.path.join(args["name"], file[start:])
      outfile = '/' + args["name"] + file[start:]
      try:
        process_file(file, outfile)
      except Exception as (e):
        print e
        pass

def read_arguments():
  ap = argparse.ArgumentParser(description="Digging Python projects")
  ap.add_argument('conf', help="json configuration file for example conf/name.json")
  ap.add_argument('--clear', help="clear the destination directory before starting the process", action='store_true')
  args = ap.parse_args()
  return args

def main():
  args = read_arguments()
  
  if args.clear and os.path.exists(dest):
    shutil.rmtree(dest)

  fh = open(args.conf)
  conf = json.load(fh)

  # Create destination directory and copy static files
  if not os.path.exists(dest):
    os.makedirs(dest)
  if os.path.exists(dest + '/bootstrap'):
    shutil.rmtree(dest + '/bootstrap')
  shutil.copytree('static/bootstrap', dest + '/bootstrap')
  # TODO all the files
  shutil.copy('static/robots.txt', dest)
  shutil.copy('static/pygments.css', dest)

  # delete existing tree?
  for p in conf["projects"]:
    project_name = p["name"]
    root = p["root"]
    # Alternatively, if there is no root, but let's say it has a URL then we fetch the file,
    # unzip and work from there...
    os.path.walk(root, process_dir, p) #{ "project_name" : project_name, "prefix" : len(root) })

    # add project index file listing all the files in the project
    content = '<ul>\n'
    for p in pages:
      content += '<li><a href="{}">{}</a></li>\n'.format(p["file"], p["name"])
    content += '</ul>\n'

    process_template('template/main.tmpl', dest + '/' + project_name + '/index.html',
       {'title' : 'PyDigger', 'content' : content})
    
    
  content = '<ul>\n'
  for p in conf["projects"]:
    content += '<li><a href="{}">{}</a></li>\n'.format(p["name"], p["name"])
  content += '</ul>\n'

  process_template('template/main.tmpl', dest + '/index.html',
     {'title' : 'PyDigger', 'content' : content})

  about = '''
  Created by <a href="http://szabgab.com/">Gabor Szabo</a>
  <p>
  Source code on <a href="http://github.com/szabgab/pydigger/">Github</a>.
  </p>
  '''
  process_template('template/main.tmpl', dest + '/about.html',
     {'title' : 'About PyDigger', 'content': about})
     
main()

