from __future__ import print_function, division
import pymongo
import urllib, urllib2, feedparser, re, json, os, tarfile, zipfile, time, argparse
from datetime import datetime
import logging

import signal
import pygments
import pygments.lexers
import pygments.formatters

src_root = 'www'
html_root = 'html'
rss_feed = 'https://pypi.python.org/pypi?%3Aaction=rss'

class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
	raise TimeoutException()

class PyDigger(object):
	def __init__(self):
		self.argparser = argparse.ArgumentParser()
		self.argparser.add_argument('--rss', help='process PyPi RSS feed', action='store_true')
		self.args = self.argparser.parse_args()

		logdir = 'log'
		if not os.path.exists(logdir):
		  os.makedirs(logdir)
		logfile_name = '{}/pydigger-{}.log'.format(logdir, datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
		logging.basicConfig(filename= logfile_name, level= logging.DEBUG)

	def find_or_create_pkg_info(self, link):
		#link   # http://pypi.python.org/pypi/getvps/0.1
		# check if link matches the format we are expecting:
		# http://pypi.python.org/pypi/<package>/<version>
		match = re.search(r'http://pypi.python.org/pypi/([^/]+)/([^/]+)$', link)
		if not match:
			logging.error("url {} does not match the expected format".format(link))
			return False
	
		package = match.group(1)
		version = match.group(2)
	
		data = self.packages.find_one({'package' : package, 'version' : version })
		if not data:
			data = {
				'package' : package,
				'version' : version,
				'status'  : 'waiting_for_zip_url'
			}
			logging.info("adding package {} version {} to the database ".format(package, version))
			self.packages.insert(data)
			data = self.packages.find_one({'package' : package, 'version' : version })
	
		if not data:
			logging.fatal("data just added and cannot be found? package {} version {}".format(package, version))
			return False

		self.data = data
		return True

	def get_zip_url(self):
		if 'zip_url' in self.data:
			return True

		version = self.data['version']
		url = 'http://pypi.python.org/pypi/{}/{}/json'.format(self.data['package'], version)
		try:
			w = urllib2.urlopen(url)
			json_string = w.read()
		except Exception as (e):
			logging.error("Could not fetch {}  {}".format(url, e))
			return False

		#logging.debug("json_string: {}".format(json_string))
		package_info = json.loads(json_string)

		# check if deep data structure exists with try/except
		try:
			self.data['zip_url']     = package_info['releases'][version][0]['url']
			self.data['upload_time'] = package_info['releases'][version][0]['upload_time']
		except:
			logging.info("zip_url missing from json for package {} version {} try this url: {}".format(self.data['package'], self.data['version'], url))
			return False

		self.data['package_info'] = {}
		self.data['package_info']['info'] = package_info['info']

	
		self.data['status']  = 'zip_url_found'
		logging.info("zip_url {} found in json".format(self.data['zip_url']))
		self.packages.save(self.data)
		return True

	def download_zip_file(self):
		if self.data['status'] == 'error_unknown_zip_url_prefix':
			return False
		if self.data['status'] == 'error_unknown_zip_file_type':
			return False

		# remove the URL from the beginning of the zip_url and add it to the path to 'src_root'
		m = re.search(r'^https://pypi.python.org/(.*)', self.data['zip_url'])
		if not m:
			logging.error("zip_url prefix does not match {}".format(self.data['zip_url']))
			self.data['status'] = 'error_unknown_zip_url_prefix'
			self.packages.save(self.data)
			return False
	
		local_zip_file = src_root + '/' + m.group(1)
		local_path = os.path.dirname(local_zip_file)
		if not os.path.exists(local_zip_file):
			if not os.path.exists(local_path):
				logging.info("creating dir {}".format(local_path))
				os.makedirs(local_path)
			logging.info("downloading {} to {}".format(self.data['zip_url'], local_zip_file))
			urllib.urlretrieve(self.data['zip_url'], local_zip_file)
	
		m = re.search(r'(.*)(\.tar\.gz|\.zip)$', local_zip_file)
		if m:
			project_path = m.group(1)
			extension    = m.group(2)
			if not os.path.exists(project_path):
				logging.info("unzipping {} to {} using {}".format(local_zip_file, local_path, extension))
				if extension == '.tar.gz':
					tar = tarfile.open(local_zip_file)
					tar.extractall(path=local_path)
					tar.close()
				elif extension == '.zip':
					tar = zipfile.ZipFile(local_zip_file)
					tar.extractall(path=local_path)
					tar.close()
				else:
					raise(Exception('Internal error. Unknown extension: {}'.format(extension)))
		else:
			self.data['status'] = 'error_unknown_zip_file_type'
			logging.error("unknown zip file type {}".format(local_zip_file))
			self.packages.save(self.data)
			return False
	
		# list all the files in the project_path and add it to the database
		if 'files' not in self.data:
			self.data['local_path'] = local_path[len(src_root)+1:]
			self.data['project_path'] = project_path[len(src_root)+1:]
			self.data['files'] = []
			for dirname, dirnames, filenames in os.walk(project_path):
				for filename in filenames:
					file_path = os.path.join(dirname, filename)[len(project_path)+1:]
					self.data['files'].append(file_path)
			self.packages.save(self.data)
		return True

	def highlight(self, file):
		# for now only try to process .py files
		if file[-3:] != '.py':
			return
		if 'project_path' not in self.data:
			return;
		path = src_root + '/' + self.data['project_path'] + '/' + file
		out_file = html_root + '/' + self.data['project_path'] + '/' + file
		out_path = os.path.dirname(out_file)
		if os.path.exists(out_file):
			return
		#logging.debug("syntax highlighting {}".format(path))

		fh = open(path)
		code = fh.read()
		fh.close()

		guessed_lexer = pygments.lexers.guess_lexer(code)
		used_lexer = guessed_lexer
		if file[-3:] == '.py':
			used_lexer = pygments.lexers.PythonLexer()
		#logging.debug("File {} Guessed Lexer: {} Used Lexer: {}".format(file, guessed_lexer, used_lexer))


		# Some lexers:
		# pygments.lexers.HaxeLexer
		# pygments.lexers.PerlLexer
		# pygments.lexers.PythonLexer
		# pygments.lexers.VelocityXmlLexer
		# pygments.lexers.RstLexer
		# pygments.lexers.GroffLexer
		# pygments.lexers.SourcesListLexer
		# pygments.lexers.XmlLexer
		# pygments.lexers.PrologLexer


		timeout = 10
		start = time.time()
		signal.signal(signal.SIGALRM, timeout_handler)
		signal.alarm(timeout)
		try:
			html = pygments.highlight(code, used_lexer, pygments.formatters.html.HtmlFormatter())
		except TimeoutException:
			html = 'Timeout'
			logging.error('Timeout when running syntax highlighting for {}'.format(file))
		end   = time.time()
		logging.info("Syntaxt highlighting {} with lexer: {} ellapsed time: {}".format(file, used_lexer, end - start))
		if not os.path.exists(out_path):
			os.makedirs(out_path)
		fh = open(out_file, 'w')
		fh.write(html.encode('utf8'))
		fh.close()

		return {
			'guessed_lexer' : guessed_lexer,
			'used_lexer'    : used_lexer,
			'html'          : html
		}


	def connect_to_mondodb(self):
		try:
			self.mongo_client = pymongo.MongoClient('localhost', 27017)
			self.mongo_db = self.mongo_client.pydigger
			self.packages = self.mongo_db.packages
			self.meta     = self.mongo_db.meta
			return True
		except pymongo.errors.ConnectionFailure:
			logging.fatal("Could not connect to MongoDB. Exiting")
			return False

	def parse_feed(self):
		try:
			w = urllib2.urlopen(rss_feed)
			rss = w.read()
		except urllib2.URLError:
			logging.error("Could not fetch RSS feed from PyPi. Exiting.")
			return
		
		feed = feedparser.parse( rss )
		for v in feed['entries']:
			if not self.find_or_create_pkg_info(v['link']):
				continue
	
			# It seems that a package might be already included in the RSS feed even before it was indexed by PyPi
			# and so it does not yet have the details in the 'releases' and in the 'urls'
			# we might need to take this in account when processing packages
			# or maybe if there are multiple version numbers in the 'releases' ?
	
			if not self.get_zip_url():
				continue
	
			if not self.download_zip_file():
				continue

			if 'files' in self.data:
				for f in self.data['files']:
					self.highlight(f)

	def save_last_updates(self):
		last_update = self.meta.find_one({ 'name' : 'last_update' })
		if not last_update:
			self.meta.insert({ 'name' : 'last_update' })
			last_update = self.meta.find_one({ 'name' : 'last_update' })

		last_update['value'] = datetime.utcnow()
		self.meta.save(last_update)

	# fetch the rss feed
	# list the most recent package names and version numbers
	# fetch the json file of each package
    # http://pypi.python.org/pypi/<package_name>/<version>/json
	# add information to a database
	# download each package
	# unzip them

	# collect information about the package (list of files)
	def run(self):

		start = time.time()
		logging.info("Start at {}".format(start))
		if not self.connect_to_mondodb():
			return

		if self.args.rss:
			self.parse_feed()
			self.save_last_updates()
		else:
			self.argparser.print_help()

		end   = time.time()

		logging.info("DONE. Elapsed time: {}".format(end - start))

