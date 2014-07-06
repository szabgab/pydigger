from bottle import route, run, template
from pymongo import MongoClient

mongo_client = MongoClient('localhost', 27017)
mongo_db = mongo_client.pydigger
packages = mongo_db.packages


@route('/')
def index():
	html = '<ul>';
	for p in packages.find():
		html += '<li>' + p['package'] + '</li>'
	html += '</ul>'
	return html 

@route('/hello/<name>')
def hello(name):
	return template('<b>Hello {{name}}</b>!', name=name)

@route('/about')
def about():
	return 'PyDigger is being built by <a href="http://szabgab.com/">Gabor Szabo</a>'

run(host='localhost', port=8080)

