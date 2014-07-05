from __future__ import print_function, division
import urllib2, feedparser, re, json

#import pkg_resources

rss_feed = 'https://pypi.python.org/pypi?%3Aaction=rss'
def run():
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
		url = 'http://pypi.python.org/pypi/{}/{}/json'.format(package, version)
		#print(url)
		w = urllib2.urlopen(url)
		json_string = w.read()
		#print(json_string)
		data = json.loads(json_string)
		print(data['releases'][version][0]['url']);

		# It seems that a package might be already included in the RSS feed even before it was indexed by Pypi
		# and so it does not yet have the details in the 'releases' and in the 'urls'
		# we might need to take this in account when processng packages
		# or maybe if there are multiple version numbers in the 'releases' ?

		break
	## fetch the rss feed
	## list the most recent package names and version numbers

	## fetch the json file of each package
    ## http://pypi.python.org/pypi/<package_name>/<version>/json

	# add information to a database

	# download each package
	# unzip them
	# collect information about the package (list of files)

	


#    check_dist('pydigger')
#    print(hi())

#def hi():
#    return "Hi from PyDigger"
#
#def check_dist(dist_name):
#    try:
#        bm = pkg_resources.get_distribution(dist_name)
#    except pkg_resources.DistributionNotFound:
#        print("Distribution '{}' not found".format(dist_name))
#        return
#
#    print(bm.requires())
#    print(bm.version)

