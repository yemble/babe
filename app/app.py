#!/usr/bin/env python

import os, logging

import api, actions

from flask import Flask, request, send_from_directory, render_template
app = Flask(__name__)

# probably don't have to modify this file, except for any custom api or action endpoints in add_routes()
# see "hello" examples below

def page_handler(name):
	tpl = name + '.tpl.html'
	logging.debug('Rendering template file %s', tpl)
	return render_template(tpl)

def static_handler(path=''):
	DEFAULT = 'index.html'
	if path == '':
		path = DEFAULT
	if path.endswith('/'):
		path = path + DEFAULT
	prefix = os.path.dirname(path)
	file = os.path.basename(path)
	dir = os.path.join('./static', prefix)
	logging.debug('Sending static file %s', os.path.join(dir, file))
	return send_from_directory(dir, file)

def add_routes():
	# GET    /api/v1/data/<table>/[/col/<val>]..
	# DELETE /api/v1/data/<table>/col/<val>[/col/<val>]..
	# PUT    /api/v1/data/<table>/col/<val>[/col/<val>]..
	# POST   /api/v1/data/<table>

	# Data: select & insert on all
	app.add_url_rule('/api/v1/data/<table>',             'api_data_table',      api.data_handler, methods=['GET','POST'])
	# Data: select, insert, update on all
	app.add_url_rule('/api/v1/data/<table>/<path:path>', 'api_data_table_path', api.data_handler, methods=['GET','POST','PUT'])

	# Data: delete on all (you probably don't want this!)
	#app.add_url_rule('/api/v1/data/<table>/<path:path>', 'api_data_table_path_delete', api.data_handler, methods=['DELETE'])

	# Data: example to allow delete on one table only
	#app.add_url_rule('/api/v1/data/sprocket/<path:path>', 'api_data_sprocket_delete', api.data_handler, methods=['DELETE'], defaults={'table': 'sprocket'})

	# custom api method, returns json just like data methods
	app.add_url_rule('/api/v1/hello', 'api_hello', api.hello_handler, methods=['GET'])

	# custom action, could return templated html, or a 302 redirect to some other page
	app.add_url_rule('/go/to/hello', 'action_hello', actions.hello_handler, methods=['POST'])

	# generic page handler, looks for a matching tpl.html in templates/
	app.add_url_rule('/page/<name>', 'page', page_handler, methods=['GET'])

	# generic static doc handler, looks for a matching file in static/
	app.add_url_rule('/', 'static_index', static_handler, methods=['GET'])
	app.add_url_rule('/<path:path>', 'static_default', static_handler, methods=['GET'])

if __name__ == '__main__':
	debug = os.environ.get('DEBUG', False)

	logging.basicConfig(format = '%(asctime)-15s %(levelname)s %(message)s', level = logging.DEBUG if debug else logging.INFO)

	add_routes()
	app.run(debug=debug, host='0.0.0.0', port=int(os.environ.get('HTTP_PORT', 8000)))
