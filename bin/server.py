import cherrypy
import datetime

class HelloWorld:
    def index(self):
        return "Hello world! " + str(datetime.datetime.now())
    def default(self, project):
        return "Default! " + project + ' ' + str(datetime.datetime.now())
    default.exposed = True
    index.exposed = True

cherrypy.quickstart(HelloWorld())
