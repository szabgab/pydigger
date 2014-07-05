from wsgiref.util import setup_testing_defaults
from wsgiref.simple_server import make_server

import os,sys,cgi

def not_found(start_response):
	status = '404 Not Found'
	headers = [('Content-type', 'text/html')]
	start_response(status, headers)
	return 'Not Found'

def serve(environ, start_response):
	setup_testing_defaults(environ)


	web_path = environ['PATH_INFO']
	local_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	path = local_path + '/www' + web_path
	#sys.stderr.write(web_path + "\n")
	#sys.stderr.write(local_path + "\n")
	sys.stderr.write(path + "\n")
	# if path is a directory add index.html to the end of it
	if not os.path.exists(path):
		return not_found(start_response)


	# if no index.html, shall we provide directory listing?
	if os.path.isdir(path):
		path += '/index.html'

	if not os.path.exists(path):
		return not_found(start_response)

	fh = open(path, 'r')
	status = '200 OK'
	headers = [('Content-type', 'text/html')]
	start_response(status, headers)
	return fh 
	
httpd = make_server('', 8000, serve)
print "Serving on port 8000..."
httpd.serve_forever()

