#!/usr/bin/env python
from bottle import Bottle, template, abort, TEMPLATE_PATH, response
from pymongo import MongoClient
import os,sys,re

mongo_client = MongoClient('localhost', 27017)
mongo_db = mongo_client.pydigger
packages = mongo_db.packages

app = Bottle()

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_PATH.append( root + '/views' )

def mytemplate(file, **args):
	last_update = mongo_db.meta.find_one({ 'name' : 'last_update' })
	args['last_update'] = last_update['value']
	return template(file, **args)

@app.route('/')
def index():
	return mytemplate('list.tpl', pkgs=packages.find())

@app.route('/packages/<path:path>')
def source(path):
	if re.search(r'\.\.', path):
		return abort(404, 'Invalid request')

	full_path = root + '/www/packages/' + path
	if not os.path.exists(full_path):
		return abort(404, 'File not found')

	response.set_header('Content-type', 'text/plain')
	fh = open(full_path)
	return fh.read()

@app.route('/package/<name>')
def package(name):
	pkgs = []
	for p in packages.find({'package' : name}):
		pkgs.append(p)

	if len(pkgs) > 0:
		pkgs.sort(reverse=True, key=lambda(f): f['upload_time'] if 'upload_time' in f else 0)
		return mytemplate('package.tpl', name=name, pkgs=pkgs, title=name)
	else:
		return abort(404, 'No such package found')

@app.route('/stats')
def stats():
	pkg_count=packages.find().count()
	st = {}
	statuses = [
		'waiting_for_zip_url',
		'error_unknown_zip_file_type',
		'error_unknown_zip_url_prefis',   # typo in indexer
		'error_unknown_zip_url_prefix',
		'zip_url_found'
	]
	for s in statuses:
		st[s] = packages.find({'status' : s}).count()

	return mytemplate('stats.tpl', pkg_count=pkg_count, statuses=st)


@app.route('/about')
def about():
	return mytemplate('about.tpl')

if len(sys.argv) > 1 and sys.argv[1] == 'paste':
	app.run(host='localhost', port=8080, server='paste')
else:
	app.run(host='localhost', port=8080, reloader=True, debug=True)

