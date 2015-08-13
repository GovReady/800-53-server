import os, os.path
import sys
import random
import string
import json
import cherrypy

sys.path.append(os.path.join('lib'))
sys.path.append(os.path.join('data'))
from seccontrol import SecControl
from seccontrolviz import SecControlViz
from utilities import *


class StringGenerator(object):
    @cherrypy.expose
    def index(self):
        return """<html>
          <head>
            <title>800-53 Control</title>
            <link rel="stylesheet" type="text/css" href="/assets/css/main.css">
          </head>
      <body>

        <form id="form_lookup" method="get" action="control">
          800-53 control id: <input type="text" value="AU-4" name="id" />
              <button type="submit">Show me!</button>
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
    def error404(self):
        return """<html>
          <head>
            <title>800-53 Control Error 404</title>
            <link rel="stylesheet" type="text/css" href="/assets/css/main.css">
          </head>
      <body>

        <form id="form_lookup" method="get" action="control">
          800-53 control id: <input type="text" value="" name="id" />
              <button type="submit">Show me!</button>
        </form>
        

        <h2>Error - 404</h2>
        These are not the controls you are looking for...
        """


    @cherrypy.expose
    def control(self, id="AU-4", format="html"):
        id = id.upper()
        sc = SecControl(id)
        if sc.title is None and sc.description is None and format == "html":
            # control does not exist, return 404
            print "\n*** control does not exist"
            raise cherrypy.HTTPRedirect("/error404")
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
        graph_label = "%s Control Chain" % (id)
        cv.add_edges(cv.add_nodes(cv.digraph(engine='dot', graph_attr={'label': graph_label, 'labelloc': 'bottom', 'labeljust': 'center', 'fontcolor':'slategray', 'fontname':'Arial', 'fontsize': '14', 'K': '4.6'}), cv.node_options_tuples(cv.nodes)),
            cv.edges
        ).render("output/img/%s-precursors" % id)

        # read contents of svg file into variable
        with open("output/img/%s-precursors.svg" % id, "r") as svg_file:
            svg_content = svg_file.read()

        # render json
        if format == "json":
            cherrypy.response.headers['Content-Type'] = 'application/json'
            if sc.title is None and sc.description is None:
                raise cherrypy.HTTPError("404 Not Found", "The requested resource does not exist")
            return json.dumps(sc.get_control_json())
        
        # render html page
        return """<html>
          <head>
            <title>800-53 Control {sc_id}</title>
            <link rel="stylesheet" type="text/css" href="/assets/css/main.css">
          </head>
      <body>

        <form id="form_lookup" method="get" action="control">
          800-53 control id: <input type="text" value="" name="id" />
              <button type="submit">Show me!</button>
        </form>
        

        <h2>({sc_id}) {sc_title}</h2>
        
        <!--h3>Control Description</h3-->
        <p style="width:800;">{sc_desc}</p>
        
        <!-- add in svg block into html page -->
        <h4>Control Dependency Chain</h4>
        <div id="graph">
            {sc_svg}
        </div>
        <div id="graphkey">
            key: 
            <div style="color: cornflowerblue">blue is organization responsibility</div>
            <div style="color: palevioletred">light red is information system responsibility</div>
        </div>

        <h3>Supplemental Guidance</h3>
        <p>{sc_suppl}</p>
 
      </body>
    </html>""".format( sc_id = id, sc_title = sc.title, sc_desc = replace_line_breaks(sc.description, "\n", "<br />"),
                sc_svg = svg_content, sc_suppl = replace_line_breaks(sc.supplemental_guidance), path=os.path.abspath(os.getcwd()) )

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
        },
        '/assets': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'web/assets'
        }
    }
    cherrypy.quickstart(StringGenerator(), '/', conf)