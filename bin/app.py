from bottle import Bottle, template, TEMPLATE_PATH
from pymongo import MongoClient
import os,sys

mongo_client = MongoClient('localhost', 27017)
mongo_db = mongo_client.pydigger
packages = mongo_db.packages

app = Bottle()


TEMPLATE_PATH.append( os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/views' )

@app.route('/')
def index():
	return template('list.tpl', pkgs=packages.find())

@app.route('/hello/<name>')
def hello(name):
	return template('<b>Hello {{name}}</b>!', name=name)

@app.route('/about')
def about():
	return template('about.tpl')

if len(sys.argv) > 1 and sys.argv[1] == 'paste':
	app.run(host='localhost', port=8080, server='paste')
else:
	app.run(host='localhost', port=8080)

