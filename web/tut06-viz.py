import os, os.path
import random
import string

import cherrypy

class StringGenerator(object):
    @cherrypy.expose
    def index(self):
        return """<html>
          <head>
            <link href="/static/css/style.css" rel="stylesheet">
          </head>
      <body>
        <form method="get" action="generate">
          <input type="text" value="8" name="length" />
              <button type="submit">Give it now!</button>
        </form>
      </body>
    </html>"""

    @cherrypy.expose
    def generate(self, length=8):
        some_string = ''.join(random.sample(string.hexdigits, int(length)))
        cherrypy.session['mystring'] = some_string
        return some_string

    @cherrypy.expose
    def display(self):
        return cherrypy.session['mystring']

    @cherrypy.expose
    def control(self, id="AU-5"):
        return """<html>
          <head>
            
          </head>
      <body>
        <p>/output/img/AU-5-precursors.svg</p>
        <p>path: {path}, sc_id: {sc_id}</p>
        <p>key: <span style="color: blue">organization</span> <span style="color: red">information system</span></p>
        
        <img src="/output/img/{sc_id}-precursors.svg" height="300">
      </body>
    </html>""".format( sc_id = id, path=os.path.abspath(os.getcwd()) )

if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        },
        '/output': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'output'
        }
    }
    cherrypy.quickstart(StringGenerator(), '/', conf)