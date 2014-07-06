from __future__ import print_function, division
import urllib, urllib2, feedparser, re, json, os
from pymongo import MongoClient

#import pkg_resources

root = 'www';

rss_feed = 'https://pypi.python.org/pypi?%3Aaction=rss'
def run():
	mongo_client = MongoClient('localhost', 27017)
	mongo_db = mongo_client.pydigger
	packages = mongo_db.packages

	w = urllib2.urlopen(rss_feed)
	rss = w.read()
	#print(rss);
	feed = feedparser.parse( rss )
	#print(feed)
	#for k in feed.keys():
	#	print(k)
	#	raw_input('')
	#	print(feed[k])
	#	raw_input('')
	#print(type(feed['entries'])) # list
	for v in feed['entries']:
		#print(type(v))
		#for k in v.keys():
		#	print(k)
		#	print(v[k])
		#	print('----')
		v['link']   # http://pypi.python.org/pypi/getvps/0.1
		# check if link matches the format we are expecting:
		# http://pypi.python.org/pypi/<package>/<version>
		match = re.search(r'http://pypi.python.org/pypi/([^/]+)/([^/]+)$', v['link'])
		if not match:
			print("ERROR: url {} does not match the expected format".format(v['link']))
			continue

		package = match.group(1)
		version = match.group(2)

		data = packages.find_one({'package' : package, 'version' : version });
		if data and data['status'] != 'waiting':
			print("LOG: package {} version {} are already in the database".format(package, version))
			continue

		if not data:
			data = {
				'package' : package,
				'version' : version,
				'status'  : 'waiting'
			}
			packages.insert(data)
			print("LOG: adding package {} version {} to the database ".format(package, version))
			data = packages.find_one({'package' : package, 'version' : version });

		#print(data)
		if 'zip_url' not in data:
			url = 'http://pypi.python.org/pypi/{}/{}/json'.format(package, version)
			w = urllib2.urlopen(url)
			json_string = w.read()
			#print(json_string)
			package_info = json.loads(json_string)
			zip_url = package_info['releases'][version][0]['url']
			if zip_url:
				data['zip_url'] = zip_url
				print("LOG: saving zip_url {}".format(data['zip_url']))
				packages.save(data)
			else:
				print("LOG: zip_url missing from json for package {} version {}".format(package, version))

		# It seems that a package might be already included in the RSS feed even before it was indexed by Pypi
		# and so it does not yet have the details in the 'releases' and in the 'urls'
		# we might need to take this in account when processng packages
		# or maybe if there are multiple version numbers in the 'releases' ?

		# remove the URL from the beginning of the zip_url and add it to the path to 'root'
		m = re.search(r'^https://pypi.python.org/(.*)', data['zip_url'])
		if not m:
			print("ERROR: zi_url prefix does not match {}".format(data['zip_url']))
			continue
		local_path = root + '/' + m.group(1)
		if not os.path.exists(os.path.dirname(local_path)):
			print("LOG: creating dir {}".format(os.path.dirname(local_path)))
			os.makedirs(os.path.dirname(local_path))
		print("LOG: downloading {} to {}".format(data['zip_url'], local_path))
		urllib.urlretrieve(data['zip_url'], local_path)

		break
	## fetch the rss feed
	## list the most recent package names and version numbers

	## fetch the json file of each package
    ## http://pypi.python.org/pypi/<package_name>/<version>/json

	# add information to a database

	# download each package
	# unzip them
	# collect information about the package (list of files)

