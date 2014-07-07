#!/usr/bin/env python
from bottle import Bottle, template, abort, TEMPLATE_PATH
from pymongo import MongoClient
import os,sys

mongo_client = MongoClient('localhost', 27017)
mongo_db = mongo_client.pydigger
packages = mongo_db.packages

app = Bottle()


TEMPLATE_PATH.append( os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/views' )

def mytemplate(file, **args):
	last_update = mongo_db.meta.find_one({ 'name' : 'last_update' })
	args['last_update'] = last_update['value']
	return template(file, **args)

@app.route('/')
def index():
	return mytemplate('list.tpl', pkgs=packages.find())

@app.route('/package/<name>')
def hello(name):
	pkgs = []
	for p in packages.find({'package' : name}):
		pkgs.append(p)

	if len(pkgs) > 0:
		return mytemplate('package.tpl', name=name, pkgs=pkgs, title=name)
	else:
		return abort(404, 'No such package found')

@app.route('/stats')
def stats():
	pkg_count=packages.find().count()
	return mytemplate('stats.tpl', pkg_count=pkg_count)


@app.route('/about')
def about():
	return mytemplate('about.tpl')

if len(sys.argv) > 1 and sys.argv[1] == 'paste':
	app.run(host='localhost', port=8080, server='paste')
else:
	app.run(host='localhost', port=8080)

