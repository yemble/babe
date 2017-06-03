
import os
from flask import request, jsonify, redirect

from data import PgSession

def hello_handler():
	data = {
		'hello': 'world'
	}
	return jsonify(data)


# Data api:

def data_handler(table, path=None):
	args = path.split('/') if path else []

	try:
		session = PgSession()

		if request.method == 'GET':
			conds = _data_conditions(args)
			rows = list( session.select(table, conds) )
			res = {
				'result': 'ok',
				'data': rows,
			}
			return jsonify(res)

		if request.method == 'DELETE':
			conds = _data_conditions(args)
			deleted = session.delete(table, conds)
			res = {
				'result': 'ok',
				'deleted': deleted,
			}
			return jsonify(res)
			
		if request.method == 'POST':
			updated = session.update(table, conds, request.json)
			res = {
				'result': 'ok',
				'updated': updated,
			}
			return jsonify(res)

		if request.method == 'POST':
			new_id = session.insert(table, request.json)
			return redirect(_data_url(table, new_id), 302)

	except Exception as e:
		res = {
			'result': 'error',
			'detail': '{}'.format(e),
		}
		return jsonify(res)

def _data_url(table, id):
	return '/api/v1/data/{}/{}'.format(table, id)

def _data_conditions(path_components):
	C = '='
	return [ (path_components[i], C, path_components[i+1],) for i in range(len(path_components)) if i % 2 == 0 ]
