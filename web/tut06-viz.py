import os, os.path
import sys
import random
import string
import cherrypy

sys.path.append(os.path.join('lib'))
sys.path.append(os.path.join('data'))
from seccontrol import SecControl
from seccontrolviz import SecControlViz

class StringGenerator(object):
    @cherrypy.expose
    def index(self):
        return """<html>
          <head>
            <link href="/static/css/style.css" rel="stylesheet">
          </head>
      <body>
        <form method="get" action="control">
          800-53 control id: <input type="text" value="AU-3" name="id" />
              <button type="submit">illucitato!</button>
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
        id = id.upper()
        sc = SecControl(id)
        cv = SecControlViz(id)

        # create graphviz file
        cv.precursor_list(cv.dep_dict, id, cv.nodes)
        # create edges
        for node in cv.nodes:
            cv.precursor_edges(cv.dep_dict, node, cv.edges)
        digraph = cv.add_nodes(cv.digraph(), cv.node_options_tuples(cv.nodes))
        # print "<%s>" % digraph

        # weak test, first delete file if exists
        try:
            os.remove("output/img/%s-precursors" % id)
            os.remove("output/img/%s-precursors.%s" % (id, cv.vizformat))
        except OSError:
            pass
        # generate graphviz file
        cv.add_edges(cv.add_nodes(cv.digraph(), cv.node_options_tuples(cv.nodes)),
            cv.edges
        ).render("output/img/%s-precursors" % id)
        
        # render html page
        return """<html>
          <head>
            <title>800-53 Control {sc_id}</title>
          </head>
      <body>
        <form method="get" action="control">
          800-53 control id: <input type="text" value="" name="id" />
              <button type="submit">illucitato!</button>
        </form>

        <h3>({sc_id}) {sc_title}</h3>
        <p style="width:800;">{sc_desc}</p>
        <!--p>/output/img/AU-5-precursors.svg</p-->
        <!--p>path: {path}, sc_id: {sc_id}</p-->
        <p>key: <span style="color: blue">organization</span> <span style="color: red">information system</span></p>
        
        <img src="/output/img/{sc_id}-precursors.svg" height="300">
      </body>
    </html>""".format( sc_id = id, sc_title = sc.title, sc_desc = "<br />".join(sc.description.split("\n")), path=os.path.abspath(os.getcwd()) )

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